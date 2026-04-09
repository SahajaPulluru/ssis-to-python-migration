# Rollback Plan

## When to Rollback

Trigger rollback if ANY of the following occur during parallel run or after cutover:

- Row count discrepancy > 1% between source and target systems
- Revenue/amount discrepancy > $0.01 per aggregation criteria
- Python ETL process fails 3+ consecutive runs unexpectedly
- Python `MemoryErrors` resulting in server crash/denial of service
- Data quality checks report critical violations in downstream reports

## Rollback Steps

### Immediate (< 1 hour)

1. **Pause Python ETL execution**
   - Comment out the deployment cron job.
   ```bash
   crontab -e
   # comment out with #: # 0 2 * * * cd /opt/etl/migration-spec-kit/04-target && ...
   ```

2. **Re-enable SSIS packages**
   - Head to SQL Server Agent -> Jobs -> Enable `ETL_Load_Customers` 

3. **Notify stakeholders**
   - Email data-team@company.com with rollback reason
   - Update `decision-log.md` with incident facts.

### Post-Rollback Investigation

1. Review the `logging` outputs on the execution server (e.g., `/var/log/etl.log` or inside the command window terminal).
2. Trace the exact row/data format where Pandas operations threw a type error or miscalculated an aggregation.
3. Compare target tables where the data was partially populated prior to error.

### Data Recovery (if needed)

If the target data warehouse tables were corrupted or malformed before the Python error was captured:

1. Target databases without Time Travel or Snapshots: Execute a script to DELETE/TRUNCATE records based on the `_etl_load_date` or specific load batch IDs for the corrupted loads.
   ```sql
   DELETE FROM production.dim_customer WHERE _etl_load_date >= '2024-06-15'
   ```
2. If total corruption occurred on the database level, request a database restore from prior night's backup.
3. Reprocess the clean source data utilizing the reliable SSIS platform.

## Prevention

After fixing the issue inside the Python scripts:
1. Add smaller unit tests representing that edge case block into the translation schema.
2. Re-run parallel deployments for minimum 3 days confirming no other outliers surface before turning off SSIS again.
