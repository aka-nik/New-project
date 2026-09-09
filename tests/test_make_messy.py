import csv

from scripts.make_messy import make_messy


def test_make_messy_injects_expected_defects(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    orders = [
        ["order_id", "customer_id", "order_status", "order_purchase_timestamp"],
        ["ord-001", "cus-001", "delivered", "2018-01-01 10:00:00"],
        ["ord-002", "cus-002", "shipped", "2018-01-02 11:30:00"],
        ["ord-003", "cus-003", "approved", "2018-01-03 12:45:00"],
        ["ord-004", "cus-004", "created", "2018-01-04 13:00:00"],
    ]
    products = [
        ["product_id", "product_category_name"],
        ["prd-001", "electronics"],
        ["prd-002", "Electronics"],
        ["prd-003", "ELECTRONIC"],
        ["prd-004", "mobile"],
    ]

    with (source_dir / "olist_orders_dataset.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(orders)

    with (source_dir / "olist_products_dataset.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(products)

    output_dir = tmp_path / "messy"
    summary = make_messy(source_dir, output_dir)

    assert summary["olist_orders_dataset.csv"]["duplicate_rows"] >= 1
    assert summary["olist_orders_dataset.csv"]["missing_values"] >= 1
    assert summary["olist_products_dataset.csv"]["category_variants"] >= 2

    with (output_dir / "olist_orders_dataset.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert any(row["customer_id"].strip() != row["customer_id"] for row in rows)
    assert any(row["order_id"] == "ord-001" for row in rows) and sum(1 for row in rows if row["order_id"] == "ord-001") > 1

    with (output_dir / "olist_products_dataset.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        product_rows = list(csv.DictReader(handle))

    values = {row["product_category_name"] for row in product_rows}
    assert values & {"Electronics", "electronics", "ELECTRONIC", "Elec.", "Consumer Electronics"}
