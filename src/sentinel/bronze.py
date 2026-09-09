"""Bronze-layer utilities for landing raw source files as partitioned Parquet."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pandas as pd


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ingest_csv_to_bronze(
    source_path: str | Path,
    bronze_dir: str | Path,
    ingest_date: str,
) -> dict[str, object]:
    """Read a CSV file, write a bronze Parquet file, and return a manifest."""
    source_path = Path(source_path)
    bronze_dir = Path(bronze_dir)

    table_name = source_path.stem.replace("olist_", "").replace("_dataset", "")
    target_dir = bronze_dir / table_name / f"ingest_date={ingest_date}"
    target_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = target_dir / "part-000.parquet"
    manifest_path = target_dir / "_manifest.json"
    source_sha256 = _sha256(source_path)

    if parquet_path.exists() and manifest_path.exists():
        existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing_manifest.get("source_sha256") == source_sha256:
            return existing_manifest

    df = pd.read_csv(source_path)
    df.to_parquet(parquet_path, index=False)

    manifest = {
        "source_file": source_path.name,
        "table_name": table_name,
        "ingest_date": ingest_date,
        "source_sha256": source_sha256,
        "row_count": int(len(df)),
        "schema": {
            "columns": df.columns.tolist(),
            "dtypes": {key: str(value) for key, value in df.dtypes.items()},
        },
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
