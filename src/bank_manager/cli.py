"""Console input/output: validated input helpers, tables and the menu."""

from collections.abc import Callable
from decimal import Decimal
from typing import TypeVar

from bank_manager.config import CURRENCY
from bank_manager.exceptions import (
    BankError,
    DuplicateAccountError,
    InvalidAccountDataError,
)
from bank_manager.models import (
    Account,
    BalanceStatistics,
    format_money,
    is_valid_account_number,
)
from bank_manager.services import (
    SortKey,
    calculate_statistics,
    calculate_total_balance,
    deposit,
    find_account,
    open_account,
    parse_amount,
    search_accounts,
    sort_accounts,
    withdraw,
)

T = TypeVar("T")

MENU_ITEMS: dict[str, str] = {
    "1": "Show all accounts",
    "2": "Open new account",
    "3": "Deposit",
    "4": "Withdraw",
    "5": "Check balance",
    "6": "Search accounts",
    "7": "Sort accounts",
    "8": "Total funds and statistics",
    "0": "Exit",
}

SORT_KEYS: dict[str, SortKey] = {"1": "client", "2": "number", "3": "balance"}


def prompt_text(message: str, allow_empty: bool = False) -> str:
    """Ask for a line of text until a non-empty value is entered."""
    while True:
        value = input(message).strip()
        if value or allow_empty:
            return value
        print("  Value must not be empty.")


def prompt_valid(message: str, convert: Callable[[str], T]) -> T:
    """Ask until `convert` accepts the input; BankError means invalid input."""
    while True:
        raw = input(message)
        try:
            return convert(raw)
        except BankError as error:
            print(f"  Error: {error}")


def prompt_amount(message: str) -> Decimal:
    """Ask for a positive amount of money."""
    return prompt_valid(message, parse_amount)


def prompt_optional_amount(message: str) -> Decimal | None:
    """Ask for an amount; an empty line means 'no value'."""
    return prompt_valid(
        message, lambda raw: parse_amount(raw) if raw.strip() else None
    )


def print_accounts(accounts: list[Account], title: str = "Accounts") -> None:
    """Print accounts as a table."""
    print(f"\n{title}:")
    if not accounts:
        print("  (no accounts)")
        return
    print(f"  {'Number':<12}{'Client':<24}{'Balance':>18}")
    print("  " + "-" * 54)
    for account in accounts:
        print(
            f"  {account.number:<12}{account.client_name:<24}"
            f"{account.formatted_balance:>18}"
        )


def print_statistics(stats: BalanceStatistics) -> None:
    """Print aggregated statistics."""
    print("\nStatistics:")
    print(f"  Accounts:             {stats.count}")
    print(f"  Total funds:          {format_money(stats.total)}")
    print(f"  Average balance:      {format_money(stats.average)}")
    print(f"  Minimum balance:      {format_money(stats.minimum)}")
    print(f"  Maximum balance:      {format_money(stats.maximum)}")
    print(f"  Low-balance accounts: {stats.low_balance_count}")


def print_menu() -> None:
    """Print the list of commands."""
    print("\n=== Bank Manager ===")
    for key, title in MENU_ITEMS.items():
        print(f"{key}. {title}")


def handle_open(accounts: list[Account]) -> None:
    client = prompt_text("Client name: ")

    def convert_number(raw: str) -> str:
        number = raw.strip().upper()
        if not is_valid_account_number(number):
            raise InvalidAccountDataError(
                "Expected UA + 8 digits, e.g. UA00000010."
            )
        if any(account.number == number for account in accounts):
            raise DuplicateAccountError(f"Account {number} already exists.")
        return number

    number = prompt_valid("Account number (UA + 8 digits): ", convert_number)
    balance = prompt_valid(
        f"Initial balance, {CURRENCY} (empty = 0): ",
        lambda raw: parse_amount(raw) if raw.strip() else Decimal(0),
    )
    account = open_account(accounts, client, number, balance)
    print(f"Account {account.number} opened for {account.client_name}.")


def handle_deposit(accounts: list[Account]) -> None:
    account = find_account(accounts, prompt_text("Account number: "))
    new_balance = deposit(account, prompt_amount(f"Amount, {CURRENCY}: "))
    print(f"Deposited. New balance: {format_money(new_balance)}")


def handle_withdraw(accounts: list[Account]) -> None:
    account = find_account(accounts, prompt_text("Account number: "))
    new_balance = withdraw(account, prompt_amount(f"Amount, {CURRENCY}: "))
    print(f"Withdrawn. New balance: {format_money(new_balance)}")


def handle_balance(accounts: list[Account]) -> None:
    account = find_account(accounts, prompt_text("Account number: "))
    print(
        f"{account.number} ({account.client_name}): "
        f"{account.formatted_balance}"
    )


def handle_search(accounts: list[Account]) -> None:
    print("Leave a field empty to skip the criterion.")
    client = prompt_text("Client name contains: ", allow_empty=True)
    min_balance = prompt_optional_amount("Min balance: ")
    max_balance = prompt_optional_amount("Max balance: ")
    result = search_accounts(accounts, client or None, min_balance, max_balance)
    print_accounts(result, f"Found {len(result)} account(s)")


def handle_sort(accounts: list[Account]) -> None:
    print("Sort by: 1 - client, 2 - number, 3 - balance")
    key = SORT_KEYS.get(prompt_text("Choice: "), "balance")
    descending = prompt_text("Descending? (y/n): ").lower().startswith("y")
    result = sort_accounts(accounts, key, descending)
    print_accounts(result, f"Sorted by {key}")


def handle_statistics(accounts: list[Account]) -> None:
    total = calculate_total_balance(accounts)
    print(f"\nTotal funds on all accounts: {format_money(total)}")
    print_statistics(calculate_statistics(accounts))


HANDLERS: dict[str, Callable[[list[Account]], None]] = {
    "1": lambda accounts: print_accounts(accounts),
    "2": handle_open,
    "3": handle_deposit,
    "4": handle_withdraw,
    "5": handle_balance,
    "6": handle_search,
    "7": handle_sort,
    "8": handle_statistics,
}


def run_menu(accounts: list[Account]) -> None:
    """Menu-driven interface; business errors are shown, not raised."""
    while True:
        print_menu()
        command = input("Select command: ").strip()
        if command == "0":
            print("Goodbye.")
            return
        handler = HANDLERS.get(command)
        if handler is None:
            print("Unknown command.")
            continue
        try:
            handler(accounts)
        except BankError as error:
            print(f"Error: {error}")
