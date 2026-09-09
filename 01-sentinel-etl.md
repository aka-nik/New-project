# Project 1 — SentinelETL: Orchestrated ETL Pipeline with LLM-Powered Data Quality Auditing

**Owner:** Nikhil Akash
**Target roles:** Data Engineer, Analytics Engineer, AI/ML Data Engineer
**Estimated effort:** 45–60 hours (3–4 weeks part-time)

---

## 1. Clarification questions (answer before building)

These gate the scope. An agent should ask a human these before writing code.

**Domain & data**
1. Which dataset will be the source of truth? (Recommended: reuse the Amazon/e-commerce sales data from the internship so the domain is already understood. Alternatives: Kaggle Brazilian E-Commerce (Olist), NYC TLC trips, or Instacart.)
2. Should the pipeline handle **multiple heterogeneous sources** (CSV + Excel + a REST API + a raw JSON dump), or is a single-format multi-file source acceptable? *(Recommendation: at least 3 formats — this is the differentiator vs. an analyst project.)*
3. What is the expected data volume? Under 1 GB (laptop-friendly) or must it demonstrate handling 10 GB+ (requires chunking/partitioning strategy)?
4. Is the data static (batch backfill) or should the pipeline simulate **daily incremental arrival**? *(Recommendation: simulate incremental — it forces idempotency and watermarking, which interviewers probe.)*

**Infrastructure & cost**
5. Cloud or fully local? Options: (a) 100% local via Docker Compose, (b) free-tier cloud (Neon/Supabase Postgres + GitHub Actions + Motherduck), (c) paid AWS/GCP.
6. Is there a budget for LLM API calls? Roughly $5–15 is enough for the full build. If zero budget, is a local model via Ollama (Llama 3.1 8B / Qwen 2.5) acceptable?
7. Which orchestrator — **Airflow** (most recognised on JDs, heavier) or **Prefect/Dagster** (lighter, faster to demo)? *(Recommendation: Airflow via `astro dev` or Docker Compose, because JD keyword matching favours it.)*

**Scope boundaries**
8. Should the LLM only *detect and report* quality issues, or also *auto-remediate* (write corrected values back)? *(Recommendation: detect + propose, with a human-approval gate. Auto-writing LLM output into a warehouse is a red flag in interviews unless gated.)*
9. Is a BI layer required at the end (Power BI dashboard on the curated tables), or does the project stop at the warehouse?
10. Should this be deployed and publicly reachable, or is a GitHub repo + README + demo video sufficient? *(Recommendation: repo + 3-minute Loom demo. Deployment cost rarely pays off for this project type.)*

---

## 2. Objective

Build a production-shaped batch data pipeline that ingests messy multi-source commerce data, lands it in a warehouse through bronze/silver/gold layers, and uses an LLM as an **automated data quality auditor** that produces human-readable data quality reports and proposes remediation rules — with deterministic checks doing the heavy lifting and the LLM handling the parts that are genuinely hard to hard-code (semantic anomalies, free-text category normalisation, root-cause narration).

**The core thesis to communicate:** the LLM is not decorative. It solves a class of problem deterministic rules cannot — reconciling inconsistent categorical vocabularies across sources and explaining *why* a metric broke.

---

## 3. Scope

**In scope**
- Multi-format ingestion (CSV, Excel, JSON, one REST API)
- Medallion architecture: bronze (raw, immutable) → silver (cleaned, typed, deduplicated) → gold (dimensional model, business-ready)
- Airflow DAG with dependencies, retries, sensors, and SLA
- Deterministic data quality suite (Great Expectations or Soda Core)
- LLM quality auditor with structured output and a human approval gate
- dbt for silver→gold transformations
- Data quality metrics stored as a time series so quality trend is itself queryable
- Containerised local deployment
- CI: lint, unit tests, dbt build against a test schema

**Out of scope**
- Real-time streaming (that is Project 2)
- Multi-tenancy, RBAC, cost optimisation
- Production monitoring stack (Prometheus/Grafana) — a simple metrics table is enough

