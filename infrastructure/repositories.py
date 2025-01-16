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
from sqlalchemy.orm import Session
from domain.models import Order

class OrderRepository:
    def list_orders(self, db: Session) -> List[Order]:
        return db.query(Order).all()  # Ou la logique de récupération des commandes

    def get_order_by_id(self, order_id: str, db: Session) -> Order:
        return db.query(Order).filter(Order.order_id == order_id).first()