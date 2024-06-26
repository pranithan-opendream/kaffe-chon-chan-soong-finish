

from decimal import Decimal
from app.domain.menu_repository import IMenuRepository
from app.domain.menu_service import IMenuService
from sqlalchemy.exc import NoResultFound

class MenuService(IMenuService):
    def __init__(self, repository: IMenuRepository):
        self.repo = repository

    def validate_code(self, code: str) -> bool:
        try:
            self.repo.find_by_code(code)
            return True
        except NoResultFound:
            return False
    
    def find_invalid_codes(self, codes: list[str]) -> set[str]:
        valid_menus = self.repo.find_by_codes(codes)
        # all_codes - valid_codes
        invalid_codes = set(codes) - set([m.code for m in valid_menus])
        return invalid_codes
    
    def get_price(self, code: str) -> Decimal:
        menu = self.repo.find_by_code(code)
        return menu.price
    
    def get_prices(self, codes: list[str]) -> dict[str, Decimal]:
        menus = self.repo.find_by_codes(codes)
        return {m.code: m.price for m in menus}