from sqlalchemy import Column, ForeignKey, Integer, Numeric, Sequence, String, Table, DateTime, func
from app.domain.order import Order
from app.domain.order_repository import IOrderRepository
from sqlalchemy.orm import Session, composite
from .repository import metadata


order_table = Table(
    "order",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_name', String),
    Column('order_number', String),
    Column('date', DateTime),
    Column('cashier_name', String),
    Column('status', String),
)

order_item_table = Table(
    "order_item",
    metadata,
    Column('item_id', Integer, primary_key=True),
    Column('menu_code', String),
    Column('quantity', Integer),
    Column('order_id', Integer, ForeignKey("order.id")),
    Column('price', Numeric),
    Column('remark', String),
)

class OrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> None:
        self.session.add(order)

    def find_by_id(self, order_id: int) -> Order:
        return self.session.get(Order, order_id)