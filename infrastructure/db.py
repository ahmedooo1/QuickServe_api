from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration pour la base de données des utilisateurs (UsersService)
USER_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/usersservice"
user_engine = create_engine(USER_DATABASE_URL, echo=True)
UserBase = declarative_base()

# Configuration pour la base de données des commandes (OrdersService)
ORDER_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/orderservice"
order_engine = create_engine(ORDER_DATABASE_URL, echo=True)
OrderBase = declarative_base()

# Session pour les utilisateurs
UserSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=user_engine)

# Session pour les commandes
OrderSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=order_engine)

# Fonction pour créer les tables pour les utilisateurs
def create_user_database():
    UserBase.metadata.create_all(bind=user_engine)

# Fonction pour créer les tables pour les commandes
def create_order_database():
    OrderBase.metadata.create_all(bind=order_engine)

# Fonction pour obtenir la session des utilisateurs
def get_user_db():
    db = UserSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour obtenir la session des commandes
def get_order_db():
    db = OrderSessionLocal()
    try:
        yield db
    finally:
        db.close()
