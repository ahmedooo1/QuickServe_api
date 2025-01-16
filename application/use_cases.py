from infrastructure.repositories import UserRepository, OrderRepository
from infrastructure.db import SessionLocal
from application.dto import UserDTO, OrderDTO
from sqlalchemy.orm import Session

# Obtenir une session de base de données
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer un utilisateur
def create_user_service(user: UserDTO, db: Session):
    user_repository = UserRepository(db)
    return user_repository.create_user(user)

# Créer une commande
def create_order_service(order: OrderDTO, db: Session):
    order_repository = OrderRepository(db)
    return order_repository.create_order(order)
