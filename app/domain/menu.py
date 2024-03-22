from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Menu:
    id: int
    menu_name: str
    price: Decimal
    code: str
    description: str = None

    def __eq__(self, __value: "Menu") -> bool:
        if not isinstance(__value, Menu):
            return False
        return self.id == __value.id
    

