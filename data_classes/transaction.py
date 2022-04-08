from dataclasses import dataclass
from enum import Enum, auto

class TransactionAction(Enum):
    # for liquidity providers
    DEPOSIT = auto()
    WITHDRAW = auto()

    # for purchasers
    PURCHASE = auto()
    EXERCISE = auto()
    REJECT = auto()

@dataclass
class Transaction:
    date: str
    action: TransactionAction
    value: float
