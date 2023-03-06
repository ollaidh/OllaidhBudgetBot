# interface for adapters

from typing import Protocol, Optional
from dataclasses import dataclass


@dataclass
class PurchaseInfo:
    name: str
    price: float
    category: str


class Adapter(Protocol):
    def add_purchase(self, purchase: PurchaseInfo) -> bool:
        ...

    def delete_purchase(self) -> bool:
        ...

    def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
        ...
