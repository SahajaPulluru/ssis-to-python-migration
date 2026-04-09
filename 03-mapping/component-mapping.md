# SSIS → Python Component Mapping

## Control Flow Tasks

| SSIS Task | Python Equivalent | Notes |
|---|---|---|
| **Execute SQL Task** | `sqlalchemy` `engine.execute(text(...))` | Direct SQL execution. Parameters become `text()` binding parameters. |
| **Data Flow Task** | Pandas Pipeline / Function | Each source/target becomes read/write, transforms become pandas DataFrame operations. |
| **Execute Process Task** | `subprocess.run()` | System/Shell commands within the script. |
| **Script Task (C#)** | Native Python Function | Rewrite custom logic in standard Python. |
| **For Each Loop Container** | Python `for` loop | `for file in os.listdir(path):` or `for row in df.itertuples():` |
| **For Loop Container** | Python `while` or `for` loop | Counter-based iteration. |
| **Sequence Container** | Python module / Function | Group logic into well-named functions in `main.py`. |
| **Send Mail Task** | Python `smtplib` | Send emails via standard SMTP modules. |
| **File System Task** | `os`, `shutil` | Copy/move/delete using `shutil.copy`, `os.remove`, etc. |
| **FTP Task** | Python `ftplib` | Download/Upload files directly within script. |
| **Expression Task** | Python variable assignment | `variable = expression` |
| **Execute Package Task** | Function calls / `subprocess.run` | Import and run other python ETL sub-scripts. |

## Data Flow Transformations

| SSIS Transform | Pandas Equivalent | Example |
|---|---|---|
| **OLE DB Source** | `pd.read_sql()` | `df = pd.read_sql("SELECT *", con=engine)` |
| **Flat File Source** | `pd.read_csv()` | `df = pd.read_csv('file.csv', delimiter=',')` |
| **Excel Source** | `pd.read_excel()` | Requires `openpyxl` library. |
| **Lookup** | `pd.merge()` | `df = pd.merge(df, lookup_df, on="key", how="left")` |
| **Conditional Split** | DataFrame masking | `df_high = df[df['amount'] > 100]` |
| **Derived Column** | Column assignment | `df['new_col'] = df['a'] + df['b']` |
| **Data Conversion** | `df['col'].astype()` | `df['col'] = df['col'].astype('float64')` |
| **Aggregate** | `df.groupby().agg()` | `df.groupby('dept').agg(total=('salary', 'sum'))` |
| **Sort** | `df.sort_values()` | `df = df.sort_values(by='col', ascending=False)` |
| **Merge Join** | `pd.merge()` | Inner join between two frames: `pd.merge(df1, df2)` |
| **Union All** | `pd.concat()` | `pd.concat([df1, df2], ignore_index=True)` |
| **Multicast** | Variable reuse | Same DataFrame reference passed into multiple functions. |
| **Row Count** | `len(df)` | Store `len(df)` in a variable for auditing. |
| **OLE DB Destination** | `df.to_sql()` | `df.to_sql('table', con=engine, if_exists='append')` |
| **Flat File Destination** | `df.to_csv()` | `df.to_csv('output.csv', index=False)` |
| **Error Output** | `try / except` or Validation | Validate rows before insertion, or catch `SQLAlchemyError`. |

## Precedence Constraints

| SSIS Constraint | Python Equivalent |
|---|---|
| **On Success** (green arrow) | Natural sequential script execution. |
| **On Failure** (red arrow) | `except` block in a `try/except` structure. |
| **On Completion** | `finally` block in a `try/except/finally` structure. |
| **Expression-based** | Python `if / elif / else` block. |

## Event Handlers

| SSIS Event | Python Equivalent |
|---|---|
| **OnError** | `try`/`except` + `logging.error()` |
| **OnPreExecute** | Logic at the top of the ETL function. |
| **OnPostExecute** | Logic at the bottom/return of the ETL function. |
| **OnWarning** | `logging.warning()` |

## Variables and Parameters

| SSIS Concept | Python Equivalent | Example |
|---|---|---|
| **Package Variable** | Python Local Variable | `batch_date = "2024-01-01"` |
| **Package Parameter** | Function argument | `def extract(start_date):` |
| **Project Parameter** | Environment Variable | `os.environ.get('DB_HOST')` via `.env` |
| **Expression** | Python f-string | `query = f"SELECT * FROM t WHERE date > '{batch_date}'"` |

## Containers → Python Patterns

```
SSIS:
┌─────────────────────────────────────┐
│ Sequence Container: Pre-Processing  │
│  ├── Execute SQL: Truncate Staging  │
│  └── Execute SQL: Get Max ID       │
├─────────────────────────────────────┤
│ Data Flow: Load Data                │
├─────────────────────────────────────┤
│ Execute SQL: Merge to Dimension     │
└─────────────────────────────────────┘

Python Script:
┌─────────────────────────────────────┐
│ # Step 1: Pre-Processing           │
│ engine.execute(text("TRUNCATE.."))  │
│ max_id = pd.read_sql("SELECT MAX..")│
├─────────────────────────────────────┤
│ # Step 2: Load Data (Data Flow)    │
│ df = pd.read_sql("SELECT...", src)  │
│ df['new_col'] = ...                 │
│ df.to_sql('staging', dest)          │
├─────────────────────────────────────┤
│ # Step 3: Merge to Dimension       │
│ engine.execute(text("MERGE INTO.."))│
└─────────────────────────────────────┘
```
