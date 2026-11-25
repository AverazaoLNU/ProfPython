"""Application entry point."""

import argparse
from decimal import Decimal

from bank_manager.cli import print_accounts, print_statistics, run_menu
from bank_manager.exceptions import BankError
from bank_manager.models import Account, format_money
from bank_manager.services import (
    calculate_statistics,
    calculate_total_balance,
    deposit,
    find_account,
    get_balance,
    search_accounts,
    sort_accounts,
    withdraw,
)


def create_demo_accounts() -> list[Account]:
    """Sample data used by the demo and as the initial state of the menu."""
    return [
        Account("Olena Kovalenko", "UA00000001", Decimal("12500.00")),
        Account("Taras Melnyk", "UA00000002", Decimal("850.50")),
        Account("Iryna Bondar", "UA00000003", Decimal("43200.00")),
        Account("Andrii Shevchenko", "UA00000004", Decimal("0.00")),
        Account("Oksana Melnyk", "UA00000005", Decimal("7300.75")),
    ]


def run_demo(accounts: list[Account]) -> None:
    """Non-interactive demonstration of every operation of variant 4."""
    print_accounts(accounts, "All accounts")

    account = find_account(accounts, "ua00000002")
    print(f"\nFound account: {account.number} - {account.client_name}")

    new_balance = deposit(account, Decimal(1500))
    print(f"Deposit 1 500.00 to {account.number}: {format_money(new_balance)}")

    new_balance = withdraw(account, Decimal("2000.50"))
    print(f"Withdraw 2 000.50 from {account.number}: {format_money(new_balance)}")

    try:
        withdraw(account, Decimal(5000))
    except BankError as error:
        print(f"Withdraw 5 000.00 rejected: {error}")

    balance = get_balance(accounts, "UA00000003")
    print(f"\nBalance of UA00000003: {format_money(balance)}")

    melnyks = search_accounts(accounts, client_name="melnyk")
    print_accounts(melnyks, "Search: client name contains 'melnyk'")

    rich = search_accounts(accounts, min_balance=Decimal(5000))
    print_accounts(rich, "Search: balance >= 5 000.00")

    by_balance = sort_accounts(accounts, key="balance", descending=True)
    print_accounts(by_balance, "Sorted by balance (descending)")

    total = calculate_total_balance(accounts)
    print(f"\nTotal funds on all accounts: {format_money(total)}")
    print_statistics(calculate_statistics(accounts))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="bank-manager",
        description="Bank accounts accounting system (Professional Python, lab 1).",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="run a non-interactive demonstration instead of the menu",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    accounts = create_demo_accounts()
    if args.demo:
        run_demo(accounts)
    else:
        run_menu(accounts)


if __name__ == "__main__":
    main()
