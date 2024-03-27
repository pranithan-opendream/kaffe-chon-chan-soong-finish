
from abc import ABC, abstractmethod
from decimal import Decimal


class IMenuService(ABC):

    @abstractmethod
    def validate_code(self, code: str) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    def find_invalid_codes(self, codes: list[str]) -> set[str]:
        raise NotImplementedError
    
    @abstractmethod
    def get_price(self, code: str) -> Decimal:
        raise NotImplementedError
    
    @abstractmethod
    def get_prices(self, codes: list[str]) -> dict[str, Decimal]:
        raise NotImplementedError