# Skills Inventory & Learning Roadmap
### For the five-project portfolio (SentinelETL, StreamScribe, QueryMind, DocuFlow, LineageLens)

---

## How to use this document

Do not read this front to back and then start building. Learning-then-building wastes most of what you watch, because you have no context to hang it on.

The correct loop is: **watch the minimum needed to start → build until you hit a wall → go back for the specific thing that blocked you.** The roadmap below is sequenced so each block of learning immediately unblocks a phase of a project. Anything marked *just-in-time* should not be studied in advance at all.

A note on the links: these were found by searching rather than recalled, so they were live at the time of writing. YouTube content moves and channels reorganise. If a link is dead, the channel name and search term are given alongside so you can find the replacement. Where I could not verify a single strong video for a topic, I have said so explicitly and given search terms instead of guessing at a URL.

---

# PART 1 — THE SKILLS INVENTORY

## 1.1 What you already have

From the resume, these are real and can be built on rather than learned from scratch:

| Skill | Current level | Where it gets used |
|---|---|---|
| SQL (querying) | Working | Every project |
| Python | Working | Every project |
| PostgreSQL | Working | Projects 1, 2, 3, 4, 5 |
| Power BI / DAX | Working | Projects 1, 4 |
| Excel | Working | Project 1 (source data) |
| Data cleaning / wrangling | Working | Projects 1, 4 |
| HTML/CSS/JavaScript | Working | Project 3 frontend |
| Basic ML concepts | Exposure only | Project 3 (stretch), Project 4 |

**Honest read:** the gap is not analysis. It is everything around the analysis — version control discipline, containers, orchestration, testing, deployment, and the software-engineering habits that separate a script from a system. That is the bulk of what follows.

---

## 1.2 The full skill list, grouped

### Group A — Engineering foundations (needed before anything else)
These are not optional and they are not glamorous. Every project assumes them.

1. **Git and GitHub properly** — branches, meaningful commits, PRs, `.gitignore`, never committing secrets
2. **Command line / Bash** — navigation, pipes, environment variables, process management
3. **Python packaging & environments** — `uv` or Poetry, `pyproject.toml`, pinned dependencies, editable installs
4. **Python beyond scripting** — modules and packages, type hints, dataclasses, context managers, exceptions, logging (not `print`)
5. **Testing with pytest** — fixtures, parametrisation, mocking, test structure
6. **Docker & Docker Compose** — images vs containers, volumes, networks, healthchecks, multi-service stacks
7. **Configuration & secrets** — `.env` files, environment-based config, never hardcoding credentials
8. **CI with GitHub Actions** — running lint and tests on push, service containers

### Group B — Core data engineering
9. **Advanced SQL** — window functions, CTEs (including recursive), `EXPLAIN ANALYZE`, indexing, query cost
10. **PostgreSQL administration basics** — roles and grants, schemas, transactions and isolation, `statement_timeout`, partitioning
11. **Dimensional modelling** — facts vs dimensions, grain, star vs snowflake, surrogate keys, conformed dimensions
12. **Slowly Changing Dimensions** — Type 1/2/3, and why Type 2 is asked about in every interview
13. **Medallion / layered architecture** — bronze, silver, gold, and why raw is immutable
14. **Idempotency & watermarking** — the single most important pipeline property; reruns must not duplicate
15. **Incremental loading** — high-water marks, late-arriving data, backfills
16. **File formats** — Parquet vs CSV, columnar storage, partitioning, compression
17. **Object storage** — S3/MinIO concepts, key design, why you land raw files before loading
18. **Orchestration with Airflow** — DAGs, operators, task groups, sensors, retries, backfill, XComs, and their limits
19. **dbt** — models, refs, sources, materialisations, snapshots, tests, macros, Jinja, docs and lineage
20. **Data quality engineering** — Great Expectations or Soda, expectations, quarantine patterns, schema drift detection
21. **Data contracts & schema evolution** — backward/forward compatibility, why it matters

