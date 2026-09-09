import csv

from sentinel.quality import evaluate_csv, schema_fingerprint


def test_evaluate_csv_reports_duplicates_and_missing_values(tmp_path):
    path = tmp_path / "orders.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id", "customer_id", "status"])
        writer.writerow(["ord-001", "cus-001", "delivered"])
        writer.writerow(["ord-001", "", "shipped"])
        writer.writerow(["ord-002", "cus-002", ""])

    report = evaluate_csv(path, "order_id")

    assert report["row_count"] == 3
    assert report["duplicate_count"] == 1
    assert report["missing_values"] == {"customer_id": 1, "status": 1}
    assert report["status"] == "fail"


def test_evaluate_csv_writes_quarantine_rows_with_flags(tmp_path):
    path = tmp_path / "orders.csv"
    quarantine_path = tmp_path / "quarantine" / "orders.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["order_id", "customer_id", "status"])
        writer.writerow(["ord-001", "cus-001", "delivered"])
        writer.writerow(["ord-001", "", "shipped"])

    report = evaluate_csv(path, "order_id", quarantine_path)

    assert report["quarantined_count"] == 2
    rows = list(csv.DictReader(quarantine_path.open(encoding="utf-8", newline="")))
    assert len(rows) == 2
    assert all("duplicate_key" in row["_dq_flags"] for row in rows)
    assert "missing_values:customer_id" in rows[1]["_dq_flags"]


def test_evaluate_csv_detects_schema_drift(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text(
        "order_id,customer_id,status\nord-001,cus-001,delivered\n",
        encoding="utf-8",
    )

    report = evaluate_csv(
        path,
        "order_id",
        expected_columns=["order_id", "customer_id", "order_status"],
    )

    assert report["schema_drift"] is True
    assert report["missing_columns"] == ["order_status"]
    assert report["unexpected_columns"] == ["status"]
    assert report["status"] == "fail"
    assert report["schema_fingerprint"] == schema_fingerprint(
        ["order_id", "customer_id", "status"]
    )
