from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Order:
    id: int
    customer_name: str
    order_number: str
    date: datetime
    # TODO: make this to be user binding
    cashier_name: str
    items: list["OrderItem"]

    def list_items(self):
        return self.items

    def create(
        self,
        customer_name: str,
        order_number: str,
        date: datetime,
        cashier_name: str,
        items: list["OrderItem"],
    ):
        return self
    
    def dehydrate(
        self,
        id: int,
        customer_name: str,
        order_number: str,
        date: datetime,
        cashier_name: str,
        items: list["OrderItem"],
    ):
        return self


@dataclass
class OrderItem:
    item_id: int
    order_id: int
    menu_id: int
    quantity: int
    price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity
