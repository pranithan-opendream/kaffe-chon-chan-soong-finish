from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from app.domain.entity import entity

@entity
@dataclass
class Menu:
    id: int
    menu_name: str
    price: Decimal
    code: str
    description: str = None


