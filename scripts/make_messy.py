"""Create deliberately messy copies of source CSV files for quality-tests."""

import argparse
import csv
from pathlib import Path


def _empty_value_count(rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in rows
        for value in row.values()
        if value is None or value == ""
    )


def make_messy(source_dir: Path, output_dir: Path) -> dict[str, dict[str, int]]:
    """Write messy versions of source CSVs and return a defect summary."""
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict[str, int]] = {}

    orders_path = source_dir / "olist_orders_dataset.csv"
    if orders_path.exists():
        with orders_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        if rows:
            duplicate_row = rows[0].copy()
            duplicate_row["order_id"] = rows[0]["order_id"]
            duplicate_row["customer_id"] = f" {rows[0]['customer_id']} "
            duplicate_row["order_status"] = ""
            duplicate_row["order_purchase_timestamp"] = ""
            rows.append(duplicate_row)

            if len(rows) > 1:
                rows[1]["customer_id"] = f" {rows[1]['customer_id']} "
                rows[1]["order_status"] = ""

            target_path = output_dir / "olist_orders_dataset.csv"
            fieldnames = list(rows[0].keys())
            with target_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            duplicate_rows = sum(
                1
                for row in rows
                if row["order_id"] == rows[0]["order_id"]
            ) - 1
            summary["olist_orders_dataset.csv"] = {
                "duplicate_rows": duplicate_rows,
                "missing_values": _empty_value_count(rows),
                "category_variants": 0,
            }

    products_path = source_dir / "olist_products_dataset.csv"
    if products_path.exists():
        with products_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        if rows:
            variants = [
                "Electronics",
                "electronics",
                "ELECTRONIC",
                "Elec.",
                "Consumer Electronics",
            ]
            for index, row in enumerate(rows[: min(len(rows), len(variants))]):
                row["product_category_name"] = variants[index]
            rows[-1]["product_category_name"] = ""

            target_path = output_dir / "olist_products_dataset.csv"
            fieldnames = list(rows[0].keys())
            with target_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            summary["olist_products_dataset.csv"] = {
                "duplicate_rows": 0,
                "missing_values": _empty_value_count(rows),
                "category_variants": len({row["product_category_name"] for row in rows if row.get("product_category_name")}),
            }

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, help="Directory of clean source CSV files")
    parser.add_argument("output_dir", type=Path, help="Directory to write messy CSV copies")
    args = parser.parse_args()

    summary = make_messy(args.source_dir, args.output_dir)
    for table_name, counts in sorted(summary.items()):
        print(f"{table_name}: {counts}")


if __name__ == "__main__":
    main()
