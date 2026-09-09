import csv

from scripts.check_quality import check_csv


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
