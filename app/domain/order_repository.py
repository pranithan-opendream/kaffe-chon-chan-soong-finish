

from abc import ABC, abstractmethod

from app.domain.order import Order


class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, order_id: int) -> Order:
        raise NotImplementedError
    