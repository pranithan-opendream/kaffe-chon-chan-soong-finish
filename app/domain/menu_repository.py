
from abc import ABC, abstractmethod

from .menu import Menu


class IMenuRepository(ABC):
    @abstractmethod
    def save(self, menu: Menu) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, menu_id) -> Menu:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code) -> Menu:
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_menu_name(self, name):
        raise NotImplementedError