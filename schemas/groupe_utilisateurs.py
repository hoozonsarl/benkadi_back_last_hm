from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime, date
from schemas.permissions import PermissionResponseModel
from models.users import Gender


class GroupeUtilisateurCreate(BaseModel):
    nom: str


class GroupeUtilisateurUpdate(BaseModel):
    nom: str
    


class UserResponseModel(BaseModel):
    id:int 
    email:EmailStr 
    password: str 
    gender : Gender
    dateNaissance: date 
    intituleDuPoste: str
    telephone: str
    nom: str 
    prenom: str 
    nationality: str 
    id_groupe_utilisateur: int


class GroupeUtilisateurResponseModel(GroupeUtilisateurCreate):
    id: int 
    createdAt: datetime
    updatedAt: datetime
    permissions: List[PermissionResponseModel]
    users: List[UserResponseModel]
    



