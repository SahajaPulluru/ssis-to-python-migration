# Contributing

Thanks for your interest in contributing to migration-spec-kit!

## How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature or fix: `git checkout -b feature/your-feature`
3. **Make your changes** following the structure and conventions below
4. **Test** your changes (especially DTSX examples and Python ETL code)
5. **Submit a Pull Request** with a clear description

## Structure Conventions

- Source files go in `01-source/` — never modify existing example files
- Analysis outputs go in `02-analysis/`
- Mapping docs go in `03-mapping/` — use Markdown tables
- Python ETL scripts go in `04-target/{extract|transform|load}/`
- Configurations (like `.env.example`) go in `04-target/config/`
- Validation queries go in `05-validation/`
- Skill files follow the Claude skill spec — see `skills/ssis-migration/SKILL.md`

## Naming Conventions

- Folders: `kebab-case`
- Python files: `snake_case.py`
- SQL files: `snake_case.sql` or `PascalCase.sql` for stored procedures
- DTSX files: `PascalCase.dtsx` (matching SSIS convention)

## Adding New SSIS Patterns

If you want to add a new SSIS component migration pattern:

1. Add an example DTSX in `01-source/dtsx/` demonstrating the pattern
2. Add the component mapping in `03-mapping/component-mapping.md`
3. Add a target Python script in the appropriate `04-target/` subfolder (`extract/`, `transform/`, or `load/`) showing the conversion
4. Update the skill's `SKILL.md` component mapping table if needed

## Code Quality

- Python scripts should have clear docstrings explaining the logic
- SQL should be formatted consistently (uppercase keywords)
- All Python scripts should implement standard libraries (like `pandas`, `sqlalchemy`, `pyodbc`, or `psycopg2`) where possible
- All Python extraction/transformation/load scripts should reference the original SSIS component they replace in comments
