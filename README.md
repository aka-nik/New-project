# SentinelETL

SentinelETL is a local data engineering project built around the public Olist Brazilian e-commerce dataset.

## Current step

The project profiles the original CSV source files, writes raw CSV data to partitioned
bronze Parquet with idempotent reruns, and applies deterministic quality checks with
optional row-level quarantine files.

## Run the profiler

From `D:\New Project`:

```powershell
.\.venv\Scripts\python.exe .\scripts\profile_source.py .\data\source
```

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Relationship checks:

```powershell
.\.venv\Scripts\python.exe .\scripts\check_relationships.py .\data\source
```

Run the quality scan across all nine source tables and write a structured report:

```powershell
.\.venv\Scripts\python.exe .\scripts\check_quality.py .\data\source --output .\quality-report.json
```

The report uses composite keys for order items and payments, and treats the
geolocation reference data as keyless because its source contract declares no
unique row identity. It also validates the expected columns and configured
foreign-key relationships, reporting orphan counts in both console and JSON output.

The quality library can write failed rows to a quarantine CSV while preserving the
original source files. Bronze manifests include a source checksum, so rerunning the
same source for the same ingest date reuses the existing output. Quality reports also
include deterministic schema fingerprints and can fail a run when expected columns
are missing or unexpected columns appear. Directory-level checks can also validate
configured foreign-key relationships and fail the child table when orphan rows exist.

## Important folders

- `data/raw/`: original downloaded archive
- `data/source/`: extracted source CSV files
- `src/sentinel/`: application package
- `scripts/`: command-line utilities
- `tests/`: automated tests
- `docs/`: decisions and data notes

The project vocabulary is maintained in [docs/glossary.md](docs/glossary.md).
The first source rules are maintained in [docs/data_contract.md](docs/data_contract.md).
