"""Data models of the bank manager application."""

from dataclasses import dataclass
from decimal import Decimal

from bank_manager.config import (
    ACCOUNT_NUMBER_DIGITS,
    ACCOUNT_NUMBER_PREFIX,
    CURRENCY,
    MIN_BALANCE,
)
from bank_manager.exceptions import InvalidAccountDataError


def is_valid_account_number(number: str) -> bool:
    """Check the format UA + 8 digits, e.g. UA00000001."""
    prefix_length = len(ACCOUNT_NUMBER_PREFIX)
    digits = number[prefix_length:]
    return (
        number.startswith(ACCOUNT_NUMBER_PREFIX)
        and len(digits) == ACCOUNT_NUMBER_DIGITS
        and digits.isdigit()
    )


@dataclass
class Account:
    """Bank account: client name, account number and balance."""

    client_name: str
    number: str
    balance: Decimal = MIN_BALANCE

    def __post_init__(self) -> None:
        self.client_name = self.client_name.strip()
        self.number = self.number.strip().upper()
        self.balance = Decimal(self.balance).quantize(Decimal("0.01"))

        if not self.client_name:
            raise InvalidAccountDataError("Client name must not be empty.")
        if not is_valid_account_number(self.number):
            raise InvalidAccountDataError(
                f"Invalid account number {self.number!r}: expected "
                f"{ACCOUNT_NUMBER_PREFIX} + {ACCOUNT_NUMBER_DIGITS} digits."
            )
        if self.balance < MIN_BALANCE:
            raise InvalidAccountDataError("Balance must not be negative.")

    @property
    def formatted_balance(self) -> str:
        """Balance with thousands separator and currency, e.g. 12 500.00 UAH."""
        return format_money(self.balance)


@dataclass(frozen=True)
class BalanceStatistics:
    """Aggregated statistics over a collection of accounts."""

    count: int
    total: Decimal
    average: Decimal
    minimum: Decimal
    maximum: Decimal
    low_balance_count: int


def format_money(amount: Decimal) -> str:
    """Format an amount as '12 500.00 UAH'."""
    return f"{amount:,.2f}".replace(",", " ") + f" {CURRENCY}"
