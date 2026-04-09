---
name: ssis-migration
description: >
  Analyzes SSIS packages (.dtsx) and SQL Server stored procedures, then generates
  Python ETL scripts.
  Use when user says "migrate SSIS", "convert DTSX", "SSIS to Python",
  "analyze this package", "convert stored procedure to Python", or uploads .dtsx files.
  Do NOT use for ADF pipeline migration or general SQL conversion without SSIS context.
license: MIT
metadata:
  author: yasarkocyigit
  version: 1.0.1
  category: data-engineering
  tags: [ssis, python, migration, etl]
---

# SSIS to Python Migration Skill

## Overview

This skill converts SSIS (SQL Server Integration Services) ETL packages and associated
stored procedures into standard Python ETL scripts using libraries like `pandas`, `sqlalchemy`, or pure Python processing.

## Instructions

### Step 1: Analyze the DTSX Package

Parse the DTSX XML file and extract:

1. **Connection Managers** — identify all data sources and destinations
2. **Control Flow** — list all tasks in execution order (follow PrecedenceConstraints)
3. **Data Flow** — for each Pipeline task, extract:
   - Source components (OLE DB, Flat File, etc.) and their SQL queries
   - Transformations (Derived Column, Conditional Split, Lookup, Aggregate, etc.)
   - Destinations and their target tables
   - Error outputs
4. **Variables and Parameters** — list all package/project variables with data types
5. **Precedence Constraints** — map execution order and conditions (Success/Failure/Expression)
6. **Script Tasks** — identify C# or VB.NET code within script tasks for Python conversion
7. **Custom Components** — note any third-party or custom-built pipeline components
8. **Package Configurations** — identify XML configuration files (.dtsConfig) or environment variables

When analyzing, consult `references/dtsx-structure-guide.md` for DTSX XML element mappings.

### Step 2: Analyze Stored Procedures

For each `.sql` file referenced by the DTSX:

1. Identify the merge/upsert pattern (INSERT, MERGE, SCD Type 1/2)
2. Extract source and target tables
3. Note any cryptographic functions (like HASHBYTES) to map to Python `hashlib`
4. Identify transaction handling (BEGIN TRAN / COMMIT / ROLLBACK)
5. Extract audit/logging logic

### Step 3: Generate Migration Output

For each SSIS package, produce Python ETL scripts:

**Extract scripts** (`extract/`):
- Connect to sources using `sqlalchemy` or specific DB connectors
- Query extraction or file reading logic (e.g., `pandas.read_sql`, `pandas.read_csv`)
- Handle XML configurations by loading them into Python dictionaries or converting to `.env`/JSON

**Transform scripts** (`transform/`):
- Implement Data Flow transformations using Python/pandas (e.g., merging, filtering, applying rules)
- Convert Script Tasks with C# code into native Python functions
- Implement Custom Components logic with custom Python modules

**Load scripts** (`load/`):
- Write modified DataFrames back to destination databases using `to_sql` or bulk insertion tools
- Implement Stored Procedure logic (MERGE/UPSERT) natively in Python, or orchestrate SQL commands via Python
- Implement audit/logging

### Step 4: Generate Supporting Artifacts

- **Configuration Files** (`config/`): JSON or YAML files migrating XML configuration details
- **Requirements** (`requirements.txt`): Python dependent libraries
- **Orchestration** (`main.py` or `dag.py`): Entry point executing extract, transform, load scripts in correct precedence

## Component Mapping Reference

Use this quick reference for translating SSIS components.

| SSIS Component | Python Equivalent |
|---|---|
| Execute SQL Task | `sqlalchemy.text()` execution |
| Data Flow Task | Python ETL pipeline (often `pandas` based) |
| OLE DB Source | `pd.read_sql()` |
| Flat File Source | `pd.read_csv()` |
| Derived Column | DataFrame column assignment (`df['new_col'] = ...`) |
| Conditional Split | DataFrame filtering (`df[df['col'] == cond]`) |
| Lookup | `pd.merge()` |
| Aggregate | `df.groupby().agg()` |
| OLE DB Destination | `df.to_sql()` or specific fast loaders |
| Package Variable | Python variables or loaded from config/`.env` |
| Connection Manager | External DB connection configurations |
| HASHBYTES | `hashlib` library (e.g., `hashlib.sha256()`) |
| Script Task (C#) | Python functions running custom logic |
| Custom Component | Custom Python module implementation |
| Package Config (XML) | JSON / YAML / `.env` config file |

## Data Type Mapping

| SQL Server | Python/Pandas |
|---|---|
| int | int / `Int64` |
| bigint | int / `Int64` |
| varchar/nvarchar | str / `object` / `string` |
| decimal(p,s) | `decimal.Decimal` |
| money | `decimal.Decimal` |
| datetime/datetime2 | `datetime` / `pd.Timestamp` |
| date | `datetime.date` |
| bit | bool / `boolean` |
| uniqueidentifier | `uuid.UUID` or str |

## CRITICAL Rules

- Always preserve the original SSIS execution order from PrecedenceConstraints
- Never hardcode credentials — use `.env` files or secure vaults in Python
- Add proper logging via standard Python `logging` module to replace SSIS logging
- Accurately convert C# syntax (LINQ, specific .NET classes) to standard Pythonic equivalents
- Use `decimal.Decimal` for financial amounts — precision matters
- Handle NULL values correctly (e.g., `pd.isna`, `None`)
- Replace XML configurations natively with Python dictionaries parsed from JSON or python classes

## Troubleshooting

**Error: Cannot parse DTSX**
Cause: File may be encrypted or use non-standard XML
Solution: Ask user to export without encryption from SSDT/Visual Studio

**Error: Complex C# Script Task**
Cause: Script uses highly specific .NET libraries
Solution: Identify the core logical goal and replicate it using available Python modules, requesting user clarification if the external library behavior is unknown.

**Error: Custom Component not recognized**
Cause: Third-party component logic is proprietary or unknown
Solution: Ask user what the component does and implement an equivalent Python function.

**Error: XML config mapping missing**
Cause: Config relies on external runtime state
Solution: Set up a runtime argument parser in Python (`argparse`) or ask user for the resolved values.
