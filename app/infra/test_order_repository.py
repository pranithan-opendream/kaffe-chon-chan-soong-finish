from datetime import datetime
from decimal import Decimal
import pytest
from sqlalchemy import select
from app.domain.order import OrderItem
from app.infra.mapper import init_mapper
from app.shared import get_id
from app.infra.order_repository import order_table

@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.infra.repository import metadata

    engine = create_engine("sqlite:///:memory:")
    # engine = create_engine("sqlite:///kaffe-chon-chan-soong.db")

    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    init_mapper()

    session = Session()
    yield session
    session.close()

def test_create_order(session):
    from app.domain.order import Order
    from app.infra.order_repository import OrderRepository

    now = datetime.now()

    order = Order(
        get_id(),
        "customer",
        now,
        "cashier",
        _items=[
            OrderItem(get_id(), "menu_a", 2, Decimal("250")),
            OrderItem(get_id(), "menu_b", 1, Decimal("200")),
            OrderItem(get_id(), "menu_c", 1, Decimal("200")),
        ]
    )
    order_repository = OrderRepository(session)
    order_repository.save(order)
    session.commit()

    saved_order: Order = session.scalars(
        select(Order).where(order_table.c.id == order.id)
    ).first()

    assert saved_order.id == order.id
    assert saved_order.customer_name == order.customer_name
    assert saved_order.order_number == order.order_number
    assert saved_order.date == order.date
    assert saved_order.cashier_name == order.cashier_name
    assert len(saved_order.items) == 3

def test_update_order(session):
    from app.domain.order import Order
    from app.infra.order_repository import OrderRepository

    now = datetime.now()

    order = Order(
        get_id(),
        customer_name="customer",
        date=now,
        cashier_name="cashier",
        _items=[
            OrderItem(get_id(), "menu_a", 2, Decimal("250")),
        ]
    )
    order_repository = OrderRepository(session)
    order_repository.save(order)
    session.commit()

    updated_order: Order = session.scalars(
        select(Order).where(order_table.c.id == order.id)
    ).first()
    updated_order.customer_name = "updated_customer"
    updated_order.cashier_name = "updated_cashier"
    updated_order._status = "paid"
    updated_order._items.append(OrderItem(get_id(), "menu_d", 1, Decimal("150")))

    order_repository.save(updated_order)

    saved_order: Order = session.scalars(
        select(Order).where(order_table.c.id == updated_order.id)
    ).first()

    assert saved_order.id == updated_order.id
    assert saved_order.customer_name == updated_order.customer_name
    assert saved_order.cashier_name == updated_order.cashier_name
    assert saved_order.status == updated_order.status
    assert len(saved_order.items) == 2

def test_find_by_id(session):
    from app.domain.order import Order
    from app.infra.order_repository import OrderRepository

    now = datetime.now()

    order = Order(
        get_id(),
        customer_name="customer",
        date=now,
        cashier_name="cashier",
        _items=[
            OrderItem(get_id(), "menu_a", 2, Decimal("250")),
        ]
    )
    order_repository = OrderRepository(session)
    order_repository.save(order)
    session.commit()

    found_order = order_repository.find_by_id(order.id)

    assert found_order.id == order.id
    assert found_order.customer_name == order.customer_name
    assert found_order.order_number == order.order_number
    assert found_order.date == order.date
    assert found_order.cashier_name == order.cashier_name
    assert len(found_order.items) == 1