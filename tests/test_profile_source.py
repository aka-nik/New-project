import csv

from scripts.profile_source import profile_csv


def test_profile_csv_returns_rows_and_columns(tmp_path):
    source_file = tmp_path / "orders.csv"
    with source_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id", "status"])
        writer.writerow(["order-1", "delivered"])
        writer.writerow(["order-2", "shipped"])

    row_count, columns = profile_csv(source_file)

    assert row_count == 2
    assert columns == ["order_id", "status"]
