from typing import List, Optional
from models import User

class InMemoryUserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        self.users[user.user_id] = user
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def update_user(self, user_id: str, user: User) -> User:
        self.users[user_id] = user
        return user

    def delete_user(self, user_id: str) -> None:
        if user_id in self.users:
            del self.users[user_id]

    def list_users(self) -> List[User]:
        return list(self.users.values())