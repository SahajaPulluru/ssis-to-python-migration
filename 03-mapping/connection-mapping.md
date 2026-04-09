# SSIS → Python Connection Mapping

## Connection Manager Types

| SSIS Connection Manager | Python Library | Configuration |
|---|---|---|
| **OLE DB (SQL Server)** | `sqlalchemy` + `pyodbc` | Connection string via `create_engine()` |
| **ADO.NET (SQL Server)** | `sqlalchemy` + `pyodbc` | Same as OLE DB equivalent in Python |
| **ODBC** | `pyodbc` | ODBC DSN or connection string |
| **Flat File (CSV/TXT)** | `pandas` `read_csv()` | File path string |
| **Excel** | `pandas` `read_excel()` | Requires `openpyxl` engine |
| **FTP/SFTP** | `ftplib` / `paramiko` | Connect, download to local path, read |
| **HTTP** | `requests` | API calls generating JSON / DataFrames |
| **SMTP (Email)** | `smtplib` | Standard library mailing |

## SQL Server (OLE DB / ADO.NET) → Python `sqlalchemy`

### SSIS Connection String
```
Data Source=SQLPROD01;
Initial Catalog=AdventureWorks;
Provider=SQLNCLI11.1;
Integrated Security=SSPI;
```

### Python Equivalent
```python
import os
import sqlalchemy as sa
from sqlalchemy.engine import URL

# Loading from our .env file instead of hardcoded strings
server = os.environ.get('DB_SERVER', 'localhost')
database = os.environ.get('DB_NAME', 'AdventureWorks')
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

# Create ODBC connection string
connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)

engine = sa.create_engine(connection_url)

# Read table into dataframe
import pandas as pd
df = pd.read_sql_table("Customer", schema="dbo", con=engine)
```

### With Parameterized Query Pushdown
```python
query = sa.text("""
    SELECT CustomerID, CustomerName, Email, ModifiedDate
    FROM dbo.Customer
    WHERE ModifiedDate > :watermark
""")

df = pd.read_sql_query(query, con=engine, params={"watermark": '2024-01-01'})
```

## Flat File → Local Filesystem

### SSIS Flat File Connection
```
C:\ETL\Data\customers.csv
Format: Delimited (comma)
Header: Yes
Text Qualifier: double-quote
```

### Python Equivalent
```python
import pandas as pd

# Files are loaded directly from the local filesystem
file_path = "C:/ETL/Data/customers.csv"

df = pd.read_csv(
    file_path, 
    sep=',', 
    header=0, 
    quotechar='"', 
    escapechar='\\'
)

# With explicit typing (recommended)
dtype_mapping = {
    'CustomerID': 'int64',
    'CustomerName': 'string',
    'Email': 'string'
}
df = pd.read_csv(file_path, dtype=dtype_mapping, parse_dates=['ModifiedDate'])
```

## Secrets Management

### SSIS: Package/Project Parameters + SQL Server Agent
```
Connection string stored in SSIS Catalog environment variables
or SQL Server Agent job step configuration.
```

### Python: `.env` files using `python-dotenv`
```python
# Create a .env file locally (never committed to git):
# DB_SERVER=SQLPROD01
# DB_NAME=AdventureWorks
# DB_USER=admin
# DB_PASSWORD=SecretPassword123

# Usage in Python scripts:
import os
from dotenv import load_dotenv

# Load it once at the start of your script
load_dotenv(dotenv_path='config/.env')

# Access securely
username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
```
