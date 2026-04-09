<p align="center">
  <img src="https://img.shields.io/badge/SSIS-→_Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" alt="SSIS to Databricks" />
  <img src="https://img.shields.io/badge/Unity_Catalog-Medallion-00A1E0?style=for-the-badge&logo=delta&logoColor=white" alt="Unity Catalog" />
  <img src="https://img.shields.io/badge/AI_Assisted-Claude-C97539?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude AI" />
</p>

<h1 align="center">migration-spec-kit</h1>

<p align="center">
  <strong>A structured, AI-assisted framework for migrating SSIS ETL pipelines to Databricks.</strong>
  <br />
  Medallion Architecture &bull; Unity Catalog &bull; Full Lifecycle Coverage
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#repository-structure">Structure</a> &bull;
  <a href="#component-mapping">Mapping</a> &bull;
  <a href="#claude-skill">AI Skill</a> &bull;
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

## The Problem

Migrating from SSIS to Databricks is not a lift-and-shift. SSIS packages contain implicit logic buried in XML (DTSX), data flow transformations, connection managers, embedded SQL, and event handlers. Manual conversion is slow, error-prone, and inconsistent across teams.

**migration-spec-kit** solves this by providing:

| Capability | Description |
|---|---|
| **Source Inventory** | Organize DTSX packages and stored procedures before touching anything |
| **Automated Analysis** | AI-powered DTSX parsing to extract data flows, dependencies, and transformation logic |
| **Component Mapping** | 30+ SSIS-to-Databricks translation references with working code examples |
| **Code Generation** | Databricks notebooks following Bronze/Silver/Gold Medallion architecture |
| **Validation Framework** | Row counts, data quality checks, and reconciliation between source and target |
| **Claude Skill** | Purpose-built AI skill that reads DTSX files and generates Databricks notebooks |

---

## Quick Start

```bash
# Clone
git clone https://github.com/yasarkocyigit/migration-spec-kit.git
cd migration-spec-kit

# Add your SSIS packages
cp /path/to/your/*.dtsx 01-source/dtsx/
cp /path/to/your/*.sql  01-source/stored-procedures/

# (Optional) Run the DTSX parser
pip install lxml pandas
python skills/ssis-migration/scripts/parse_dtsx.py 01-source/dtsx/YourPackage.dtsx
```

---

## How It Works

<img width="1512" height="946" alt="ssis-migration-spec" src="https://github.com/user-attachments/assets/2b766057-257c-455a-979c-7b0e2fb5b89f" />


```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Phase 1   │     │   Phase 2   │     │   Phase 3   │     │   Phase 4   │     │   Phase 5   │
│   Source    │────▶│  Analysis   │────▶│  Mapping    │────▶│  Generate   │────▶│  Validate   │
│  Inventory  │     │  (AI/Manual)│     │  Review     │     │  Notebooks  │     │  & Compare  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
  01-source/          02-analysis/        03-mapping/         04-target/          05-validation/
```

**Phase 1 — Source Inventory:** Drop `.dtsx` files and stored procedures into `01-source/`. These are read-only originals — never modified.

**Phase 2 — Automated Analysis:** Use the Claude skill or parser script to extract package metadata: tasks, data flows, dependencies, and complexity scores. Output goes to `02-analysis/`.

**Phase 3 — Mapping Review:** Consult the mapping docs in `03-mapping/` to understand how each SSIS component, connection type, and data type translates to Databricks.

**Phase 4 — Code Generation:** Generate Databricks notebooks following Medallion architecture. Bronze (raw ingestion), Silver (cleansed/validated), Gold (business dimensions and facts).

**Phase 5 — Validation:** Run SQL queries from `05-validation/` to compare row counts, aggregates, and data quality between source and target.

---

## Repository Structure

```
migration-spec-kit/
│
├── 01-source/                          # Original SSIS artifacts (read-only)
│   ├── dtsx/                           # SSIS package files (.dtsx)
│   ├── stored-procedures/              # SQL Server stored procedures (.sql)
│   ├── sql-queries/                    # Embedded SQL extracted from packages
│   └── connection-managers/            # Connection documentation (sanitized)
│
├── 02-analysis/                        # Analysis output
│   ├── package-inventory.md            # What each DTSX does
│   ├── dependency-map.md               # Inter-package and table dependencies
│   └── complexity-assessment.md        # Effort estimation per package
│
├── 03-mapping/                         # SSIS → Databricks translation reference
│   ├── component-mapping.md            # 30+ task/transform equivalents
│   ├── connection-mapping.md           # OLE DB / Flat File → JDBC / cloud storage
│   └── data-type-mapping.md            # SQL Server → Spark/Delta type mapping
│
├── 04-target/                          # Generated Databricks code
│   ├── notebooks/
│   │   ├── bronze/                     # Raw ingestion (JDBC → Delta)
│   │   ├── silver/                     # Cleansing, dedup, validation
│   │   └── gold/                       # SCD Type 2, fact merges, aggregations
│   ├── ddl/                            # Unity Catalog CREATE TABLE statements
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── workflows/                      # Databricks Workflow job definitions (JSON)
│   └── shared/                         # Reusable utility functions
│
├── 05-validation/                      # Post-migration validation
│   ├── row-count-checks.sql            # Source vs. target counts
│   ├── data-quality-checks.sql         # Nulls, dupes, referential integrity, SCD2
│   └── reconciliation-report.md        # Sign-off template
│
├── 06-docs/                            # Project documentation
│   ├── migration-runbook.md            # Step-by-step execution guide
│   ├── rollback-plan.md                # Recovery procedures + Delta time travel
│   └── decision-log.md                 # Architecture decision records
│
└── skills/                             # Claude AI skill
    └── ssis-migration/
        ├── SKILL.md                    # Skill instructions (Anthropic skill spec)
        ├── references/                 # DTSX structure guide + Databricks patterns
        └── scripts/
            └── parse_dtsx.py           # Standalone DTSX XML parser
```

