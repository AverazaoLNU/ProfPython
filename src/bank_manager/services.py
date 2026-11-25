"""Business logic: operations on bank accounts."""

from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from typing import Literal

from bank_manager.config import (
    LOW_BALANCE_THRESHOLD,
    MAX_OPERATION_AMOUNT,
    MIN_BALANCE,
)
from bank_manager.exceptions import (
    AccountNotFoundError,
    DuplicateAccountError,
    InsufficientFundsError,
    InvalidAmountError,
)
from bank_manager.models import Account, BalanceStatistics

SortKey = Literal["client", "number", "balance"]
CENT = Decimal("0.01")


def parse_amount(value: str | float | Decimal) -> Decimal:
    """Convert user input to a positive amount with two decimal places.

    Raises InvalidAmountError for non-numbers, zero, negative values,
    more than two decimal places or values above MAX_OPERATION_AMOUNT.
    """
    try:
        amount = Decimal(str(value).strip().replace(",", "."))
    except InvalidOperation as error:
        raise InvalidAmountError(f"{value!r} is not a number.") from error

    if not amount.is_finite():
        raise InvalidAmountError("Amount must be a finite number.")
    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than zero.")
    if amount != amount.quantize(CENT):
        raise InvalidAmountError("Amount must have at most two decimal places.")
    if amount > MAX_OPERATION_AMOUNT:
        raise InvalidAmountError(
            f"Amount must not exceed {MAX_OPERATION_AMOUNT}."
        )
    return amount.quantize(CENT)


def open_account(
    accounts: list[Account],
    client_name: str,
    number: str,
    initial_balance: Decimal = MIN_BALANCE,
) -> Account:
    """Create a new account and add it to the list."""
    account = Account(client_name, number, initial_balance)
    if any(existing.number == account.number for existing in accounts):
        raise DuplicateAccountError(f"Account {account.number} already exists.")
    accounts.append(account)
    return account


def find_account(accounts: Iterable[Account], number: str) -> Account:
    """Find an account by its number (case-insensitive)."""
    wanted = number.strip().upper()
    for account in accounts:
        if account.number == wanted:
            return account
    raise AccountNotFoundError(f"Account {wanted} not found.")


def get_balance(accounts: Iterable[Account], number: str) -> Decimal:
    """Return the balance of the account with the given number."""
    return find_account(accounts, number).balance


def deposit(account: Account, amount: Decimal) -> Decimal:
    """Add money to the account and return the new balance."""
    amount = parse_amount(amount)
    account.balance += amount
    return account.balance


def withdraw(account: Account, amount: Decimal) -> Decimal:
    """Take money from the account; the balance can never become negative."""
    amount = parse_amount(amount)
    if account.balance - amount < MIN_BALANCE:
        raise InsufficientFundsError(
            f"Insufficient funds on {account.number}: balance "
            f"{account.balance}, requested {amount}."
        )
    account.balance -= amount
    return account.balance


def calculate_total_balance(accounts: Iterable[Account]) -> Decimal:
    """Total amount of money on all accounts."""
    return sum((account.balance for account in accounts), MIN_BALANCE)


def search_accounts(
    accounts: Iterable[Account],
    client_name: str | None = None,
    min_balance: Decimal | None = None,
    max_balance: Decimal | None = None,
) -> list[Account]:
    """Search by several criteria; criteria set to None are ignored."""
    name_part = client_name.strip().lower() if client_name else None
    return [
        account
        for account in accounts
        if (name_part is None or name_part in account.client_name.lower())
        and (min_balance is None or account.balance >= min_balance)
        and (max_balance is None or account.balance <= max_balance)
    ]


def sort_accounts(
    accounts: Iterable[Account],
    key: SortKey = "balance",
    descending: bool = False,
) -> list[Account]:
    """Return a new list sorted by client name, number or balance."""
    if key == "client":
        return sorted(
            accounts,
            key=lambda account: account.client_name.lower(),
            reverse=descending,
        )
    if key == "number":
        return sorted(
            accounts, key=lambda account: account.number, reverse=descending
        )
    return sorted(
        accounts, key=lambda account: account.balance, reverse=descending
    )


def calculate_statistics(accounts: list[Account]) -> BalanceStatistics:
    """Count, total, average, min, max and number of low-balance accounts."""
    if not accounts:
        zero = MIN_BALANCE
        return BalanceStatistics(0, zero, zero, zero, zero, 0)

    balances = [account.balance for account in accounts]
    total = sum(balances, MIN_BALANCE)
    return BalanceStatistics(
        count=len(balances),
        total=total,
        average=(total / len(balances)).quantize(CENT),
        minimum=min(balances),
        maximum=max(balances),
        low_balance_count=sum(
            1 for balance in balances if balance < LOW_BALANCE_THRESHOLD
        ),
    )
