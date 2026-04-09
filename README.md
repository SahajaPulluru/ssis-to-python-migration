<p align="center">
  <img src="https://img.shields.io/badge/SSIS-→_Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="SSIS to Python" />
  <img src="https://img.shields.io/badge/Pandas-SQLAlchemy-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas toolkit" />
  <img src="https://img.shields.io/badge/AI_Assisted-Claude-C97539?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude AI" />
</p>

<h1 align="center">migration-spec-kit</h1>

<p align="center">
  <strong>A structured, AI-assisted framework for migrating SSIS ETL pipelines to generic Python.</strong>
  <br />
  Pandas &bull; SQLAlchemy &bull; Full Lifecycle Coverage
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

Migrating from SSIS to purely coded environments is not a lift-and-shift. SSIS packages contain implicit logic buried in XML (DTSX), data flow transformations, connection managers, embedded SQL, and event handlers. Manual conversion is slow, error-prone, and inconsistent across teams.

**migration-spec-kit** solves this by providing:

| Capability | Description |
|---|---|
| **Source Inventory** | Organize DTSX packages and stored procedures before touching anything |
| **Automated Analysis** | AI-powered DTSX parsing to extract data flows, dependencies, and transformation logic |
| **Component Mapping** | 30+ SSIS-to-Python/Pandas translation references with working code examples |
| **Code Generation** | Python standard scripts deployed through cron orchestrators |
| **Validation Framework** | Row counts, data quality checks, and reconciliation between source and target |
| **Claude Skill** | Purpose-built AI skill that reads DTSX files and generates Python architecture |

---

## Quick Start

```bash
# Clone
git clone https://github.com/yasarkocyigit/migration-spec-kit.git
cd migration-spec-kit

# Install Requirements
python -m venv venv
source venv/bin/activate
pip install -r 04-target/requirements.txt

# Add your SSIS packages
cp /path/to/your/*.dtsx 01-source/dtsx/

# Create Environment secrets
cp 04-target/config/.env.example 04-target/config/.env
```

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Phase 1   │     │   Phase 2   │     │   Phase 3   │     │   Phase 4   │     │   Phase 5   │
│   Source    │────▶│  Analysis   │────▶│  Mapping    │────▶│  Generate   │────▶│  Validate   │
│  Inventory  │     │  (AI/Manual)│     │  Review     │     │  Python Code│     │  & Compare  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
  01-source/          02-analysis/        03-mapping/         04-target/          05-validation/
```

**Phase 1 — Source Inventory:** Drop `.dtsx` files and stored procedures into `01-source/`. These are read-only originals — never modified.

**Phase 2 — Automated Analysis:** Use the Claude skill or parser script to extract package metadata: tasks, data flows, dependencies, and complexity scores. Output goes to `02-analysis/`.

**Phase 3 — Mapping Review:** Consult the mapping docs in `03-mapping/` to understand how each SSIS component, connection type, and data type translates to Python.

**Phase 4 — Code Generation:** Generate independent `.py` scripts executing `sqlalchemy` extraction, `pandas` transformations, and target loading via `pyodbc` or `psycopg2`.

**Phase 5 — Validation:** Run SQL queries from `05-validation/` to compare row counts, aggregates, and data quality between source and target DBs.

---

## Repository Structure

```
migration-spec-kit/
│
├── 01-source/                          # Original SSIS artifacts (read-only)
│   ├── dtsx/                           # SSIS package files (.dtsx)
│   ├── stored-procedures/              # SQL Server stored procedures (.sql)
│   └── connection-managers/            # Connection documentation (sanitized)
│
├── 02-analysis/                        # Analysis output
│   ├── package-inventory.md            # What each DTSX does
│   └── dependency-map.md               # Inter-package and table dependencies
│
├── 03-mapping/                         # SSIS → Python translation reference
│   ├── component-mapping.md            # 30+ Pandas/Task component equivalents
│   ├── connection-mapping.md           # OLE DB / Flat File → Python libraries
│   └── data-type-mapping.md            # SQL Server → Python types
│
├── 04-target/                          # Generic Python Execution Shell
│   ├── config/                         # .env setups
│   ├── extract/                        # Source extractions (like OLE DB Src)
│   ├── transform/                      # Data Flow Transformations execution
│   ├── load/                           # Target Destinations
│   ├── tests/                          # Pytest framework logic validation
│   ├── main.py                         # ETL Orchestrator logic
│   └── requirements.txt                # pip dependencies
│
├── 05-validation/                      # Post-migration validation
│   ├── row-count-checks.sql            # Source vs. target counts
│   ├── data-quality-checks.sql         # Nulls, dupes, referential integrity
│   └── reconciliation-report.md        # Sign-off template
│
├── 06-docs/                            # Project documentation
│   ├── migration-runbook.md            # Execution guides/Cron jobs
│   ├── rollback-plan.md                # Recovery protocols
│   └── decision-log.md                 # Architecture decision records
│
└── skills/                             # Claude AI skill
    └── ssis-migration/
        └── SKILL.md                    # Defines ETL standards
```

---

## Target Architecture

Data follows a standard staging procedure instead of Medallion pools:

```
Target Database
│
├── staging                         ← Raw inserted records mapped natively
│   ├── raw_customers
│   └── raw_orders
│
└── production                      ← SCD Type 2 inserted Dimensions and Facts
    ├── dim_customer 
    ├── dim_date
    ├── fact_order
    └── _audit_log                  ← Custom Python auditing logging target
```

---

## Component Mapping Highlight

> Full details in [`03-mapping/component-mapping.md`](03-mapping/component-mapping.md)

| SSIS Component | Python Equivalent |
|---|---|
| Execute SQL Task | `engine.execute(sa.text())` |
| Data Flow Task | Independent function mutating Pandas `.DataFrame` |
| OLE DB Source | `pd.read_sql()` |
| Flat File Source | `pd.read_csv()` / `.read_json()` |
| Lookup Transform | `pd.merge()` |
| Derived Column | `df['col'] = df['other'] + 1` |
| Aggregate | `df.groupby().agg()` |
| Event Handler | `try/except` -> `logging.error()` -> `smtplib` |

---

## Claude Skill

The `skills/ssis-migration/` folder contains a purpose-built [Claude skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) that automates DTSX analysis and generating standard Python Data Engineering patterns.

**Installation:**

Upload the `skills/ssis-migration/` folder as a zip via Claude.ai (Settings → Skills) or place it in your CLI tools.

**Usage:**

```
"Analyze my SSIS package ETL_Load_Customers.dtsx and restructure its operations
 into standard extract.py, transform.py, load.py flows governed by requirements.txt."
```

---

## Prerequisites

| Requirement | Purpose |
|---|---|
| Target Database | Your destination (Snowflake/Postgres/MSSQL) |
| Python 3.9+ | Target language |
| Cron Tools | System scheduler for pipelines |

---

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE) for details.
