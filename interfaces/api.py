from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict
from infrastructure.db import get_user_db
from application.dto import UserDTO, OrderDTO, LoginDTO, UserResponseDTO
from domain.models import User, Order
from application.utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM

router = APIRouter()

user_router = APIRouter(prefix="/users", tags=["UserService"])
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
order_router = APIRouter(prefix="/orders", tags=["OrderService"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_user_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@auth_router.post("/", response_model=UserResponseDTO)
def create_user(user: UserDTO, db: Session = Depends(get_user_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if (existing_user):
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


@auth_router.post("/login", response_model=Dict[str, str])
def login(login_data: LoginDTO, db: Session = Depends(get_user_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/", response_model=List[UserResponseDTO])
def list_users(db: Session = Depends(get_user_db)):
    try:
        users = db.query(User).all()
        return [UserResponseDTO(id=user.id, name=user.name, email=user.email) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@user_router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, db: Session = Depends(get_user_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO(id=user.id, name=user.name, email=user.email)


@user_router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(user_id: int, user: UserDTO, db: Session = Depends(get_user_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name
    existing_user.email = user.email
    db.commit()
    db.refresh(existing_user)

    return UserResponseDTO(id=existing_user.id, name=existing_user.name, email=existing_user.email)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_user_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token, db)
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(order_router)