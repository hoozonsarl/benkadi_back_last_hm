from pydantic import Field, BaseModel, EmailStr
from enum import Enum as PyEnum
from typing import List, Union, Optional
from datetime import date, datetime
from schemas.bon_de_sang import BonDeSangResponseModel

class GroupeSanguin(str, PyEnum):
    Aplus = "A+"
    Amoins = "A-"

    ABplus = "AB+"
    ABmoins = "AB-"

    Oplus = "O+"
    Omoins = "O-"

    Bplus = "B+"
    Bmoins = "B-"

class Sexe(str, PyEnum):
    HOMME = "HOMME"
    FEMMME = "FEMME"


    

class ReceveurCreate(BaseModel):
    nom: str 
    prenom: Union[str, None]
    hospital: Optional[str] = None
    dateDeNaissance: date
    sexe: Sexe
    groupe_sanguin: Optional[str] = None
    groupe_sanguin_receveur: Optional[str] = None
    phenotype: Optional[str] = None
    email: Optional[str] = None
    telephone: str = Field(pattern=r"^6(\d){8}")
    service: Optional[str] = None


class ReceveurUpdate(BaseModel):
    nom: Optional[str] = Field(default=None)
    prenom: Optional[str] = Field(default=None)
    hospital: Optional[str] = Field(default=None)
    dateDeNaissance: Optional[date] = Field(default=None)
    sexe: Optional[Sexe] = Field(default=None)
    groupe_sanguin: Optional[str] = Field(default=None)
    groupe_sanguin_receveur: Optional[str] = Field(default=None)
    phenotype: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    telephone: Optional[str] = Field(default=None)
    service: Optional[str] = Field(default=None)


class GroupeSanguin(str, PyEnum):
    Aplus = "A+"
    Amoins = "A-"

    ABplus = "AB+"
    ABmoins = "AB-"

    Oplus = "O+"
    Omoins = "O-"

    Bplus = "B+"
    Bmoins = "B-"

class ReceveurResponseModel(BaseModel):
    id: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    userName: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    sexe: Optional[str] = None
    groupe_sanguin: Optional[str] = None
    groupe_sanguin_receveur: Optional[str] = None
    phenotype: Optional[str] = None
    id_user: int
    createdAt: datetime
    updatedAt: datetime
    hospital: Optional[str] = None


class HospitalResponseModel(BaseModel):
    id: int
    nom: str
    ville: str
    createdAt: datetime
    updatedAt: datetime

class HospitalResponseModel(BaseModel):
    nom: str
    ville: str
    id:int
    id_user: int
    updatedAt: datetime
    createdAt: datetime


class ReceveurWithBonDeSangResponseModel(ReceveurCreate):
    id: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    userName: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    sexe: Optional[str] = None
    groupe_sanguin: Optional[str] = None
    groupe_sanguin_receveur: Optional[str] = None
    phenotype: Optional[str] = None
    hospital: Optional[str] = None
    service: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    id_user: int
    bon_de_sangs: List[BonDeSangResponseModel]




class ReceveurResponseModel(ReceveurUpdate):
    id: int
    createdAt: datetime
    updatedAt: datetime
    id_user: int
    hospital: HospitalResponseModel