# BankEase — Project Report Template

> Replace bracketed placeholders with your actual details and insert genuine screenshots from your own running application. Do not claim tests you did not perform.

## Cover Page
**Project Title:** BankEase — Banking Management System  
**Submitted by:** [Student name, roll number, section]  
**Programme / Semester:** [Programme and semester]  
**Subject:** [Subject name]  
**Submitted to:** [Faculty name]  
**Institution:** [University / college]  
**Academic session:** [Year]

## Certificate / Declaration
[Insert the institution's required certificate/declaration wording and signatures, if applicable.]

## Abstract
BankEase is an academic desktop banking prototype developed using Python Tkinter and Oracle Database. It supports customer registration, account opening, deposits, withdrawals, fund transfers and transaction history. PL/SQL procedures implement the core operations, while database constraints and views support data integrity and reporting.

## 1. Introduction
Describe the need for maintaining customer, account and transaction data in a structured system.

## 2. Objectives and Scope
List the objectives from `PROJECT_OVERVIEW.md` and state clearly that this is a classroom prototype, not a real banking platform.

## 3. Software and Hardware Requirements
Software: Windows, Python 3.13, Tkinter, Oracle Database XE, SQL Developer, `python-oracledb`, VS Code.  
Hardware: a typical Windows laptop/desktop with sufficient RAM and disk space for Oracle XE.

## 4. System Design
Explain the GUI, Python application logic, Oracle driver and database layer. Add your own architecture diagram if required.

## 5. Database Design
Describe `CUSTOMERS`, `ACCOUNTS`, `TRANSACTIONS`, the views and PL/SQL procedures. Include screenshots from SQL Developer.

## 6. Implementation
Explain customer registration, account opening, deposits, withdrawals, transfers, dashboard and history. Add code screenshots with captions and keep code readable.

## 7. Testing
Fill a table with your actual test results:

| Test case | Input | Expected result | Actual result | Status |
|---|---|---|---|---|
| Database connection | Valid local connection | App loads data | [Fill after test] | [Pass/Fail] |
| Register customer | Valid name | New customer ID returned | [Fill] | [Pass/Fail] |
| Deposit | Positive amount | Balance increases and transaction appears | [Fill] | [Pass/Fail] |
| Insufficient withdrawal | Amount above balance | Operation rejected | [Fill] | [Pass/Fail] |
| Transfer | Two active accounts | Source decreases, destination increases | [Fill] | [Pass/Fail] |

## 8. Screenshots
Insert actual screenshots: Dashboard, Customers, Accounts, Operations, Transaction History, SQL Developer verification. Add figure numbers and captions.

## 9. Limitations and Future Scope
Discuss authentication, role-based access, audit logging, stronger security, reporting/export, and deployment as future work.

## 10. Conclusion
Summarize what you implemented and tested, without overstating the scope.

## References
- Oracle Database SQL Language Reference and PL/SQL Language Reference.
- Python documentation: Tkinter and `python-oracledb` documentation.
