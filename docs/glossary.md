# SentinelETL Keyword Glossary

This is the running reference for project terms. Each term is introduced when the project needs it.

## Already used

- **ETL:** Extract, Transform, Load. The general pattern of moving data from sources into a useful destination.
- **Pipeline:** A sequence of data-processing steps that runs in a defined order.
- **Raw data:** The original source preserved without cleaning or modification.
- **Source data:** Data supplied by an external file, service, or system.
- **Schema:** The columns, names, types, and structural rules of a table.
- **Row count:** The number of records in a table.
- **Primary key:** A column, or group of columns, that uniquely identifies a row.
- **Duplicate key:** A repeated value where uniqueness was expected.
- **Missing value:** An empty or unavailable field.
- **Referential integrity:** The rule that a reference in one table must point to an existing record in another table.
- **Orphan row:** A row whose referenced key does not exist in the related table.
- **Foreign key:** A column that refers to a key in another table.
- **Grain:** What one row represents, such as one order or one order line.
- **One-to-many relationship:** One record in one table relates to multiple records in another table.
- **Join:** Combining tables through related columns.
- **Virtual environment:** An isolated Python environment for one project.
- **Package:** Reusable Python code organized for installation.
- **Unit test:** An automated check of one small behavior.
- **Dependency:** Software that a project needs in order to run.
- **`pyproject.toml`:** Python project configuration, including metadata and dependencies.
- **Editable install:** A development installation that uses the current source files directly.
- **Version control:** A system for recording file changes over time.
- **Git:** The version-control tool used by this project.
- **GitHub:** A service that can host Git repositories and collaboration workflows.

## Coming next

- **Data quality check:** A rule that tests whether data meets an expected condition.
- **Deterministic check:** A check that gives the same result for the same input.
- **Profiling:** Summarizing a dataset's size, structure, and possible problems.
- **Validation:** Testing data or code against stated rules.
- **Fixture:** Small, controlled data used by a test.
- **Exception:** A Python signal that something went wrong.
- **Logging:** Recording useful runtime events for diagnosis.
- **Idempotency:** Running the same pipeline input again does not create duplicate results.
- **Watermark:** A saved position showing how far an incremental pipeline has processed.
- **Incremental load:** Processing only new or changed data instead of everything again.
- **Batch:** A bounded group of data processed together.
- **Bronze layer:** Raw, immutable data retained for traceability.
- **Silver layer:** Cleaned, typed, deduplicated data.
- **Gold layer:** Business-ready data shaped for reporting and analysis.
- **Medallion architecture:** The bronze, silver, and gold layering pattern.
- **Data warehouse:** A structured store optimized for analytical queries.
- **Schema drift:** An unexpected change in columns or data types.
- **Data contract:** An agreed description of expected columns, keys, types, and relationships.
- **Quarantine:** Separating rows that fail quality rules for review.
- **Orchestrator:** A tool that schedules and coordinates pipeline tasks.
- **DAG:** Directed Acyclic Graph; a workflow whose tasks have ordered dependencies and no loops.
- **Airflow:** The orchestration tool planned for this project.
- **Container:** An isolated process with its own packaged software environment.
- **Docker:** A tool for building and running containers.
- **Docker Compose:** A configuration tool for running multiple related containers.
- **Object storage:** File storage organized by keys and folders rather than database tables.
- **MinIO:** The local S3-compatible object store planned for the bronze layer.
- **Parquet:** A compressed, column-oriented data file format.
- **dbt:** A tool for managing SQL transformations, tests, and documentation.
- **Dimensional model:** A reporting model built from fact and dimension tables.
- **Fact table:** A table containing measurable business events.
- **Dimension table:** A table describing the entities involved in those events.
- **Star schema:** A fact table connected directly to descriptive dimension tables.
- **SCD Type 2:** A method that preserves historical versions of changing dimension records.
- **LLM:** Large Language Model; planned for interpreting quality findings, not replacing deterministic checks.
- **Structured output:** Machine-readable model output validated against a defined schema.
- **Human-in-the-loop:** A workflow where a person approves sensitive automated proposals.
- **Evaluation set:** Labeled examples used to measure a system's quality.
- **Precision:** The share of system-positive results that are correct.
- **Recall:** The share of all correct positives that the system found.
- **CI:** Continuous Integration; automated checks run when code changes.
