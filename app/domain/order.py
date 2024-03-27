from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domain.entity import entity
from app.domain.menu_service import IMenuService


class DomainOrderError(Exception):
    pass

@entity
@dataclass
class Order:
    id: int
    customer_name: str
    order_number: str
    date: datetime
    # TODO: make this to be user binding
    cashier_name: str
    
    menu_service: IMenuService = None

    _status: str = "pending"
    _items: list["OrderItem"] = field(default_factory=list)


    @property
    def status(self) -> str:
        return self._status

    @property
    def items(self) -> tuple["OrderItem"]:
        return tuple(self._items)

    def dehydrate_items(self, items: tuple["OrderItem"]) -> None:
        self._items = items

    def dehydrate_status(self, status: str) -> None:
        self._status = status

    def add_item(self, item: "OrderItem") -> None:
        menu_code = item.menu_code
        if not self.menu_service.validate_code(menu_code):
            raise DomainOrderError("Given menu_code is invalid")
        self._items = self._items + [item,]

    def add_items(self, items: list["OrderItem"]) -> None:
        invalid_menu_codes = self.menu_service.find_invalid_codes([i.menu_code for i in items])
        if invalid_menu_codes:
            raise DomainOrderError(f"Given menu_codes {invalid_menu_codes} is invalid")
        self._items = self._items + items

    def remove_item(self, item_id: int) -> None:
        if self.status == "paid":
            raise DomainOrderError("Cannot remove item from paid order")
        self._items = tuple([i for i in self.items if i.item_id != item_id])
    
    def serve(self) -> None:
        if self.status == "served":
            raise DomainOrderError("Order already served")
        self.dehydrate_status("served")
    
    def pay(self) -> None:
        if self.status != "served":
            raise DomainOrderError("Order must be served before payment")
        self.dehydrate_status("paid")

@entity(iden_field_name="item_id")
@dataclass
class OrderItem:
    item_id: int
    menu_code: str
    quantity: int
    price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity
