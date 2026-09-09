from pathlib import Path

from sentinel.quality import evaluate_directory


def test_evaluate_directory_reports_each_table_status(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    orders = [
        ["order_id", "customer_id", "status"],
        ["ord-001", "cus-001", "delivered"],
        ["ord-001", "", "shipped"],
    ]
    customers = [
        ["customer_id", "city"],
        ["cus-001", "sao paulo"],
        ["cus-002", "rio"],
    ]

    orders_path = source_dir / "olist_orders_dataset.csv"
    customers_path = source_dir / "olist_customers_dataset.csv"

    orders_path.write_text("\n".join(",".join(row) for row in orders), encoding="utf-8")
    customers_path.write_text("\n".join(",".join(row) for row in customers), encoding="utf-8")

    reports = evaluate_directory(
        source_dir,
        {
            "orders": ("olist_orders_dataset.csv", "order_id"),
            "customers": ("olist_customers_dataset.csv", "customer_id"),
        },
        quarantine_dir=tmp_path / "quarantine",
    )

    assert reports["orders"]["duplicate_count"] == 1
    assert reports["orders"]["status"] == "fail"
    assert reports["orders"]["quarantined_count"] == 2
    assert (tmp_path / "quarantine" / "orders.csv").exists()
    assert reports["customers"]["status"] == "pass"


def test_evaluate_directory_fails_child_table_with_orphans(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    (source_dir / "orders.csv").write_text(
        "order_id\nord-001\n", encoding="utf-8"
    )
    (source_dir / "items.csv").write_text(
        "order_id\nord-001\nmissing-order\n", encoding="utf-8"
    )

    reports = evaluate_directory(
        source_dir,
        {
            "orders": ("orders.csv", "order_id"),
            "items": ("items.csv", "order_id"),
        },
        relationships=[("items.csv", "order_id", "orders.csv", "order_id")],
    )

    relationship = "items.csv:order_id -> orders.csv:order_id"
    assert reports["items"]["relationship_orphans"][relationship] == 1
    assert reports["items"]["status"] == "fail"