---

## 4. Technology stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11 | Resume match |
| Orchestration | Apache Airflow 2.9 (Docker Compose) | Highest JD keyword frequency for DE |
| Warehouse | PostgreSQL 16 (local Docker) or Neon free tier | Resume match (PostgreSQL listed) |
| Transformation | dbt-core + dbt-postgres | Analytics-engineering credibility |
| Data quality | Great Expectations 0.18 or Soda Core | Deterministic baseline |
| LLM | Anthropic Claude API (or OpenAI, or Ollama local) | Structured-output auditing |
| Storage abstraction | MinIO (S3-compatible) for the bronze layer | Demonstrates object-store landing zone |
| BI | Power BI Desktop connected to gold schema | Resume match |
| Packaging | Docker Compose, `uv` or Poetry | Reproducibility |
| CI | GitHub Actions | Engineering hygiene |

---

## 5. Architecture

```
                 ┌──────────────────────────────────────────┐
   CSV / XLSX ──▶│  Ingestion tasks (Python operators)       │
   JSON dump  ──▶│  - schema capture                        │
   REST API   ──▶│  - checksum + row count                  │
                 └───────────────────┬──────────────────────┘
                                     ▼
                        MinIO bronze/  (raw, partitioned by ingest_date)
                                     │
                                     ▼
                 ┌──────────────────────────────────────────┐
                 │  Deterministic DQ gate (Great Expectations)│
                 │  schema, nullability, ranges, uniqueness  │
                 └───────────────┬──────────────┬───────────┘
                          pass   │              │  fail/warn
                                 ▼              ▼
                     Postgres silver.*    ┌──────────────────────┐
                                 │        │ LLM Quality Auditor  │
                                 │        │ - anomaly narration  │
                                 │        │ - category mapping   │
                                 │        │ - remediation rules  │
                                 │        └──────────┬───────────┘
                                 │                   ▼
                                 │        dq.audit_findings (JSONB)
                                 │        dq.proposed_mappings
                                 │                   │
                                 │        human approval task ◀──┘
                                 ▼                   │
                     dbt run (silver → gold) ◀───────┘
                                 ▼
                     Postgres gold.* (star schema)
                                 ▼
                     Power BI + dq_trend dashboard
```

---

## 6. Repository structure

```
sentinel-etl/
├── README.md
├── docker-compose.yml
├── .env.example
├── Makefile
├── dags/
│   ├── ingest_sales_daily.py
│   ├── dq_audit.py
│   └── utils/
│       ├── connectors.py
│       ├── checksums.py
│       └── watermark.py
├── src/sentinel/
│   ├── ingestion/
│   │   ├── csv_reader.py
│   │   ├── excel_reader.py
│   │   ├── json_reader.py
│   │   └── api_client.py
│   ├── quality/
│   │   ├── expectations/          # GE suites as JSON
│   │   ├── deterministic.py
│   │   ├── llm_auditor.py
│   │   ├── prompts/
│   │   │   ├── anomaly_narration.md
│   │   │   ├── category_normalisation.md
│   │   │   └── remediation_rules.md
│   │   └── schemas.py             # Pydantic models for LLM output
│   └── warehouse/
│       └── loaders.py
├── dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   │       ├── fct_orders.sql
│   │       ├── dim_customer.sql
│   │       ├── dim_product.sql
│   │       └── dim_date.sql
│   └── tests/
├── tests/
│   ├── test_ingestion.py
│   ├── test_llm_auditor.py        # with mocked LLM responses
│   └── test_transformations.py
├── notebooks/
│   └── exploration.ipynb
├── powerbi/
│   └── sentinel_dashboard.pbix
└── .github/workflows/ci.yml
```

---

## 7. Data model

### Bronze (MinIO, Parquet)
Path convention: `bronze/{source_name}/ingest_date={YYYY-MM-DD}/part-{n}.parquet`
Every file accompanied by a `_manifest.json`: source, row_count, sha256, schema fingerprint, ingested_at.

