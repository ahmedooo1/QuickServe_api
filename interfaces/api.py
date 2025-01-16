from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict
from infrastructure.db import get_db
from application.dto import UserDTO, OrderDTO, LoginDTO, UserResponseDTO
from domain.models import User, Order
from application.utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/users", response_model=UserResponseDTO)
def create_user(user: UserDTO, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)

        # Créer un nouvel utilisateur
        new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Renvoie l'objet UserResponseDTO sans le mot de passe
        return UserResponseDTO(id=new_user.id, name=new_user.name, email=new_user.email)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@router.post("/login", response_model=Dict[str, str])
def login(login_data: LoginDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserDTO])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [UserDTO(id=user.id, name=user.name, email=user.email) for user in users]


@router.get("/orders/{order_id}", response_model=OrderDTO)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderDTO(order_id=order.order_id, user_id=order.user_id, details=order.details)
