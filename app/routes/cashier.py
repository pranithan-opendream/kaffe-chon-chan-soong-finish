from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union
from fastapi import APIRouter, Depends
from starlette.responses import Response
from app.database import get_db
from app.domain.menu import Menu
from app.domain.order import Order, OrderItem
from app.infra.menu_repository import MenuRepository
from sqlalchemy.orm import Session

from app.infra.menu_service import MenuService
from app.infra.order_repository import OrderRepository
from app.shared import get_id

router = APIRouter(prefix="/cashier", tags=["cashier"])

# TODO: Error handling

# region Menu
@dataclass
class EditMenuDTO:
    menu_name: str
    price: Decimal
    code: str
    description: Optional[str] = None

@dataclass
class MenuDTO:
    id: str
    menu_name: str
    price: Decimal
    code: str
    description: Optional[str] = None

@router.post("/menu/")
def add_menu(new_menu: EditMenuDTO, db: Session = Depends(get_db)) -> "MenuDTO":
    # TODO: repository injection
    menu = Menu(
        get_id(),
        menu_name=new_menu.menu_name,
        price=new_menu.price,
        code=new_menu.code,
        description=new_menu.description,
    )
    MenuRepository(db).save(menu)
    db.commit()
    new_menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return new_menu

@router.put("/menu/{id}")
def update_menu(id: str, updated_menu: EditMenuDTO, db: Session = Depends(get_db)) -> "MenuDTO":
    menu = MenuRepository(db).find_by_id(int(id))
    menu.menu_name = updated_menu.menu_name
    menu.price = updated_menu.price
    menu.code = updated_menu.code
    menu.description = updated_menu.description
    MenuRepository(db).save(menu)
    db.commit()
    updated_menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return updated_menu

@router.get("/menu/{id}")
def get_menu(id: str, db: Session = Depends(get_db)) -> MenuDTO:
    menu = MenuRepository(db).find_by_id(int(id))
    menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return menu

@router.get("/menu/by-code/{code}")
def get_menu_by_code(code: str, db: Session = Depends(get_db)) -> MenuDTO:
    menu = MenuRepository(db).find_by_code(code)
    menu = MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    return menu


@router.get("/menu/by-name/{name}")
def get_menu_by_name(name: str, db: Session = Depends(get_db)) -> list[MenuDTO]:
    menus = MenuRepository(db).find_by_menu_name(name)
    return [MenuDTO(
        id=str(menu.id),
        menu_name=menu.menu_name,
        price=menu.price,
        code=menu.code,
        description=menu.description,
    )
    for menu in menus]

# endregion

# region Order

@dataclass
class OrderItemDTO:
    menu_code: str
    quantity: int
    remark: Optional[str] = None

@dataclass
class CreateOrderDTO:
    customer_name: str
    cashier_name: str
    items: list[OrderItemDTO]

@dataclass
class OrderDTO:
    id: str
    customer_name: str
    date: datetime
    cashier_name: str
    status: str
    items: list[OrderItemDTO]

def convert_order_to_dto(order: Order) -> OrderDTO:
    return OrderDTO(
        id=str(order.id),
        customer_name=order.customer_name,
        date=order.date,
        cashier_name=order.cashier_name,
        status=order.status,
        items=[
            OrderItemDTO(
                menu_code=item.menu_code,
                quantity=item.quantity,
                remark=item.remark,
            )
            for item in order.items
        ]
    )

@router.post("/order/")
def add_order(new_order: CreateOrderDTO, db: Session = Depends(get_db)) -> OrderDTO:
    order = Order(
        get_id(),
        customer_name=new_order.customer_name,
        date=datetime.now(),
        cashier_name=new_order.cashier_name,
        menu_service=MenuService(MenuRepository(db)),
    )
    order.add_items(
        [
            OrderItem(
                item_id=get_id(),
                menu_code=item.menu_code,
                quantity=item.quantity,
                remark=item.remark,
            )
            for item in new_order.items
        ]
    )
    OrderRepository(db).save(order)
    db.commit()
    return convert_order_to_dto(order)

@router.get("/order/{id}")
def get_order(id: str, db: Session = Depends(get_db)) -> OrderDTO:
    order = OrderRepository(db).find_by_id(int(id))
    return convert_order_to_dto(order)

@router.put("/order/{id}/serve")
def serve_order(id: str, db: Session = Depends(get_db)) -> OrderDTO:
    order = OrderRepository(db).find_by_id(int(id))
    order.serve()
    OrderRepository(db).save(order)
    db.commit()
    return convert_order_to_dto(order)

@router.put("/order/{id}/pay")
def pay_order(id: str, db: Session = Depends(get_db)) -> OrderDTO:
    order = OrderRepository(db).find_by_id(int(id))
    order.pay()
    OrderRepository(db).save(order)
    db.commit()
    return convert_order_to_dto(order)

# endregion