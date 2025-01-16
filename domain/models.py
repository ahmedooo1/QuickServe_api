from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db import UserBase, OrderBase

# Modèle User
class User(UserBase):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True) 
    hashed_password = Column(String)

 #   orders = relationship("Order", back_populates="user")

# Modèle Order
class Order(OrderBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(255), unique=True, index=True)  # Ajout de la longueur de la colonne order_id
    user_id = Column(Integer, index=True)
    details = Column(String(255)) 

    # Si tu veux une relation avec l'utilisateur, tu peux ajouter la ligne suivante :
   # user = relationship("User", back_populates="orders")