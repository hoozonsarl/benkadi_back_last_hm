from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional
from models.users import Gender
from datetime import datetime
from schemas.permissions import PermissionResponseModel

class UserCreate(BaseModel):
    email:EmailStr = Field(examples=["samanidarix@gmail.com"])
    password: str = Field(examples=["6775212952"])
    gender : Gender
    dateNaissance: date = Field(examples=["2019-12-04"])
    intituleDuPoste: str = Field(examples=["Medecin"])
    telephone: str = Field(examples=["6775212952"])
    nom: str = Field(examples=["SAMANI SIEWE"])
    prenom: str = Field(examples=["Darix"])
    nationality: str = Field(examples=["Camerounaise"])


class UserUpdate(BaseModel):
    email:Optional[EmailStr] = Field(examples=["samanidarix@gmail.com"])
    password: Optional[str] = Field(examples=["6775212952"])
    gender : Optional[Gender]
    dateNaissance: Optional[date] = Field(examples=["2019-12 -04"])
    intituleDuPoste: Optional[str] = Field(examples=["Medecin"])
    telephone: Optional[str] = Field(examples=["6775212952"])
    nom: Optional[str] = Field(examples=["SAMANI SIEWE"])
    prenom: Optional[str] = Field(examples=["Darix"])
    nationality: Optional[str] = Field(examples=["Camerounaise"])



class GroupeUtilisateurResponseModel(BaseModel):
    id: int
    nom: str
    createdAt: datetime
    updatedAt: datetime


class UserResponseModel(UserCreate):
    id: int 
    id_groupe_utilisateur: int 
    groupe_utilisateur: GroupeUtilisateurResponseModel
    createdAt: datetime
    updatedAt: datetime





class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponseModel
    permissions: List[PermissionResponseModel]
