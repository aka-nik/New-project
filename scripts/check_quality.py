"""Run basic deterministic quality checks against selected CSV tables."""

import argparse
import csv
from pathlib import Path


TABLES = {
    "orders": ("olist_orders_dataset.csv", "order_id"),
    "order_items": ("olist_order_items_dataset.csv", "order_id"),
    "customers": ("olist_customers_dataset.csv", "customer_id"),
    "products": ("olist_products_dataset.csv", "product_id"),
}


def check_csv(path: Path, key_column: str) -> tuple[int, int, dict[str, int]]:
    """Return row count, duplicate key count, and missing values by column."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        keys: list[str] = []
        missing = {column: 0 for column in reader.fieldnames or []}
        row_count = 0
        for row in reader:
            row_count += 1
            keys.append(row[key_column])
            for column, value in row.items():
                if not value.strip():
                    missing[column] += 1

    duplicate_count = row_count - len(set(keys))
    return row_count, duplicate_count, missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    arguments = parser.parse_args()

    for table_name, (filename, key_column) in TABLES.items():
        row_count, duplicate_count, missing = check_csv(
            arguments.source_dir / filename, key_column
        )
        missing_summary = ", ".join(
            f"{column}={count:,}" for column, count in missing.items() if count
        ) or "none"
        print(f"{table_name}: {row_count:,} rows")
        print(f"  duplicate {key_column}: {duplicate_count:,}")
        print(f"  missing values: {missing_summary}")


if __name__ == "__main__":
    main()
