

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
    
    def find_invalid_codes(self, codes: list[str]) -> list[str]:
        
        return super().find_invalid_codes()