### Silver (Postgres schema `silver`)
```sql
CREATE TABLE silver.orders (
    order_id            TEXT PRIMARY KEY,
    customer_id         TEXT NOT NULL,
    product_id          TEXT NOT NULL,
    order_ts            TIMESTAMPTZ NOT NULL,
    quantity            INTEGER NOT NULL CHECK (quantity > 0),
    unit_price          NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    discount_pct        NUMERIC(5,4) DEFAULT 0,
    currency            CHAR(3) NOT NULL,
    region              TEXT,
    category_raw        TEXT,          -- as received
    category_canonical  TEXT,          -- LLM-normalised, approved
    source_system       TEXT NOT NULL,
    ingest_date         DATE NOT NULL,
    _dq_flags           JSONB DEFAULT '[]'::jsonb,
    _loaded_at          TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON silver.orders (order_ts);
CREATE INDEX ON silver.orders (ingest_date);
```

### Data quality schema (`dq`)
```sql
CREATE TABLE dq.run_metrics (
    run_id           UUID PRIMARY KEY,
    dag_run_id       TEXT,
    table_name       TEXT,
    ingest_date      DATE,
    rows_in          BIGINT,
    rows_rejected    BIGINT,
    null_rate        NUMERIC(6,5),
    dup_rate         NUMERIC(6,5),
    schema_drift     BOOLEAN,
    ge_success_pct   NUMERIC(5,2),
    created_at       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE dq.audit_findings (
    finding_id       UUID PRIMARY KEY,
    run_id           UUID REFERENCES dq.run_metrics(run_id),
    severity         TEXT CHECK (severity IN ('critical','high','medium','low')),
    category         TEXT,
    affected_column  TEXT,
    affected_rows    BIGINT,
    description      TEXT,
    suggested_action TEXT,
    llm_model        TEXT,
    llm_confidence   NUMERIC(3,2),
    created_at       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE dq.proposed_mappings (
    mapping_id       UUID PRIMARY KEY,
    run_id           UUID,
    column_name      TEXT,
    raw_value        TEXT,
    proposed_value   TEXT,
    confidence       NUMERIC(3,2),
    status           TEXT DEFAULT 'pending'
                     CHECK (status IN ('pending','approved','rejected')),
    reviewed_by      TEXT,
    reviewed_at      TIMESTAMPTZ
);
```

### Gold (schema `gold`)
Star schema: `fct_orders`, `dim_customer` (SCD Type 2), `dim_product`, `dim_date`, `dim_region`.
Build `dim_customer` as SCD2 with `valid_from` / `valid_to` / `is_current` — SCD2 is a very common DE interview question and having built one is worth stating.

---

## 8. Phased implementation

### Phase 0 — Foundation (4–6 h)
1. `docker-compose.yml` with services: `postgres`, `minio`, `airflow-webserver`, `airflow-scheduler`, `airflow-init`.
2. Dependency management with `uv` / Poetry; pin versions.
3. `.env.example` with every required variable, no secrets committed.
4. `Makefile` targets: `make up`, `make down`, `make seed`, `make test`, `make dbt`.
5. Create schemas `bronze_meta`, `silver`, `gold`, `dq` via an init SQL script.

**Acceptance:** `make up` brings the stack to healthy; Airflow UI reachable at `localhost:8080`; Postgres has all four schemas.

### Phase 1 — Source data preparation (4–6 h)
1. Take the chosen clean dataset and write `scripts/make_messy.py` that deliberately injects realistic defects into a copy:
   - 2–4% nulls in non-critical columns, 0.3% in critical ones
   - duplicate order_ids (~1%)
   - inconsistent category spellings: `Electronics`, `electronics`, `ELECTRONIC`, `Elec.`, `Consumer Electronics`
   - mixed date formats across sources: ISO, `DD/MM/YYYY`, epoch millis
   - currency inconsistency: some rows in INR, some in USD, currency column occasionally missing
   - 0.1% negative quantities and impossible prices
   - one column silently renamed midway through the date range (schema drift)
   - trailing whitespace and non-breaking spaces in IDs
