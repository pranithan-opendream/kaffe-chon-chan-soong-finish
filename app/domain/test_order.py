
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from app.domain.menu_service import IMenuService
from app.domain.order import DomainOrderError, Order, OrderItem
from app.shared import get_id


class MockMenuService(IMenuService):
    def validate_code(self, code: str) -> bool:
        pass
        
    def find_invalid_codes(self, codes: list[str]) -> set[str]:
        pass

def test_init_order():
    now = datetime.now()
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=MockMenuService())
    assert order.id
    assert order.customer_name == "Foo"
    assert order.date == now
    assert order.cashier_name == "John Doe"
    assert order.status == "pending"
    assert order.items == ()

def test_dehydrate_items():
    now = datetime.now()
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=MockMenuService())
    items = (
        OrderItem(item_id=1, menu_code="menu_a", quantity=2, price=Decimal("25000")),
        OrderItem(item_id=2, menu_code="menu_b", quantity=1, price=Decimal("20000")),
    )
    order.dehydrate_items(items)
    assert order.items == items

def test_dehydrate_status():
    now = datetime.now()
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=MockMenuService())
    order.dehydrate_status("completed")
    assert order.status == "completed"

def test_add_item():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item1 = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item1)

    item2 = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("250"))
    order.add_item(item2)

    item3 = OrderItem(item_id=get_id(), menu_code="menu_b", quantity=2, price=Decimal("25000"))
    order.add_item(item3)

    assert order.items == (item1, item2, item3)

def test_add_item_with_invalid_code():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(side_effect=lambda x: x != "menu_c")
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item1 = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item1)

    item2 = OrderItem(item_id=get_id(), menu_code="menu_c", quantity=2, price=Decimal("250"))
    try:
        order.add_item(item2)
    except Exception as e:
        assert str(e) == "Given menu_code is invalid"

def test_add_items():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.find_invalid_codes = MagicMock(return_value=set())
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    items = [
        OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25")),
        OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("250")),
        OrderItem(item_id=get_id(), menu_code="menu_b", quantity=2, price=Decimal("25000")),
    ]
    order.add_items(items)
    assert order.items == tuple(items)

def test_add_items_with_invalid_code():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.find_invalid_codes = MagicMock(return_value={"menu_c"})
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    items = [
        OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25")),
        OrderItem(item_id=get_id(), menu_code="menu_c", quantity=2, price=Decimal("250")),
        OrderItem(item_id=get_id(), menu_code="menu_b", quantity=2, price=Decimal("25000")),
    ]
    try:
        order.add_items(items)
    except Exception as e:
        assert str(e) == "Given menu_codes {'menu_c'} is invalid"

def test_remove_item():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.find_invalid_codes = MagicMock(return_value=set())
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    items = [
        OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25")),
        OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("250")),
        OrderItem(item_id=get_id(), menu_code="menu_b", quantity=2, price=Decimal("25000")),
    ]
    order.add_items(items)
    order.remove_item(items[0].item_id)
    assert order.items == (items[1], items[2])

def test_remove_item_from_paid_order():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item)
    order.dehydrate_status("paid")
    with pytest.raises(DomainOrderError, match="Cannot remove item from paid order"):
        order.remove_item(item.item_id)

def test_serve():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item)
    order.serve()
    assert order.status == "served"

def test_serve_with_already_served():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item)
    order.dehydrate_status("served")
    with pytest.raises(DomainOrderError, match="Order already served"):
        order.serve()

def test_pay():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item)
    order.serve()
    order.pay()
    assert order.status == "paid"

def test_pay_without_serving():
    now = datetime.now()
    mock_menu_service = MockMenuService()
    mock_menu_service.validate_code = MagicMock(return_value=True)
    order = Order(
        id=get_id(),
        customer_name="Foo",
        order_number="123",
        date=now,
        cashier_name="John Doe",
        menu_service=mock_menu_service)
    item = OrderItem(item_id=get_id(), menu_code="menu_a", quantity=2, price=Decimal("25"))
    order.add_item(item)
    
    with pytest.raises(DomainOrderError, match="Order must be served before payment"):
        order.pay()