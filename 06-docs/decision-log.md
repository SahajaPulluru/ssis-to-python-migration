# Decision Log

Record all architecture and design decisions made during migration.

## Template

**Decision:** [What was decided]
**Date:** [When]
**Context:** [Why this decision was needed]
**Options Considered:** [What alternatives were evaluated]
**Rationale:** [Why this option was chosen]
**Consequences:** [What trade-offs or implications]

---

## Decisions

### DEC-001: Standardized Data Warehouse Tiering (Landing -> Staging -> Production)

**Date:** 2024-xx-xx
**Context:** Need to decide target DB architecture for the migrated SSIS pipelines using Python.
**Options Considered:**
1. Direct migration — replicate SSIS staging/dim/fact structure exactly as-is into final destination tables
2. Tiered Staging Layer — Landing Tables (Raw Extract) -> Staging (Cleansed/Transformed Types) -> Production (Fact/Dimensions)

**Rationale:** Using a tiered 3-stage process allows Python transformations (`pandas`) to cleanly commit raw data before complex merging happens. Breaking execution into stages significantly eases restarting from points of failure.

**Consequences:** Requires additional persistent staging tables and schema management.

---

### DEC-002: SCD Type 2 via Native Python Hash Generation

**Date:** 2024-xx-xx
**Context:** Original sp_MergeCustomerDim uses HASHBYTES for change detection. Need to implement this efficiently in Python.
**Options Considered:**
1. SQL-side HASHBYTES within the load process.
2. Python-side hashing using `hashlib` iterating over Pandas rows during Transformation.
3. Column-by-column logical comparisons dynamically generated in Pandas.

**Rationale:** Generating hashes natively during the `transform.py` phase via `hashlib.sha256` ensures the data arriving at the Destination is immediately calculatable without putting stress on the target Data Warehouse's compute.

**Consequences:** Increases memory consumption locally in standard DataFrames during transformation routines.

---

### DEC-003: Cron/OS Level Orchestration vs Apache Airflow

**Date:** 2024-xx-xx
**Context:** We need a way to schedule and trigger the daily ETL python scripts after migrating away from SQL Server Agent.
**Options Considered:**
1. Apache Airflow / Prefect (Specialized orchestration platforms)
2. Standard Unix `cron` / Windows Task Scheduler running `main.py`
3. CI/CD Pipeline Triggers (e.g. GitHub Actions / Jenkins)

**Rationale:** For simplicity during the initial cutover phase, triggering `main.py` directly through standard cron jobs mimics SQL Server Agent best without standing up new orchestration infrastructure. We will evaluate Airflow later if dependency complexity demands it.

**Consequences:** Built-in alerting will be heavily reliant on Python's `logging` and native exceptions sending email alerts via `smtplib` manually embedded instead of Airflow's built-in hooks.