---

## Target Architecture

```
Unity Catalog: migration_prod
│
├── bronze                          ← Raw, source-aligned, append-only
│   ├── raw_customers
│   ├── raw_orders
│   └── _audit_log
│
├── silver                          ← Cleansed, deduplicated, validated
│   ├── cleansed_customers
│   ├── cleansed_orders
│   └── inactive_customers_log
│
└── gold                            ← Business-level dimensions & facts
    ├── dim_customer (SCD Type 2)
    ├── dim_date
    ├── dim_region
    ├── fact_order
    ├── ref_currency_rate
    └── _audit_log
```

---

## Component Mapping

> Full details in [`03-mapping/component-mapping.md`](03-mapping/component-mapping.md)

| SSIS Component | Databricks Equivalent |
|---|---|
| Execute SQL Task | `spark.sql()` or `%sql` notebook cell |
| Data Flow Task | PySpark DataFrame pipeline |
| OLE DB Source | `spark.read.format("jdbc")` with query pushdown |
| Flat File Source | `spark.read.csv()` / `.parquet()` / `.json()` |
| Lookup Transform | `df.join(broadcast(lookup_df))` |
| Conditional Split | `df.filter()` per branch |
| Derived Column | `df.withColumn()` + `F.when()` / `F.upper()` / `F.trim()` |
| Aggregate | `df.groupBy().agg(F.sum(), F.count(), F.avg())` |
| Merge Join | `df1.join(df2, on="key", how="inner")` |
| OLE DB Destination | `df.write.format("delta").saveAsTable()` |
| Execute Package Task | `dbutils.notebook.run()` |
| For Each Loop Container | Python `for` loop + `dbutils.notebook.run()` |
| Sequence Container | Notebook sections or orchestrated notebooks |
| Package Variables | `dbutils.widgets` |
| Connection Manager | `dbutils.secrets` + JDBC URL / Unity Catalog connection |
| Event Handler (OnError) | `try`/`except` + workflow notifications |
| HASHBYTES | `F.sha2(F.concat_ws(...), 256)` |
| T-SQL MERGE | Delta Lake `MERGE INTO` |
| Checkpoint | Delta transactions (ACID guarantees) |

---

## What's Included (Examples)

This repo ships with **working examples** demonstrating a realistic migration:

| Source (SSIS) | Target (Databricks) | Pattern |
|---|---|---|
| `ETL_Load_Customers.dtsx` | `bronze/load_raw_customers.py` → `silver/cleanse_customers.py` → `gold/merge_dim_customer.py` | Incremental load → SCD Type 2 |
| `ETL_Load_Orders.dtsx` | `bronze/load_raw_orders.py` → `gold/merge_fact_orders.py` | Multi-output data flow → Fact merge with surrogate keys |
| `sp_MergeCustomerDim.sql` | `gold/merge_dim_customer.py` | HASHBYTES → `sha2()`, SCD Type 2 expire/insert |
| `sp_MergeOrderFact.sql` | `gold/merge_fact_orders.py` | Late-arriving dimensions, currency conversion, region aggregation |

---

## Claude Skill

The `skills/ssis-migration/` folder contains a purpose-built [Claude skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) that automates DTSX analysis and Databricks code generation.

**Installation:**

Upload the `skills/ssis-migration/` folder as a zip via Claude.ai (Settings → Skills) or place it in your Claude Code skills directory.

**Usage:**

```
"Analyze my SSIS package ETL_Load_Customers.dtsx and convert it to
 a Databricks notebook using Medallion architecture with Unity Catalog."
```

The skill will:
1. Parse the DTSX XML and extract all components
2. Generate Bronze, Silver, and Gold notebooks
3. Create Unity Catalog DDL statements
4. Produce validation queries

See [`skills/ssis-migration/SKILL.md`](skills/ssis-migration/SKILL.md) for full capabilities and patterns.

---

## Prerequisites

| Requirement | Purpose |
|---|---|
| Databricks workspace | Unity Catalog enabled, with compute access |
| SQL Server access | Source system for validation queries |
| Python 3.9+ | DTSX parser script (`lxml`, `pandas`) |
| Claude *(optional)* | AI-assisted analysis and code generation |

---

## Contributing

Contributions welcome — especially new SSIS component patterns, additional examples, and edge case handling. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built by <a href="https://github.com/yasarkocyigit">@yasarkocyigit</a>
</p>
