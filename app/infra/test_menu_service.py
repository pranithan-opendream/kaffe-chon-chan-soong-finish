
from decimal import Decimal
from unittest.mock import MagicMock
import pytest

from app.domain.menu import Menu
from app.domain.menu_repository import IMenuRepository
from app.infra.menu_service import MenuService
from sqlalchemy.exc import NoResultFound

class MockMenuRepository(IMenuRepository):
    def save(self, menu: Menu) -> None:
        pass

    def find_by_id(self, menu_id: int) -> Menu:
        pass

    def find_by_code(self, code: str) -> Menu:
        pass

    def find_by_codes(self, codes: list[str]) -> list[Menu]:
        pass

    def find_all(self) -> list[Menu]:
        pass

    def find_by_menu_name(self, name: str) -> list[Menu]:
        pass
    

@pytest.fixture
def menu_repository() -> IMenuRepository:
    return MockMenuRepository()

def test_validate_code(menu_repository):
    service = MenuService(menu_repository)
    service.repo.find_by_code = MagicMock(return_value=Menu(2, "test menu name", Decimal("123.25"), "TMN-001", "test menu name that is very awesome ingredients"))
    assert service.validate_code("TMN-001") == True
    
def test_validate_code_not_found(menu_repository):
    service = MenuService(menu_repository)
    def side_effect(code):
        raise NoResultFound
    service.repo.find_by_code = MagicMock(side_effect=side_effect)
    
def test_find_invalid_codes(menu_repository):
    service = MenuService(menu_repository)
    service.repo.find_by_codes = MagicMock(return_value=[
        Menu(1, "menu 1", Decimal("100"), "abc"),
        Menu(2, "menu 2", Decimal("100"), "bcd"),
        Menu(3, "menu 3", Decimal("100"), "mno"),
    ])

    invalid_codes = service.find_invalid_codes(["abc", "bcd", "wxy", "xyz"])
    assert invalid_codes == {"wxy", "xyz"}

def test_find_invalid_codes_empty_list_input(menu_repository):
    service = MenuService(menu_repository)
    service.repo.find_by_codes = MagicMock(return_value=[])
    invalid_codes = service.find_invalid_codes([])
    assert len(invalid_codes) == 0


def test_find_invalid_codes_not_found_any_code(menu_repository):
    service = MenuService(menu_repository)
    service.repo.find_by_codes = MagicMock(return_value=[])
    invalid_codes = service.find_invalid_codes(["abc", "bcd", "wxy", "xyz"])
    assert invalid_codes == {"abc", "bcd", "wxy", "xyz"}