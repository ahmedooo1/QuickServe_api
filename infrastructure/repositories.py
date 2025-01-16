from typing import List
from domain.models import User, Order

# InMemoryUserRepository
class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        self.users[user.user_id] = user
        return user

    def get_user_by_id(self, user_id: str) -> User:
        return self.users.get(user_id)

    def list_users(self) -> List[User]:
        return list(self.users.values())

    def update_user(self, user_id: str, user: User) -> User:
        if user_id in self.users:
            self.users[user_id] = user
            return user
        return None

    def delete_user(self, user_id: str) -> None:
        if user_id in self.users:
            del self.users[user_id]

# InMemoryOrderRepository
class InMemoryOrderRepository:
    def __init__(self):
        self.orders = {}

    def create_order(self, order: Order) -> Order:
        self.orders[order.order_id] = order
        return order

    def get_order_by_id(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def list_orders(self) -> List[Order]:
        return list(self.orders.values())

    def update_order(self, order_id: str, order: Order) -> Order:
        if order_id in self.orders:
            self.orders[order_id] = order
            return order
        return None

    def delete_order(self, order_id: str) -> None:
        if order_id in self.orders:
            del self.orders[order_id]
