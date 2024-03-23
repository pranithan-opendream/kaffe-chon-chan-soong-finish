
from abc import ABC, abstractmethod

from .menu import Menu


class IMenuRepository(ABC):
    @abstractmethod
    def save(self, menu: Menu) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, menu_id: int) -> Menu:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code: str) -> Menu:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_codes(self, codes: list[str]) -> Menu:
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_menu_name(self, name: str):
        raise NotImplementedError