2. Split output across formats: CSV, XLSX (multi-sheet), JSON lines.
3. Stand up a tiny FastAPI service that serves one slice of the data as a paginated REST endpoint, so the pipeline exercises an API connector with pagination and retry.

**Acceptance:** a documented defect manifest exists (`docs/injected_defects.md`) listing every defect and its expected detection method — this is the ground truth used to prove the pipeline works.

### Phase 2 — Ingestion to bronze (6–8 h)
1. Implement each reader with a common interface returning `(DataFrame, IngestionManifest)`.
2. Handle: encoding detection, multi-sheet Excel, JSONL streaming for large files, API pagination with exponential backoff.
3. Write Parquet to MinIO partitioned by `ingest_date`; never mutate bronze.
4. Implement watermarking: a `bronze_meta.watermarks` table tracking last successfully ingested date per source, so reruns are idempotent.
5. Airflow DAG `ingest_sales_daily` with one task group per source, `max_active_runs=1`, retries=2 with exponential backoff.

**Acceptance:** running the DAG twice for the same logical date produces no duplicate bronze objects and no duplicate silver rows. Demonstrate this in the README with before/after row counts.

### Phase 3 — Deterministic quality gate (6–8 h)
1. Define Great Expectations suites per source: expected columns, types, non-null on keys, uniqueness on `order_id`, value ranges, referential integrity to product/customer sets, freshness.
2. Implement schema-drift detection by comparing the current schema fingerprint to the previous run's.
3. Route rows: clean rows → silver; failing rows → `silver.orders_quarantine` with the failing expectation attached in `_dq_flags`.
4. Write results into `dq.run_metrics`.
5. Airflow branch: if `ge_success_pct < threshold` (make it configurable, e.g. 90), skip the gold build and raise an alert task.

**Acceptance:** every defect in `docs/injected_defects.md` that is deterministically detectable is caught, with the detection rate reported in the README as a table.

### Phase 4 — LLM quality auditor (10–14 h) ← the differentiator

**Component A: Category normalisation**
- Input: distinct `category_raw` values with frequency counts (send the value list, never raw customer rows).
- Prompt the LLM to cluster variants to a canonical taxonomy and return strict JSON.
- Enforce output with Pydantic:
```python
class CategoryMapping(BaseModel):
    raw_value: str
    canonical_value: str
    confidence: float = Field(ge=0, le=1)
    reasoning: str

class CategoryMappingBatch(BaseModel):
    mappings: list[CategoryMapping]
    new_canonical_values: list[str]
```
- Write to `dq.proposed_mappings` with `status='pending'`.
- Auto-approve above a confidence threshold **only if** the canonical value already exists in the approved taxonomy; everything else waits for human approval.

**Component B: Anomaly narration**
- Input: aggregated metrics only (daily revenue, order counts, AOV, null rates, per-region splits) for the last N days — never row-level PII.
- Ask the LLM to identify which movements are statistically notable, propose plausible root causes, and rank by severity.
- Pair it with a deterministic baseline (z-score or STL decomposition) so the LLM narrates detections rather than inventing them. **This is important:** the LLM interprets, the statistics detect. State this design decision explicitly in the README — it shows judgement.

**Component C: Remediation rule generation**
- Given a recurring finding, ask the LLM to emit a candidate Great Expectations expectation or SQL constraint that would catch it in future.
- Never execute generated SQL directly. Write it to `docs/proposed_expectations/` for human review. Say so in the README.

