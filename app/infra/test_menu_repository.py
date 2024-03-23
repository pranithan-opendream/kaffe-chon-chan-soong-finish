from decimal import Decimal
import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.infra.mapper import init_mapper
from app.infra.menu_repository import menu_table
from app.shared import get_id

init_mapper()

@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.infra.repository import metadata

    engine = create_engine("sqlite:///:memory:")
    # engine = create_engine("sqlite:///kaffe-chon-chan-soong.db")

    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    yield session
    session.close()


def test_save(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu = Menu(get_id(), "menu_name", Decimal("100"), "code")
    menu_repository = MenuRepository(session)
    menu_repository.save(menu)
    session.commit()

    saved_menu = session.execute(
        select(menu_table).where(menu_table.c.id == menu.id)
    ).first()

    assert saved_menu.id == menu.id
    assert saved_menu.menu_name == menu.menu_name
    assert saved_menu.price == menu.price
    assert saved_menu.code == menu.code

def test_find_by_id(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu = Menu(get_id(), "menu_name", Decimal("100"), "code")
    menu_repository = MenuRepository(session)
    menu_repository.save(menu)
    session.commit()

    found_menu = menu_repository.find_by_id(menu.id)

    assert found_menu.id == menu.id
    assert found_menu.menu_name == menu.menu_name
    assert found_menu.price == menu.price
    assert found_menu.code == menu.code

def test_find_by_id_not_found(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu = Menu(1, "menu_name", Decimal("100"), "code")
    menu_repository = MenuRepository(session)
    menu_repository.save(menu)
    session.commit()

    found_menu = menu_repository.find_by_id(2)
    assert found_menu is None

def test_find_by_code(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)
    menu1 = Menu(get_id(), "abc", Decimal("100"), "abc")
    menu_repository.save(menu1)
    menu2 = Menu(get_id(), "bcd", Decimal("100"), "bcd")
    menu_repository.save(menu2)
    menu3 = Menu(get_id(), "cde", Decimal("100"), "cde")
    menu_repository.save(menu3)

    session.commit()

    found_menu = menu_repository.find_by_code("abc")
    assert found_menu.id == menu1.id
    assert found_menu.menu_name == menu1.menu_name
    assert found_menu.price == menu1.price
    assert found_menu.code == menu1.code

def test_find_by_code_not_found(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)
    menu = Menu(get_id(), "abc", Decimal("100"), "abc")
    menu_repository.save(menu)
    session.commit()

    with pytest.raises(NoResultFound, ):
        menu_repository.find_by_code("xyz")
        pass

def test_find_by_codes(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)
    menu1 = Menu(get_id(), "abc", Decimal("100"), "abc")
    menu_repository.save(menu1)
    menu2 = Menu(get_id(), "bcd", Decimal("100"), "bcd")
    menu_repository.save(menu2)
    menu3 = Menu(get_id(), "cde", Decimal("100"), "cde")
    menu_repository.save(menu3)

    session.commit()

    found_menus = menu_repository.find_by_codes(["abc", "bcd"])
    assert len(found_menus) == 2
    assert found_menus[0].id == menu1.id
    assert found_menus[0].menu_name == menu1.menu_name
    assert found_menus[0].price == menu1.price
    assert found_menus[0].code == menu1.code
    assert found_menus[1].id == menu2.id
    assert found_menus[1].menu_name == menu2.menu_name
    assert found_menus[1].price == menu2.price
    assert found_menus[1].code == menu2.code

def test_find_by_menu_name(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)
    menu1 = Menu(get_id(), "abc", Decimal("100"), "abc")
    menu_repository.save(menu1)
    menu2 = Menu(get_id(), "bcd", Decimal("100"), "bcd")
    menu_repository.save(menu2)
    menu3 = Menu(get_id(), "cde", Decimal("100"), "cde")
    menu_repository.save(menu3)

    session.commit()

    found_menus = menu_repository.find_by_menu_name("bc")
    assert len(found_menus) == 2
    assert found_menus[0].id == menu1.id
    assert found_menus[0].menu_name == menu1.menu_name
    assert found_menus[0].price == menu1.price
    assert found_menus[0].code == menu1.code
    assert found_menus[1].id == menu2.id
    assert found_menus[1].menu_name == menu2.menu_name
    assert found_menus[1].price == menu2.price
    assert found_menus[1].code == menu2.code

def test_find_all(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)
    menu1 = Menu(get_id(), "abc", Decimal("100"), "abc")
    menu_repository.save(menu1)
    menu2 = Menu(get_id(), "bcd", Decimal("100"), "bcd")
    menu_repository.save(menu2)
    menu3 = Menu(get_id(), "cde", Decimal("100"), "cde")
    menu_repository.save(menu3)

    session.commit()

    found_menus = menu_repository.find_all()
    assert len(found_menus) == 3
    assert found_menus[0].id == menu1.id
    assert found_menus[0].menu_name == menu1.menu_name
    assert found_menus[0].price == menu1.price
    assert found_menus[0].code == menu1.code
    assert found_menus[1].id == menu2.id
    assert found_menus[1].menu_name == menu2.menu_name
    assert found_menus[1].price == menu2.price
    assert found_menus[1].code == menu2.code
    assert found_menus[2].id == menu3.id
    assert found_menus[2].menu_name == menu3.menu_name
    assert found_menus[2].price == menu3.price
    assert found_menus[2].code == menu3.code


def test_find_all_no_data_in_table(session):
    from app.domain.menu import Menu
    from app.infra.menu_repository import MenuRepository

    menu_repository = MenuRepository(session)

    session.commit()

    found_menus = menu_repository.find_all()
    assert len(found_menus) == 0