### Group C — Streaming (Project 2 only)
22. **Streaming fundamentals** — log-based messaging, topics, partitions, offsets, consumer groups, rebalancing
23. **Kafka / Redpanda operationally** — producer acks, manual offset commit, consumer lag, DLQ patterns
24. **Serialisation & schema registry** — Avro, JSON Schema, compatibility modes
25. **Delivery semantics** — at-most-once, at-least-once, exactly-once, and idempotent sinks
26. **Windowing & watermarks** — tumbling, sliding, session windows; late data; event time vs processing time
27. **Time-series storage** — TimescaleDB hypertables, continuous aggregates, retention policies
28. **Statistical anomaly detection** — rolling z-score, EWMA, STL decomposition, seasonality, alert fatigue

### Group D — AI/ML and LLM engineering
29. **LLM API fundamentals** — messages, system prompts, temperature, tokens, context windows, cost model
30. **Prompt engineering that survives production** — versioning, few-shot, task decomposition, instruction specificity
31. **Structured output** — JSON mode, tool/function calling, Pydantic enforcement, `instructor`, retry-on-parse-failure
32. **Embeddings & vector search** — what an embedding is, cosine similarity, pgvector, indexing (HNSW/IVFFlat)
33. **RAG** — chunking, retrieval, hybrid search (BM25 + dense), reranking, and why naive RAG underperforms
34. **Evaluation harnesses** — golden datasets, execution accuracy vs exact match, precision/recall, LLM-as-judge and its limits
35. **Grounding & hallucination control** — numeric validation, citation to source, refusal behaviour
36. **Vision LLMs / document AI** — image inputs, OCR as grounding, bounding boxes, confidence calibration
37. **LLM cost & latency engineering** — caching by input hash, model routing, batching, token accounting
38. **Guardrails** — input validation, output validation, denylists, least-privilege execution
39. **Classical ML basics** — train/test split, precision/recall/F1, overfitting, class imbalance (enough to speak credibly)

### Group E — Application & tooling
40. **FastAPI** — routing, Pydantic request/response models, dependency injection, async, background tasks
41. **Async task queues** — Celery or RQ, workers, retries, dead-letter, idempotent tasks
42. **Redis** — as broker and as cache
43. **Streamlit** — fast internal UIs for review queues and demos
44. **SQL parsing** — sqlglot AST, `qualify`, dialect transpilation, lineage extraction
45. **Graph algorithms (light)** — networkx, DAGs, topological sort, cycle detection, traversal
46. **OCR & image preprocessing** — Tesseract/PaddleOCR, deskew, denoise, word confidence
47. **Observability** — structured logging, metrics tables, tracing LLM calls

### Group F — Professional practice
48. **Writing a README that gets read** — architecture diagram, results table, honest limitations
49. **Architecture Decision Records** — what you chose, what you rejected, why
50. **Demo recording** — 3 minutes, no dead air, show a failure being caught

---

# PART 2 — THE ROADMAP

Ten stages. Roughly 5–7 months at 10–12 hours per week. Stages 6 and 9 are optional depending on which projects you build.

---

## STAGE 0 — Set the foundation (2 weeks, ~20 h)
**Blocks:** everything. Do not skip.

### Git & GitHub
- **freeCodeCamp / Traversy** — search `git and github full course for beginners` on YouTube; any 1–2 hour course from a major channel works, the content is stable.
- Practice target: make a repo, branch, open a PR against yourself, merge it. That is the whole loop.

### Command line
- Search `linux command line for data engineers` or `bash crash course`. 1 hour is enough.

### Docker (the highest-leverage foundation skill)
- **TechWorld with Nana — Docker Tutorial for Beginners (playlist)**
  https://www.youtube.com/playlist?list=PLy7NrYWoggjzfAHlUusx2wuDwfCrmJYcs
  Widely regarded as the best free Docker material. ~3 hours.
- Channel: https://www.youtube.com/c/TechWorldwithNana
- Practice target: write a `docker-compose.yml` that runs Postgres + a Python container that connects to it. If you can do that from memory, you are ready.

### Python engineering habits
- Search `python type hints tutorial`, `pytest tutorial for beginners`, `python logging tutorial`. Short videos, one each.
- Practice target: take any old script, restructure it into a package with `pyproject.toml`, add three tests, replace every `print` with `logging`.

> **Checkpoint:** you can spin up a multi-container stack, connect to it from Python, and run tests against it. Do not proceed until this is true.

---

