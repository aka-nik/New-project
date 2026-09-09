import json
from pathlib import Path

import pandas as pd

from sentinel.bronze import ingest_csv_to_bronze


def test_ingest_csv_to_bronze_writes_partitioned_parquet_and_manifest(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    source_path = source_dir / "orders.csv"
    df = pd.DataFrame(
        [
            {"order_id": "ord-001", "customer_id": "cus-001", "order_status": "delivered"},
            {"order_id": "ord-002", "customer_id": "cus-002", "order_status": "shipped"},
        ]
    )
    df.to_csv(source_path, index=False)

    bronze_dir = tmp_path / "bronze"
    manifest = ingest_csv_to_bronze(source_path, bronze_dir, ingest_date="2024-01-15")
    second_manifest = ingest_csv_to_bronze(
        source_path, bronze_dir, ingest_date="2024-01-15"
    )

    expected_path = bronze_dir / "orders" / "ingest_date=2024-01-15" / "part-000.parquet"
    assert expected_path.exists()
    assert manifest["row_count"] == 2
    assert manifest["source_file"] == "orders.csv"
    assert second_manifest == manifest
    assert manifest["source_sha256"]

    output_df = pd.read_parquet(expected_path)
    assert len(output_df) == 2

    manifest_path = bronze_dir / "orders" / "ingest_date=2024-01-15" / "_manifest.json"
    assert manifest_path.exists()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert payload["row_count"] == 2
    assert payload["schema"]["columns"] == ["order_id", "customer_id", "order_status"]
