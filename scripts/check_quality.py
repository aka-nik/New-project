"""Run deterministic quality checks against the source CSV tables."""

import argparse
import csv
import json
from pathlib import Path

from sentinel.quality import KeyColumns, evaluate_directory


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

EXPECTED_COLUMNS = {
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "payments": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
    "sellers": [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ],
    "geolocation": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ],
    "category_translation": [
        "product_category_name",
        "product_category_name_english",
    ],
}

RELATIONSHIPS = [
    ("olist_orders_dataset.csv", "customer_id", "olist_customers_dataset.csv", "customer_id"),
    ("olist_order_items_dataset.csv", "order_id", "olist_orders_dataset.csv", "order_id"),
    ("olist_order_items_dataset.csv", "product_id", "olist_products_dataset.csv", "product_id"),
    ("olist_order_items_dataset.csv", "seller_id", "olist_sellers_dataset.csv", "seller_id"),
    ("olist_order_reviews_dataset.csv", "order_id", "olist_orders_dataset.csv", "order_id"),
    ("olist_order_payments_dataset.csv", "order_id", "olist_orders_dataset.csv", "order_id"),
]

CATEGORICAL_COLUMNS = {
    "products": ["product_category_name"],
    "category_translation": ["product_category_name"],
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

    duplicate_count = row_count - len(set(keys)) if key_columns else 0
    return row_count, duplicate_count, missing


def build_quality_report(source_dir: Path) -> dict[str, dict[str, object]]:
    """Evaluate every configured source table, including missing-file statuses."""
    return evaluate_directory(
        source_dir,
        TABLES,
        expected_columns=EXPECTED_COLUMNS,
        relationships=RELATIONSHIPS,
        categorical_columns=CATEGORICAL_COLUMNS,
    )


def summarize_quality_report(
    reports: dict[str, dict[str, object]],
) -> dict[str, int | float]:
    """Summarize table statuses as a deterministic run-level quality score."""
    total_tables = len(reports)
    passed_tables = sum(report.get("status") == "pass" for report in reports.values())
    failed_tables = sum(report.get("status") == "fail" for report in reports.values())
    missing_tables = sum(
        report.get("status") == "missing" for report in reports.values()
    )
    evaluated_tables = total_tables - missing_tables
    pass_rate = (
        round(passed_tables / evaluated_tables * 100, 2)
        if evaluated_tables
        else 0.0
    )
    return {
        "total_tables": total_tables,
        "evaluated_tables": evaluated_tables,
        "passed_tables": passed_tables,
        "failed_tables": failed_tables,
        "missing_tables": missing_tables,
        "pass_rate_pct": pass_rate,
    }


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
    summary = summarize_quality_report(reports)
    print(
        "quality summary: "
        f"{summary['passed_tables']}/{summary['evaluated_tables']} passed "
        f"({summary['pass_rate_pct']:.2f}%), "
        f"{summary['failed_tables']} failed, "
        f"{summary['missing_tables']} missing"
    )
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
        whitespace_summary = ", ".join(
            f"{column}={count:,}"
            for column, count in report.get("whitespace_values", {}).items()
            if count
        ) or "none"
        print(f"  key whitespace: {whitespace_summary}")
        for column, variants in report.get("category_variants", {}).items():
            if variants:
                print(f"  category variants in {column}: {len(variants):,} groups")
        for relationship, orphan_count in report.get("relationship_orphans", {}).items():
            print(f"  {relationship}: {orphan_count:,} orphan rows")

    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        payload = {"summary": summary, "tables": reports}
        arguments.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
