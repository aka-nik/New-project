"""Check key relationships between the initial Olist source tables."""

import argparse
import csv
from pathlib import Path


def read_column(path: Path, column: str) -> set[str]:
    """Read one column into a set of unique values."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row[column] for row in csv.DictReader(handle)}


def count_orphans(path: Path, key_column: str, valid_keys: set[str]) -> int:
    """Count rows whose reference does not exist in the parent key set."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(
            1
            for row in csv.DictReader(handle)
            if row[key_column] not in valid_keys
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    arguments = parser.parse_args()
    source_dir = arguments.source_dir

    order_ids = read_column(source_dir / "olist_orders_dataset.csv", "order_id")
    customer_ids = read_column(
        source_dir / "olist_customers_dataset.csv", "customer_id"
    )
    product_ids = read_column(source_dir / "olist_products_dataset.csv", "product_id")

    checks = {
        "order_items.order_id -> orders.order_id": count_orphans(
            source_dir / "olist_order_items_dataset.csv", "order_id", order_ids
        ),
        "orders.customer_id -> customers.customer_id": count_orphans(
            source_dir / "olist_orders_dataset.csv", "customer_id", customer_ids
        ),
        "order_items.product_id -> products.product_id": count_orphans(
            source_dir / "olist_order_items_dataset.csv", "product_id", product_ids
        ),
    }

    for relationship, orphan_count in checks.items():
        print(f"{relationship}: {orphan_count:,} orphan rows")


if __name__ == "__main__":
    main()
