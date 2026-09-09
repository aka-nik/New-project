"""Run deterministic quality checks against the source CSV tables."""

import argparse
import csv
import json
from pathlib import Path

from sentinel.quality import KeyColumns, evaluate_csv


TABLES = {
    "orders": ("olist_orders_dataset.csv", "order_id"),
    "order_items": ("olist_order_items_dataset.csv", ("order_id", "order_item_id")),
    "customers": ("olist_customers_dataset.csv", "customer_id"),
    "products": ("olist_products_dataset.csv", "product_id"),
    "payments": ("olist_order_payments_dataset.csv", ("order_id", "payment_sequential")),
    "reviews": ("olist_order_reviews_dataset.csv", "review_id"),
    "sellers": ("olist_sellers_dataset.csv", "seller_id"),
    "geolocation": (
        "olist_geolocation_dataset.csv",
        None,
    ),
    "category_translation": (
        "product_category_name_translation.csv",
        "product_category_name",
    ),
}


def check_csv(path: Path, key_column: KeyColumns) -> tuple[int, int, dict[str, int]]:
    """Return row count, duplicate key count, and missing values by column."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        key_columns = (
            [key_column]
            if isinstance(key_column, str)
            else list(key_column or [])
        )
        keys: list[tuple[str, ...]] = []
        missing = {column: 0 for column in reader.fieldnames or []}
        row_count = 0
        for row in reader:
            row_count += 1
            keys.append(tuple(row[column] for column in key_columns))
            for column, value in row.items():
                if not value.strip():
                    missing[column] += 1

    duplicate_count = row_count - len(set(keys))
    return row_count, duplicate_count, missing


def build_quality_report(source_dir: Path) -> dict[str, dict[str, object]]:
    """Evaluate every configured source table, including missing-file statuses."""
    reports: dict[str, dict[str, object]] = {}
    for table_name, (filename, key_column) in TABLES.items():
        path = source_dir / filename
        if path.exists():
            reports[table_name] = evaluate_csv(path, key_column)
        else:
            reports[table_name] = {
                "path": str(path),
                "row_count": 0,
                "duplicate_count": 0,
                "missing_values": {},
                "status": "missing",
            }
    return reports


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the complete quality report as JSON to this path",
    )
    arguments = parser.parse_args()

    reports = build_quality_report(arguments.source_dir)
    for table_name, report in reports.items():
        key_column = TABLES[table_name][1]
        key_label = (
            "+".join(key_column)
            if isinstance(key_column, tuple)
            else key_column or "none"
        )
        missing_summary = ", ".join(
            f"{column}={count:,}"
            for column, count in report["missing_values"].items()
            if count
        ) or "none"
        print(f"{table_name}: {report['row_count']:,} rows ({report['status']})")
        print(f"  duplicate {key_label}: {report['duplicate_count']:,}")
        print(f"  missing values: {missing_summary}")

    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
