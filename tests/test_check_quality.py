import csv

from scripts.check_quality import (
    build_quality_report,
    check_csv,
    summarize_quality_report,
)


def test_check_csv_counts_duplicate_keys_and_missing_values(tmp_path):
    source_file = tmp_path / "orders.csv"
    with source_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id", "status"])
        writer.writerow(["order-1", "delivered"])
        writer.writerow(["order-1", ""])

    row_count, duplicate_count, missing = check_csv(source_file, "order_id")

    assert row_count == 2
    assert duplicate_count == 1
    assert missing == {"order_id": 0, "status": 1}


def test_build_quality_report_covers_all_source_tables(tmp_path):
    source_file = tmp_path / "olist_orders_dataset.csv"
    source_file.write_text(
        "order_id,customer_id,order_status,order_purchase_timestamp,"
        "order_approved_at,order_delivered_carrier_date,"
        "order_delivered_customer_date,order_estimated_delivery_date\n"
        "order-1,customer-1,delivered,2018-01-01,2018-01-01,"
        "2018-01-02,2018-01-03,2018-01-05\n",
        encoding="utf-8",
    )

    reports = build_quality_report(tmp_path)

    assert len(reports) == 9
    assert reports["orders"]["status"] == "pass"
    assert reports["payments"]["status"] == "missing"
    assert reports["geolocation"]["duplicate_count"] == 0


def test_summarize_quality_report_excludes_missing_tables_from_pass_rate():
    reports = {
        "orders": {"status": "pass"},
        "products": {"status": "fail"},
        "payments": {"status": "missing"},
    }

    assert summarize_quality_report(reports) == {
        "total_tables": 3,
        "evaluated_tables": 2,
        "passed_tables": 1,
        "failed_tables": 1,
        "missing_tables": 1,
        "pass_rate_pct": 50.0,
    }
