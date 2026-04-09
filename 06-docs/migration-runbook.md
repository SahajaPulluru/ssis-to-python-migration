# Migration Runbook

## Pre-Migration Checklist

- [ ] Source SQL Server access confirmed
- [ ] Target Database/Data Warehouse provisioned and accessible
- [ ] Python execution environment set up (virtualenv installed)
- [ ] Requirements installed (`pip install -r 04-target/requirements.txt`)
- [ ] Environment file `.env` created and populated locally within `04-target/config/`
- [ ] Network connectivity: Python ETL Server → Source/Target Systems
- [ ] All DTSX packages collected in `01-source/dtsx/`
- [ ] Analysis completed (`02-analysis/` populated)
- [ ] Mapping reviewed and approved (`03-mapping/`)

## Execution Steps

### Step 1: Initialize Database Schemas
Execute DDL manually against your target database to set up Landing, Staging, and Production Dimension/Fact tables.

### Step 2: Deploy Python Scaffolding
Copy the final code from your local machine to your execution server.
```bash
# Clone the deployed script
git clone <your-internal-repo> /opt/etl/migration-spec-kit
cd /opt/etl/migration-spec-kit/04-target
```

### Step 3: Initial Full Load
Run the scripts manually in order to generate the initial seed data. Since this is a full load, parameters indicating \"start_date=1900-01-01\" or similar should be invoked.

```bash
python main.py --mode fulload
```

### Step 4: Validate
Run manual reconciliation queries on the target database, comparing aggregate totals with the SSIS systems. Fill in `reconciliation-report.md`.

### Step 5: Schedule the Job
Add an entry to `crontab` on your execution server to run the job at the same schedule as SSIS was running.
```bash
# Edit crontab
crontab -e
# Add the following entry to run every day at 2:00 AM UTC
0 2 * * * cd /opt/etl/migration-spec-kit/04-target && /usr/bin/python3 main.py >> /var/log/etl.log 2>&1
```

### Step 6: Parallel Run (recommended 1-2 weeks)
- Keep SSIS packages running in SQL Server Agent
- Compare source tables daily using validation queries against Python target runs
- Resolve discrepancies before determining Python scripts are production ready.

### Step 7: Cutover
- Disable SSIS packages in SQL Server Agent.
- Continue to monitor the Python job logs for the first 3 automated runs.

## Post-Migration

- [ ] SSIS packages disabled
- [ ] Python environment running on schedule smoothly without resource starvation
- [ ] Alerting checked (e.g. forced a fake error and verified email sent)
- [ ] Documentation updated
- [ ] Stakeholders notified
