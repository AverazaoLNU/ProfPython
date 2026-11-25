"""Custom exceptions of the bank manager application."""


class BankError(Exception):
    """Base class for all application errors."""


class InvalidAccountDataError(BankError):
    """Raised when account fields (number, client name, balance) are invalid."""


class InvalidAmountError(BankError):
    """Raised when an operation amount is not a positive number within limits."""


class InsufficientFundsError(BankError):
    """Raised when a withdrawal would make the balance negative."""


class AccountNotFoundError(BankError):
    """Raised when an account with the given number does not exist."""


class DuplicateAccountError(BankError):
    """Raised when an account with the same number already exists."""
