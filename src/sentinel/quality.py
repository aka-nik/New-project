"""Deterministic data-quality checks for source CSV tables."""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Sequence
from pathlib import Path


def schema_fingerprint(columns: Sequence[str]) -> str:
    """Return a stable fingerprint for an ordered CSV header."""
    payload = "\n".join(columns).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def evaluate_relationships(
    source_dir: str | Path,
    relationships: Sequence[tuple[str, str, str, str]],
) -> dict[str, int]:
    """Count child rows whose foreign key is absent from the parent table."""
    source_dir = Path(source_dir)
    results: dict[str, int] = {}
    for child_file, child_column, parent_file, parent_column in relationships:
        parent_path = source_dir / parent_file
        child_path = source_dir / child_file
        with parent_path.open("r", encoding="utf-8-sig", newline="") as handle:
            valid_keys = {
                row[parent_column] for row in csv.DictReader(handle)
            }
        with child_path.open("r", encoding="utf-8-sig", newline="") as handle:
            orphan_count = sum(
                1
                for row in csv.DictReader(handle)
                if row[child_column] not in valid_keys
            )
        relationship = (
            f"{child_file}:{child_column} -> {parent_file}:{parent_column}"
        )
        results[relationship] = orphan_count
    return results


def evaluate_csv(
    path: str | Path,
    key_column: str,
    quarantine_path: str | Path | None = None,
    expected_columns: Sequence[str] | None = None,
) -> dict[str, object]:
    """Return quality metrics for a CSV file and flag a failing run when issues are found."""
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        row_count = 0
        keys: list[str] = []
        rows: list[dict[str, str]] = []
        missing_values: dict[str, int] = {}

        for row in reader:
            row_count += 1
            rows.append(row)
            key_value = row.get(key_column, "")
            keys.append(str(key_value) if key_value is not None else "")
            for column in fieldnames:
                if column == key_column:
                    continue
                value = row.get(column, "")
                if value is None or str(value).strip() == "":
                    missing_values[column] = missing_values.get(column, 0) + 1

    duplicate_count = max(0, row_count - len({value for value in keys if value}))
    expected = list(expected_columns) if expected_columns is not None else None
    missing_columns = [
        column for column in expected or [] if column not in fieldnames
    ]
    unexpected_columns = [
        column for column in fieldnames if expected is not None and column not in expected
    ]
    schema_drift = bool(missing_columns or unexpected_columns)
    status = (
        "fail"
        if duplicate_count
        or any(count > 0 for count in missing_values.values())
        or schema_drift
        else "pass"
    )
    quarantined_count = 0

    if quarantine_path is not None:
        quarantine_path = Path(quarantine_path)
        quarantine_path.parent.mkdir(parents=True, exist_ok=True)
        key_counts: dict[str, int] = {}
        for key in keys:
            if key:
                key_counts[key] = key_counts.get(key, 0) + 1

        quarantine_rows: list[dict[str, str]] = []
        for row, key in zip(rows, keys):
            flags: list[str] = []
            if key and key_counts.get(key, 0) > 1:
                flags.append("duplicate_key")
            if not key:
                flags.append("missing_key")
            missing_columns = [
                column
                for column in fieldnames
                if column != key_column
                and (row.get(column) is None or str(row.get(column)).strip() == "")
            ]
            if missing_columns:
                flags.append(f"missing_values:{','.join(missing_columns)}")
            if flags:
                quarantine_rows.append({**row, "_dq_flags": ";".join(flags)})

        quarantine_fieldnames = [*fieldnames, "_dq_flags"]
        with quarantine_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=quarantine_fieldnames)
            writer.writeheader()
            writer.writerows(quarantine_rows)
        quarantined_count = len(quarantine_rows)

    return {
        "path": str(path),
        "schema_fingerprint": schema_fingerprint(fieldnames),
        "schema_drift": schema_drift,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "row_count": row_count,
        "duplicate_count": duplicate_count,
        "missing_values": missing_values,
        "status": status,
        "quarantined_count": quarantined_count,
    }


def evaluate_directory(
    source_dir: str | Path,
    table_specs: dict[str, tuple[str, str]],
    quarantine_dir: str | Path | None = None,
    expected_columns: dict[str, Sequence[str]] | None = None,
    relationships: Sequence[tuple[str, str, str, str]] | None = None,
) -> dict[str, dict[str, object]]:
    """Apply the CSV quality gate to each configured table in a directory."""
    source_dir = Path(source_dir)
    if quarantine_dir is not None:
        quarantine_dir = Path(quarantine_dir)
    reports: dict[str, dict[str, object]] = {}

    for table_name, (filename, key_column) in table_specs.items():
        path = source_dir / filename
        if not path.exists():
            reports[table_name] = {
                "path": str(path),
                "row_count": 0,
                "duplicate_count": 0,
                "missing_values": {},
                "status": "missing",
                "quarantined_count": 0,
            }
            continue
        table_quarantine = (
            quarantine_dir / f"{table_name}.csv"
            if quarantine_dir is not None
            else None
        )
        table_expected_columns = (
            expected_columns.get(table_name) if expected_columns is not None else None
        )
        reports[table_name] = evaluate_csv(
            path,
            key_column,
            table_quarantine,
            table_expected_columns,
        )

    if relationships is not None:
        table_names_by_file = {
            filename: table_name
            for table_name, (filename, _key_column) in table_specs.items()
        }
        relationship_results = evaluate_relationships(source_dir, relationships)
        for relationship, orphan_count in relationship_results.items():
            child_file = relationship.split(":", 1)[0]
            child_table = table_names_by_file.get(child_file)
            if child_table is None or child_table not in reports:
                continue
            report = reports[child_table]
            orphan_reports = report.setdefault("relationship_orphans", {})
            orphan_reports[relationship] = orphan_count
            if orphan_count:
                report["status"] = "fail"

    return reports
