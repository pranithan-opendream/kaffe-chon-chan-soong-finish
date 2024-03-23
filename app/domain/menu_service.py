
from abc import ABC, abstractmethod


class IMenuService(ABC):

    @abstractmethod
    def validate_code(self, code: str) -> bool:
        raise NotImplementedError
        
    @abstractmethod
    def find_invalid_codes(self, codes: list[str]) -> set[str]:
        raise NotImplementedError