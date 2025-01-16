from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from infrastructure.db import get_order_db, get_user_db
from application.dto import OrderDTO
from domain.models import Order, User
from infrastructure.repositories import OrderRepository

router = APIRouter()

# Repositories
order_repository = OrderRepository()

# Créer une nouvelle commande
@router.post("/orders", response_model=OrderDTO)
def create_order(order: OrderDTO, user_db: Session = Depends(get_user_db), order_db: Session = Depends(get_order_db)):
    # Vérifier si l'utilisateur existe dans la base de données des utilisateurs
    user = user_db.query(User).filter(User.id == order.user_id).first()  # Utilise user_db pour interroger la base de données des utilisateurs
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Créer la commande dans la base de données des commandes
    new_order = Order(order_id=order.order_id, user_id=order.user_id, details=order.details)
    order_db.add(new_order)  # Utilise order_db pour ajouter la commande dans la base de données des commandes
    order_db.commit()
    order_db.refresh(new_order)

    return new_order


# Récupérer une commande par ID
@router.get("/orders/{order_id}", response_model=OrderDTO)
def get_order(order_id: str, db: Session = Depends(get_order_db)):
    order = order_repository.get_order_by_id(order_id, db)  # Appel à la méthode get_order_by_id du repository avec la session de la base de données
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Lister toutes les commandes
@router.get("/orders", response_model=List[OrderDTO])
def list_orders(db: Session = Depends(get_order_db)):
    return order_repository.list_orders(db)  # Appel à la méthode list_orders du repository avec la session de la base de données
