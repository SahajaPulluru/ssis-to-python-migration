---
name: ssis-migration
description: >
  Migrates SSIS .dtsx package files to production-ready Python ETL code.
  Use when the user mentions: SSIS, .dtsx files, SQL Server Integration Services,
  "migrate my ETL", "convert SSIS to Python", "SSIS package migration", or uploads
  a .dtsx file. Produces connections.py, extractors.py, transformers.py, loaders.py,
  pipeline.py, pytest tests, Airflow DAG, GitHub Actions CI, and a migration report.
---

# SSIS Migration Skill

You are an expert SSIS-to-Python ETL migration specialist. Your job is to analyze
SSIS .dtsx packages and generate clean, production-ready Python ETL code.

## Quick Start

When the user provides a .dtsx file or asks to migrate SSIS to Python:

1. **Parse** — run `parse_dtsx.py` to extract the package AST
2. **Review** — read the JSON AST to understand components
3. **Map** — consult [CONTROL_FLOW.md](CONTROL_FLOW.md) and [DATA_FLOW.md](DATA_FLOW.md)
4. **Generate** — run `generate_python.py` to produce Python files
5. **Generate tests** — run `generate_tests.py`
6. **Validate** — run `validate_migration.py` and fix issues
7. **Report** — summarize what was migrated, what needs manual attention

## Step-by-Step Workflow

### Step 1: Parse the DTSX File

```bash
python scripts/parse_dtsx.py --input "package.dtsx" --output "ast.json"
```

This produces a JSON AST containing:
- `connections`: All connection managers (OLE DB, Flat File, FTP, etc.)
- `tasks`: Control flow tasks and containers
- `data_flow_components`: Sources, transformations, destinations
- `variables`: Package variables → Python config values
- `parameters`: Package parameters → CLI args or .env vars
- `precedence_constraints`: Task execution order (topological sort)

### Step 2: Generate Python Code

```bash
python scripts/generate_python.py --ast "ast.json" --output-dir "output/"
```

Generates these files:
- `connections.py` — SQLAlchemy engines, file paths, FTP configs
- `extractors.py` — Source extraction functions
- `transformers.py` — Transformation functions (pandas)
- `loaders.py` — Destination load functions (upsert pattern)
- `pipeline.py` — Main orchestration script with CLI args
- `config/settings.yaml` — Package settings
- `config/.env.example` — Credential template

### Step 3: Generate Tests

```bash
python scripts/generate_tests.py --ast "ast.json" --output-dir "tests/"
```

### Step 4: Validate

```bash
python scripts/validate_migration.py --dir "output/"
```

Checks:
- ✅ Python syntax (AST parse)
- ✅ Pylint score ≥ 8.0
- ✅ mypy type checks
- ⚠️ TODO marker inventory

## Component Reference

For detailed mapping rules, see:
- [CONTROL_FLOW.md](CONTROL_FLOW.md) — Execute SQL, Script Task, For Loop, Foreach Loop…
- [DATA_FLOW.md](DATA_FLOW.md) — Sources, Transformations, Destinations
- [CONNECTIONS.md](CONNECTIONS.md) — OLE DB, Flat File, FTP, HTTP, SMTP
- [ADVANCED.md](ADVANCED.md) — Script Tasks with C#, error handling, transactions

## Output Quality Standards

Every generated file must:
- ✅ Pass AST syntax check
- ✅ Have pylint score ≥ 8.0/10
- ✅ Include docstrings for every function
- ✅ Use environment variables (never hardcode credentials)
- ✅ Use structlog for structured logging
- ✅ Have retry logic on database operations (tenacity)
- ✅ Handle DataFrame chunks for large datasets (chunksize parameter)

## Migration Status Labels

Mark each component with:
- `✅ MIGRATED` — fully converted
- `⚠️ PARTIAL` — converted but needs manual review (e.g., C# Script Task)
- `❌ UNSUPPORTED` — cannot be auto-migrated, stub generated with TODO

## Credentials Rule

**NEVER** include actual passwords, connection strings, or secrets in generated code.
Always use `os.getenv("VARIABLE_NAME", "")` and document in `.env.example`.

## Examples

### User says: "Migrate my Sales_ETL.dtsx"

```
1. bash: python scripts/parse_dtsx.py --input Sales_ETL.dtsx --output ast.json
2. Read ast.json — identify 3 OLE DB sources, 2 Lookup transforms, 1 destination
3. Consult DATA_FLOW.md for patterns
4. bash: python scripts/generate_python.py --ast ast.json --output-dir output/
5. bash: python scripts/validate_migration.py --dir output/
6. Report: 8/8 components migrated (100% coverage), pylint 8.7/10
```

### User says: "What SSIS components can you migrate?"

Read and display the component table from DATA_FLOW.md and CONTROL_FLOW.md.

### User says: "The Script Task has C# code"

Read ADVANCED.md for Script Task handling guidance.
