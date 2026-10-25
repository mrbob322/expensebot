from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Expense:
    id: int
    amount: Decimal
    category: str
    comment: Optional[str]
    date: date
