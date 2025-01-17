from abc import ABC, abstractmethod
from typing import List
from domain.models import User, Order

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: str, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_order_by_id(self, id: int) -> Order:
        pass

    @abstractmethod
    def list_orders(self) -> List[Order]:
        pass
