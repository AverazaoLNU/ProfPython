# Bank Manager

Laboratory project for the course **"Professional Python"**
(Ivan Franko National University of Lviv).

Variant 4 — **bank accounts accounting system**. The project is developed
through all ten laboratory works: from a structured console application
(lab 1) to a tested, containerised REST service with CI/CD (lab 10).

## Features

- account model: client name, account number (`UA` + 8 digits), balance
- deposit and withdrawal; **the balance can never become negative**
- balance check and search of an account by number
- total amount of funds on all accounts
- search by several criteria (client name, balance range)
- sorting by client, number or balance
- statistics: average, minimum, maximum, low-balance accounts
- menu-driven interface with input validation and custom exceptions

## Requirements

Python 3.11+

## Installation

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

## Run

Interactive menu:

```bash
python -m bank_manager.main
# or
python -m bank_manager
# or console command
bank-manager
```

Non-interactive demonstration of all operations:

```bash
bank-manager --demo
```

Example output (fragment):

```text
All accounts:
  Number      Client                             Balance
  ------------------------------------------------------
  UA00000001  Olena Kovalenko              12 500.00 UAH
  UA00000002  Taras Melnyk                    850.50 UAH
  UA00000003  Iryna Bondar                 43 200.00 UAH

Withdraw 5 000.00 rejected: Insufficient funds on UA00000002: balance 350.00, requested 5000.00.

Total funds on all accounts: 63 350.75 UAH
```

## Project structure

```text
ProfPython/
├── pyproject.toml          # project metadata and build configuration
├── README.md
├── .gitignore
├── src/
│   └── bank_manager/
│       ├── __init__.py     # package marker, version
│       ├── __main__.py     # `python -m bank_manager`
│       ├── config.py       # configuration constants
│       ├── exceptions.py   # custom exceptions
│       ├── models.py       # data models (Account, BalanceStatistics)
│       ├── services.py     # business logic
│       ├── cli.py          # console input/output and menu
│       └── main.py         # application entry point
├── tests/                  # automated tests (lab 6)
└── _reports/               # laboratory reports
```

## Author

Student: Liubomyr Pylypchuk

Group: FEP-33
