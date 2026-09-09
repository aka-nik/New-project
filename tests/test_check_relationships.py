import csv

from scripts.check_relationships import count_orphans, read_column


def test_relationship_helpers_find_orphans(tmp_path):
    parent_file = tmp_path / "orders.csv"
    child_file = tmp_path / "items.csv"

    with parent_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id"])
        writer.writerow(["order-1"])

    with child_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id"])
        writer.writerow(["order-1"])
        writer.writerow(["missing-order"])

    valid_keys = read_column(parent_file, "order_id")

    assert valid_keys == {"order-1"}
    assert count_orphans(child_file, "order_id", valid_keys) == 1
