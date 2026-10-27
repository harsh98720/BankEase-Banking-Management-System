# Project Overview — BankEase

## Abstract
BankEase is a desktop banking-management prototype that demonstrates how a Python GUI can call Oracle PL/SQL procedures to maintain customer, account and transaction records. It offers a dashboard and forms for common classroom banking workflows.

## Objectives
1. Register customer details in a relational database.
2. Create Savings and Current accounts.
3. Process deposits, withdrawals and transfers through stored procedures.
4. Maintain a transaction ledger and provide a summary dashboard.
5. Demonstrate constraints, views, transaction handling and application/database integration.

## Architecture
Presentation layer: Tkinter desktop interface. Application layer: Python validation and Oracle driver. Database layer: Oracle tables, constraints, views and PL/SQL stored procedures.

## Database objects
- `CUSTOMERS`: customer profile details.
- `ACCOUNTS`: account type, balance and status.
- `TRANSACTIONS`: immutable-style event history for demo operations.
- `V_ACCOUNT_SUMMARY`: joins accounts to customer details.
- `V_TRANSACTION_HISTORY`: exposes transaction ledger fields.
- Procedures: `P_CREATE_CUSTOMER`, `P_OPEN_ACCOUNT`, `P_DEPOSIT`, `P_WITHDRAW`, `P_TRANSFER`, `P_CLOSE_ACCOUNT`.

## Scope and limitations
This project is for academic demonstration and does not implement production-grade identity verification, authentication/authorization, encryption policy, regulatory controls, or high-availability design. Use fictional demo data only.
