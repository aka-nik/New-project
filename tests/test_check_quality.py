import csv

from scripts.check_quality import build_quality_report, check_csv


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
        "order_id,order_status\norder-1,delivered\n", encoding="utf-8"
    )

    reports = build_quality_report(tmp_path)

    assert len(reports) == 9
    assert reports["orders"]["status"] == "pass"
    assert reports["payments"]["status"] == "missing"
    assert reports["geolocation"]["duplicate_count"] == 0