## STAGE 1 — SQL and modelling depth (2 weeks, ~20 h)
**Blocks:** Projects 1, 3, 5.

### Advanced SQL
- Written reference (excellent and free): **PostgreSQL Advanced** — https://neon.com/postgresql/postgresql-advanced
- Search on YouTube: `sql window functions explained`, `recursive cte sql tutorial`, `explain analyze postgres tutorial`.
- Practice target: rewrite three of your internship queries using window functions. Then run `EXPLAIN ANALYZE` on each and explain to yourself why the planner chose that path.

### Dimensional modelling
- **Data Modeling Tutorial: Star Schema (Kimball Approach)** — KahanDataSolutions
  https://www.youtube.com/watch?v=gRE3E7VUzRU
- **Microsoft Learn — Understand star schema** (concise, authoritative, and directly relevant given your Power BI background)
  https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- **Dimensional modelling guide (written, 2026)** — https://datadef.io/guides/en/dimensional-modeling
- Practice target: on paper, model the Amazon sales dataset from your internship as a star schema. Declare the grain of the fact table in one sentence. If you cannot state the grain, you have not modelled it.

### PostgreSQL operations
- Search `postgres roles and permissions tutorial` and `postgres transaction isolation explained`.
- Practice target: create a `readonly` role with SELECT-only grants and prove it cannot INSERT. You will need exactly this in Project 3.

> **Checkpoint:** you can design a star schema with SCD2 on paper and defend the grain choice.

---

## STAGE 2 — Orchestration & the modern stack (3 weeks, ~30 h)
**Blocks:** Project 1 (primary), Project 4 (partly).

### The single best free structured course
- **Data Engineering Zoomcamp (DataTalks.Club)** — free, 9 weeks, project-based, and the closest thing to a canonical DE curriculum.
  Repo: https://github.com/DataTalksClub/data-engineering-zoomcamp
  YouTube playlist: https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb
  Course page: https://datatalks.club/blog/data-engineering-zoomcamp.html
  **Do modules 1, 2, 4 and 5 at minimum.** You can self-pace outside a live cohort.

### Airflow
- **Airflow 3.0 Masterclass (2026)** — 4+ hours, builds a production pipeline
  https://www.youtube.com/watch?v=RFVqzMyOicc
- **Airflow Tutorial For Beginners / Full Course (2026)**
  https://www.youtube.com/watch?v=IiczxlbQb8s
- **Written, hands-on, excellent** — Start Data Engineering: https://www.startdataengineering.com/post/airflow-tutorial/
- **Sequenced free video roadmap** — https://developereducators.com/roadmap/airflow/
- Practice target: a DAG with three dependent tasks, retries, and a rerun that does not duplicate rows.

### dbt
- **DBT Course for Beginners to Advanced (June 2026)** — https://www.youtube.com/watch?v=ziyFbdHaoxc
- **dbt Ultimate Guide with CI/CD (5 hours)** — https://www.youtube.com/watch?v=B8uwFmVt4sU
- **Written walkthrough incl. SCD2 and lineage** — https://www.startdataengineering.com/post/dbt-data-build-tool-tutorial/
- **Official free courses** — https://www.getdbt.com/dbt-learn
- Practice target: staging → intermediate → mart, one snapshot for SCD2, ten tests, `dbt docs generate` producing a lineage graph.

### Data quality
- I did not find a single strong free video course on **Great Expectations** worth linking. The official docs are genuinely good and the tool changes fast enough that videos go stale. Search `great expectations tutorial 2026` and treat anything older than a year with suspicion — the API changed significantly.
- Concept to understand first, regardless of tool: what should happen to a *failing row*. Reject the batch, quarantine the row, or let it through flagged? That decision is the design.

> **Checkpoint:** you can build Project 1 through Phase 5. Start building it now — do not wait for Stage 3.

---

## STAGE 3 — Build Project 1 (4 weeks, ~45 h)
**Stop learning. Start building.** Follow `01-sentinel-etl.md` Phases 0–3 and 5–7.

Return to Stage 2 material only when blocked. Keep a running `docs/DECISIONS.md` from day one — writing it at the end never happens.

Skip Phase 4 (the LLM auditor) for now. Come back to it after Stage 4.

---

