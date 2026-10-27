# BankEase — Banking Management System

A college demonstration project built with Python, Tkinter, Oracle Database XE, SQL and PL/SQL. The application supports customer registration, account opening, deposits, withdrawals, transfers and transaction history.

## Technology stack
- Python 3.13 recommended (standard Windows CPython build)
- Tkinter (included with standard Python on Windows)
- `python-oracledb` Python driver
- Oracle Database XE with PDB service `XEPDB1`
- Oracle PL/SQL stored procedures, views, constraints and indexes

## Important safety note
This is an academic demo, not production banking software. Use only fictional data. The reset script is destructive to the BankEase tables and views in the `BANK_USER` schema. Never run it as `SYSTEM` or against a database containing real data.

## Fresh setup in SQL Developer
1. Start Oracle Database XE and open SQL Developer.
2. Connect to service `XEPDB1`. If the user does not exist, open a `SYSTEM` connection to **XEPDB1** and run `sql/00_create_user.sql` once. If you already have `BANK_USER`, do not rerun the create-user script.
3. Connect using username `BANK_USER`, password `BankEase@123`, hostname `localhost`, port `1521`, service name `XEPDB1`.
4. For a clean reinstall, run `sql/00_reset_schema.sql` in a worksheet connected as `BANK_USER`. This removes the project's old tables/views and data. Skip it if you need to keep existing data.
5. Run scripts in order, connected as `BANK_USER`: `01_schema.sql`, `02_plsql_programs.sql`, `03_sample_data.sql`, `04_verify.sql`. Open each file and press **F5 (Run Script)**. Run sample data only once after a fresh schema.
6. In `04_verify.sql`, check that tables/views exist, procedures are `VALID`, and demo rows are present.

## Python setup
From the project root in VS Code PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Edit `app/db_config.py` if your local Oracle username, password, host, port or service name differs. For a local database, defaults are `bank_user`, `BankEase@123`, `localhost`, `1521`, `XEPDB1`. Keep the password private.

Run the app from the project root:

```powershell
python app\main.py
```

## App features
- Premium dark dashboard with live counts, active balance and recent transactions
- Customer registration with basic validation
- Account directory and account opening (Savings/Current)
- Deposit, withdrawal and inter-account transfer using PL/SQL procedures
- Transaction ledger and refresh actions
- Oracle views for account summary and transaction history

## Demo data
Aanya Sharma (Savings ₹12,500) and Rohan Verma (Current ₹8,000) are fictional seed records. After you perform operations, balances and transaction history will change.

## Troubleshooting
- `DPY-6001 Service ... not registered`: confirm service name `XEPDB1` in `app/db_config.py` and SQL Developer connection.
- `DPY-6005 cannot connect`: ensure Oracle listener/database services are running and host/port are correct.
- `ORA-00001` while running sample data: it has probably already been inserted; do not rerun it unless you reset the schema first.
- Python package installation errors on a nonstandard Python build: use standard 64-bit Windows Python 3.13 and recreate `.venv`.

## Suggested submission evidence
Capture screenshots of: dashboard, customer list, account list, successful deposit, successful transfer, transaction history, and SQL Developer verification query. Add these to your report with figure captions.
