from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db import Base

# Modèle User
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True) 
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="user")

# Modèle Order
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)  # Référence à 'users.id'
    details = Column(String)

    user = relationship("User", back_populates="orders")  # Relation avec le modèle User
