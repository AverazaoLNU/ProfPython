"""Application-wide configuration constants."""

from decimal import Decimal

CURRENCY: str = "UAH"

# The balance of an account can never drop below this value.
MIN_BALANCE: Decimal = Decimal("0.00")

# Account number format: "UA" followed by exactly 8 digits, e.g. UA00000001.
ACCOUNT_NUMBER_PREFIX: str = "UA"
ACCOUNT_NUMBER_DIGITS: int = 8

# Upper limit for a single deposit or withdrawal.
MAX_OPERATION_AMOUNT: Decimal = Decimal("1000000.00")

# Accounts whose balance is below this value are treated as "low balance".
LOW_BALANCE_THRESHOLD: Decimal = Decimal("1000.00")