## STAGE 4 — LLM engineering (3 weeks, ~30 h)
**Blocks:** Projects 1 (Phase 4), 3, 4.

### The structured course
- **LLM Zoomcamp (DataTalks.Club)** — free, 10 weeks, covers RAG, vector search, embeddings, evaluation, monitoring. This is the highest-value single resource for the AI half of your portfolio.
  Repo: https://github.com/DataTalksClub/llm-zoomcamp
  YouTube playlist: https://www.youtube.com/playlist?list=PL3MmuxUbc_hLZFNgSad56pDBKK8KO0XIv
  Course page: https://datatalks.club/blog/llm-zoomcamp.html
- **Build Your First RAG Application — Alexey Grigorev (2026 workshop)**
  https://www.youtube.com/watch?v=KSItlTAsMsk

### RAG specifically
- **RAG Tutorial: Complete Introduction to Retrieval Augmented Generation**
  https://www.youtube.com/watch?v=63B-3rqRFbQ
- **RAG Architecture Guide 2026 (written)** — covers chunking, hybrid search, reranking, and RAGAS evaluation
  https://jobsbyculture.com/blog/rag-architecture-guide-2026

### Structured outputs & Pydantic
- I did not find a single authoritative free video on `instructor` / Pydantic-enforced LLM output. Search `pydantic structured output llm tutorial` and `instructor library python llm`. The library docs are short and better than most videos here.
- Practice target: force a model to return a Pydantic object across 50 calls with zero parse failures. Handle the failures that do occur rather than retrying blindly.

### Evaluation — the part almost everyone skips
This is where your portfolio separates from the crowd, and it is under-covered on YouTube. The LLM Zoomcamp evaluation and monitoring modules are the best free treatment. Search additionally for `llm evaluation golden dataset` and `ragas tutorial`.

Understand before building: **execution accuracy vs exact match**, why LLM-as-judge is convenient and biased, and why a 50-example hand-labelled set beats a 5000-example auto-generated one.

> **Checkpoint:** you can make an LLM return validated structured data reliably, and you can measure whether it was right.

---

## STAGE 5 — Finish Project 1, then build Project 4 (5 weeks, ~55 h)
Go back and complete `01-sentinel-etl.md` Phase 4 (LLM auditor + eval).

Then build DocuFlow (`04-docuflow.md`). New skills needed along the way, all *just-in-time*:

### FastAPI
- **FastAPI Full Course (2026)** — https://www.youtube.com/watch?v=p5Gr8_5zKoY
- **Python FastAPI Full-Stack Tutorial (2026)** — https://www.youtube.com/watch?v=iukOehU5aF4
- **freeCodeCamp FastAPI Course** (older but the fundamentals are unchanged) — https://www.youtube.com/watch?v=tLKKmouUams

### Celery / Redis
- Search `celery redis python tutorial` and `celery task queue explained`. One hour.
- Concept that matters more than the syntax: what makes a task safe to retry. If your task is not idempotent, retries corrupt data.

### OCR & document AI
- No single strong course found. Search `tesseract ocr python tutorial`, `paddleocr tutorial`, `opencv deskew image python`, `vision llm document extraction`.
- The genuinely hard part is not the OCR call — it is deciding what to do when OCR confidence is low. Build the confidence-routing logic before you optimise the OCR.

---

## STAGE 6 — Build Project 3 (5 weeks, ~60 h) *— the flagship*
QueryMind (`03-querymind.md`). Prerequisites: Stages 1, 4, and FastAPI from Stage 5.

### pgvector & embeddings
- Covered in LLM Zoomcamp. Additionally search `pgvector tutorial postgres` and `sentence transformers tutorial`.

### sqlglot
- Effectively no video tutorials exist for this. The library's own README and the `lineage` module source are the documentation. Read the AST by printing `repr(sqlglot.parse_one(sql))` on progressively harder queries — an hour of that teaches more than any video would.

### Text-to-SQL as a research area
- Search `text to sql llm`, `spider benchmark`, `BIRD benchmark text to sql`. Read one or two papers rather than watching videos; the field moves faster than YouTube covers it.
- The Spider and BIRD benchmarks come with labelled question/SQL pairs and will save you days of dataset authoring.

---