**Engineering requirements for this phase**
- Cache LLM responses keyed by an input hash so reruns cost nothing.
- Retry with backoff on rate limits; fall back to deterministic-only mode if the LLM is unavailable, and mark the run degraded rather than failing it.
- Log token counts and estimated cost per run into `dq.run_metrics`.
- Redact/aggregate before sending: assert in code that no column in the outbound payload is on a `SENSITIVE_COLUMNS` denylist.
- Unit tests mock the LLM client entirely — CI must never make a network call.

**Acceptance:** an `evals/` folder containing 30–50 hand-labelled category variants with expected canonical mappings, plus a script reporting precision/recall of the LLM normaliser. Report the number in the README. *A measured eval number is what separates this from a toy.*

### Phase 5 — dbt transformations to gold (6–8 h)
1. Staging models: one per source, light renaming and typing only.
2. Intermediate models: dedup logic, currency normalisation to a single reporting currency, applied category mapping join.
3. Marts: `fct_orders`, `dim_customer` (SCD2 via dbt snapshots), `dim_product`, `dim_date`.
4. dbt tests: `unique`, `not_null`, `relationships`, `accepted_values`, plus 2–3 custom singular tests (e.g. revenue reconciliation between silver and gold within a tolerance).
5. Generate and commit dbt docs; screenshot the lineage graph into the README.

**Acceptance:** `dbt build` passes all tests; lineage graph renders.

### Phase 6 — BI and reporting (4–5 h)
1. Power BI report with two pages: **Business** (revenue, AOV, category mix, region trend) and **Data Quality** (quality score trend from `dq.run_metrics`, open findings by severity, mapping approval queue).
2. The DQ page is the interesting one — it makes data quality a first-class product surface.
3. Export screenshots to `docs/screenshots/`.

### Phase 7 — Hardening and presentation (5–6 h)
1. GitHub Actions: ruff/black, mypy, pytest, `dbt parse`, and a `dbt build` against a throwaway Postgres service container.
2. README with architecture diagram, the defect-detection table, the LLM eval numbers, cost per run, and setup instructions verified from a clean clone.
3. 3-minute demo video: trigger the DAG, show a failure being caught, show the LLM finding, approve a mapping, show gold rebuild.
4. `docs/DECISIONS.md` — 5–8 architecture decision records. Interviewers love these.

---

## 9. Testing strategy

| Level | What | Tool |
|---|---|---|
| Unit | readers, watermark logic, currency conversion, Pydantic parsing | pytest |
| Contract | LLM output schema conformance against fixtures | pytest + Pydantic |
| Data | expectations, dbt tests | GE, dbt |
| Integration | full DAG on a small fixture dataset | pytest + Airflow `dag.test()` |
| Eval | LLM normaliser precision/recall | custom script |
| Idempotency | double-run produces identical row counts | integration test |

---

## 10. Definition of done

- [ ] `git clone` → `make up` → `make seed` → DAG green, on a machine that has never run it
- [ ] Every injected defect either detected or explicitly documented as out of scope
- [ ] LLM normaliser eval ≥ 0.90 precision on the labelled set
- [ ] `dbt build` fully green with docs generated
- [ ] Pipeline is idempotent, proven by test
- [ ] CI green on `main`
- [ ] README readable in under 5 minutes with a diagram and screenshots
- [ ] Demo video recorded

---

## 11. Resume bullets (use only once actually built)

- Built an Airflow-orchestrated ETL pipeline ingesting multi-format sources (CSV, Excel, JSON, REST API) into a medallion architecture on PostgreSQL and S3-compatible object storage, with watermark-based incremental loads and proven idempotent reruns.
- Designed a two-tier data quality system pairing deterministic Great Expectations suites with an LLM auditor that normalises inconsistent categorical vocabularies and narrates metric anomalies, achieving [X]% precision on a hand-labelled evaluation set.
- Modelled a gold-layer star schema in dbt including SCD Type 2 customer dimension, with 40+ automated data tests and generated lineage documentation.
- Surfaced pipeline health as a product: Power BI data quality dashboard tracking quality score trend, open findings by severity, and a human-in-the-loop approval queue for LLM-proposed remediations.
