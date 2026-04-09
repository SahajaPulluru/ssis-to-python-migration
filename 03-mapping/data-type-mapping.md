# SQL Server → Python/Pandas Data Type Mapping

## Numeric Types

| SQL Server | SSIS Data Type | Python Built-in | Pandas/Numpy Dtype | Notes |
|---|---|---|---|---|
| `bit` | `DT_BOOL` | `bool` | `bool` or `boolean` | Use Pandas `boolean` for missing value support. |
| `tinyint` | `DT_UI1` | `int` | `uint8` | |
| `smallint` | `DT_I2` | `int` | `int16` | |
| `int` | `DT_I4` | `int` | `int32` / `Int32` | Use Pandas `Int32` for nullable ints. |
| `bigint` | `DT_I8` | `int` | `int64` / `Int64` | Use Pandas `Int64` for nullable ints. |
| `float` | `DT_R4` | `float` | `float64` | |
| `real` | `DT_R4` | `float` | `float32` | |
| `decimal(p,s)` | `DT_NUMERIC` | `decimal.Decimal` | `object` | Pandas handles `Decimal` natively via object dtype. |
| `numeric(p,s)` | `DT_NUMERIC` | `decimal.Decimal` | `object` | Same as decimal. |
| `money` | `DT_CY` | `decimal.Decimal` | `object` | Crucial for avoiding floating-point precision loss. |

## String Types

| SQL Server | SSIS Data Type | Python Built-in | Pandas Dtype | Notes |
|---|---|---|---|---|
| `char(n)` | `DT_STR` | `str` | `string` or `object` | Pandas does not enforce length. |
| `varchar(n)` | `DT_STR` | `str` | `string` or `object` | |
| `varchar(max)` | `DT_TEXT` | `str` | `string` or `object` | |
| `nchar(n)` | `DT_WSTR` | `str` | `string` or `object` | Python strings are native UTF-8. |
| `nvarchar(n)` | `DT_WSTR` | `str` | `string` or `object` | |
| `nvarchar(max)` | `DT_NTEXT` | `str` | `string` or `object` | |

## Date/Time Types

| SQL Server | SSIS Data Type | Python Built-in | Pandas Dtype | Notes |
|---|---|---|---|---|
| `date` | `DT_DBDATE` | `datetime.date` | `datetime64[ns]` | Convert to `date` objects if needed downstream. |
| `time` | `DT_DBTIME2` | `datetime.time` | `object` | Time-only data usually drops to objects in Pandas. |
| `datetime` | `DT_DBTIMESTAMP` | `datetime.datetime`| `datetime64[ns]` | |
| `datetime2(p)` | `DT_DBTIMESTAMP2`| `datetime.datetime`| `datetime64[ns]` | |
| `smalldatetime` | `DT_DBTIMESTAMP` | `datetime.datetime`| `datetime64[ns]` | |
| `datetimeoffset` | `DT_DBTIMESTAMPOFFSET` | `datetime.datetime` | `datetime64[ns, UTC]` | Pandas handles time zones robustly. |

## Binary Types

| SQL Server | SSIS Data Type | Python Built-in | Pandas Dtype | Notes |
|---|---|---|---|---|
| `binary(n)` | `DT_BYTES` | `bytes` | `object` | |
| `varbinary(n)` | `DT_BYTES` | `bytes` | `object` | |
| `varbinary(max)` | `DT_IMAGE` | `bytes` | `object` | |

## Special Types

| SQL Server | SSIS Data Type | Python Built-in | Pandas Dtype | Notes |
|---|---|---|---|---|
| `uniqueidentifier` | `DT_GUID` | `uuid.UUID` or `str` | `string` | Often cast immediately to string. |
| `xml` | `DT_NTEXT` | `str` | `string` | Parse with `xml.etree` or `lxml` if needed. |
| `json` | `DT_NTEXT` | `dict` / `list` | `object` | Parse with Python `json` library. |
| `rowversion` | `DT_BYTES` | `bytes` | `object` | Often used as change tracking indicators. |
| `hierarchyid` | `DT_BYTES` | `str` | `string` | Should be read as string representation. |

## SSIS Expression → Pandas/Python Equivalent

| SSIS Expression | Pandas / Python Equivalent |
|---|---|
| `GETDATE()` | `pd.Timestamp.now()` or `datetime.now()` |
| `YEAR(col)` | `df['col'].dt.year` |
| `MONTH(col)` | `df['col'].dt.month` |
| `DAY(col)` | `df['col'].dt.day` |
| `UPPER(col)` | `df['col'].str.upper()` |
| `LOWER(col)` | `df['col'].str.lower()` |
| `TRIM(col)` | `df['col'].str.strip()` |
| `LEN(col)` | `df['col'].str.len()` |
| `SUBSTRING(col, start, len)` | `df['col'].str[start:start+len]` |
| `REPLACE(col, old, new)` | `df['col'].str.replace(old, new)` |
| `ISNULL(col)` | `df['col'].isna()` or `pd.isna(col)` |
| `(condition) ? true : false` | `np.where(condition, true_val, false_val)` |
| `DATEADD(day, n, col)` | `df['col'] + pd.Timedelta(days=n)` |
| `DATEDIFF(day, col1, col2)` | `(df['col2'] - df['col1']).dt.days` |
| `CAST(col AS type)` | `df['col'].astype("type")` |
| `CONCATENATE(a, "|", b)` | `df['a'] + "\|" + df['b']` |
| `HASHBYTES('SHA2_256', col)` | Use `.apply()` with `hashlib.sha256` |