## STAGE 7 — Portfolio polish (1 week, ~10 h)
- Rewrite all three READMEs assuming a reader gives you 90 seconds
- Fill every `[X]%` in the resume with a measured number
- Record three demo videos
- Write ADRs for each project
- Publish dbt docs / a lineage site on GitHub Pages

---

## STAGE 8 *(optional)* — Streaming (5 weeks, ~65 h)
Only if you are specifically targeting streaming-heavy roles, or after you have shipped three projects.

### Kafka
- **Apache Kafka for Data Engineers Full Course 2026** — https://www.youtube.com/watch?v=wanQj6_-8qQ
- **TechWorld with Nana — Apache Kafka Complete Course for Beginners** — Python + Docker Compose, producer and consumer from scratch. Channel: https://www.youtube.com/c/TechWorldwithNana (search `Kafka` there; the course is ~1 hour)
- **Confluent — Apache Kafka for Python Developers (official playlist)**
  https://www.youtube.com/playlist?list=PLa7VYi0yPIH1odVnZC430071CVD_4Sx1e
- Module 6 of the Data Engineering Zoomcamp also covers streaming.

### TimescaleDB, anomaly detection
- Search `timescaledb hypertable tutorial`, `continuous aggregates timescaledb`, `time series anomaly detection python`, `statsmodels STL decomposition`.

Then build StreamScribe (`02-streamscribe.md`).

---

## STAGE 9 *(optional)* — LineageLens (3 weeks, ~45 h)
Smallest project, most niche skills. Build it if you enjoyed the sqlglot work in Project 3, or if you are targeting data platform / developer tooling roles specifically. Skills: sqlglot in depth, networkx, GitHub Actions beyond CI.

Search `networkx tutorial python`, `topological sort explained`, `github actions pull request comment action`.

---

# PART 3 — QUICK REFERENCE

## Skill → Project mapping

| Skill | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| Docker / Compose | ● | ● | ● | ● | ○ |
| Advanced SQL | ● | ● | ● | ● | ● |
| Dimensional modelling / SCD2 | ● | ○ | ● | ● | ○ |
| Airflow | ● | ○ | | ○ | |
| dbt | ● | | ○ | ● | ● |
| Data quality / GE | ● | ○ | | ● | |
| Kafka / streaming | | ● | | | |
| Windowing & watermarks | | ● | | | |
| Time-series DB | | ● | | | |
| Anomaly detection | ● | ● | | | |
| LLM APIs | ● | ● | ● | ● | ● |
| Structured output / Pydantic | ● | ● | ● | ● | ● |
| Embeddings / pgvector | | | ● | | |
| RAG | | | ● | | |
| Evaluation harness | ● | ● | ● | ● | ○ |
| Vision LLM / OCR | | | | ● | |
| FastAPI | | | ● | ● | |
| Celery / Redis | | | | ● | |
| sqlglot | | | ● | | ● |
| networkx / graphs | | | | | ● |
| Power BI | ● | | | ● | |
| GitHub Actions | ● | ● | ● | ● | ● |

● = core   ○ = light use

## The five things interviewers actually probe

Regardless of which projects you build, be able to answer these cold:

1. **Idempotency** — "What happens if this pipeline runs twice for the same day?"
2. **SCD Type 2** — "How do you track a customer changing address without losing history?"
3. **Failure handling** — "A source file arrives malformed at 3am. Walk me through what happens."
4. **LLM grounding** — "How do you know the model didn't make that number up?"
5. **Measurement** — "You said 94% accuracy. Measured how, on what set, against what baseline?"

If a project cannot answer these, it is not finished, no matter how much code exists.

## Channels worth subscribing to

Found repeatedly across searches and consistently good:
- **TechWorld with Nana** — Docker, Kafka, DevOps — https://www.youtube.com/c/TechWorldwithNana
- **DataTalks.Club** — the Zoomcamps
- **Start Data Engineering** (Joseph Machado) — written + video, unusually practical — https://www.startdataengineering.com/
- **Confluent** — official Kafka education

## A warning about tutorial time

It is very easy to spend five months watching and zero months building, and to feel productive the whole time. The videos above total well over 60 hours. **You do not need to finish any of them.** Watch until you can start, then start. The build is what you will talk about in interviews; nobody asks which courses you completed.
