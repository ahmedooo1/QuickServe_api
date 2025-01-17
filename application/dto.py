from pydantic import BaseModel, EmailStr

# DTO pour l'utilisateur (Modèle d'entrée pour la création)
class UserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str 

    class Config:
        orm_mode = True  

# DTO pour la réponse après création
class UserResponseDTO(BaseModel):
    id: int  
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# DTO pour la commande
class OrderDTO(BaseModel):
 #   id: int
    user_id: int
    details: str

# DTO pour les données de connexion
class LoginDTO(BaseModel):
    email: EmailStr
    password: str
