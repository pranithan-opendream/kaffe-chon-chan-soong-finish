from sqlalchemy.orm import mapper, relationship

from app.domain.menu import Menu
from app.domain.order import Order, OrderItem
from app.infra.repository import mapper_registry
from .menu_repository import menu_table
from .order_repository import order_table, order_item_table

is_mapper_initialized = False

def init_mapper():
    global is_mapper_initialized
    if not is_mapper_initialized:
        is_mapper_initialized = True
        mapper_registry.map_imperatively(
            Menu,
            menu_table,
        )

        mapper_registry.map_imperatively(
            OrderItem,
            order_item_table,
        )

        mapper_registry.map_imperatively(
            Order,
            order_table,
            properties={
                "_status": order_table.c.status,
                "_items": relationship(OrderItem, collection_class=list)
            }
        )
