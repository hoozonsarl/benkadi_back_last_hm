from pydantic import EmailStr, BaseModel, Field
from datetime import datetime, date, time
from models.receveurs import Sexe
from models.donneurs import StatusMatrimonial, Religion
from models.receveurs import GroupeSanguin
from typing import Optional, List
from enum import Enum

from schemas.donneurs import DonneurResponseModel
from .parametres import ParametreResponseModel

class DonneurUsersCreate(BaseModel):
    nom: str  = Field(examples=["SAMANI SIEWE"])
    prenom: str = Field(examples=["Darix"])
    dateDeNaissance: date = Field(examples=["2000-01-15"])
    lieuDeNaissance: str = Field(examples=["Bafang"])
    numeroCNI: Optional[str] = Field(examples=["123456789987654321"])
    dateDelivranceIdCard: Optional[date] = Field(examples=["2024-02-22"])
    villeResidence: Optional[str] = Field(examples=["Yatchika, Douala, Cameroun"])
    niveauEtude: Optional[str] = Field(examples=["Bac"])
    passport: Optional[str] = Field(default=None, examples=["123456789987654321"])
    permisConduire: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_scolaire: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_elec: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_etudiant: Optional[str] = Field(default=None, examples=["123456789987654321"])
    sexe: Sexe = Field(examples=["HOMME"])
    profession: str = Field(examples=["Developpeur Full Stack"])
    statusMatrimonial: StatusMatrimonial = Field(examples=["Celibataire"])
    paysOrigine: str = Field(examples=["Cameroun"])
    religion: Religion = Field(examples=["MUSULMAN"])
    adresse: str =  Field(examples=["Yatchika, Douala, Cameroun"])
    telephone: str = Field(examples=["678655006"])
    email: Optional[str] = Field(examples=["samanidarix@gmail.com"])
    groupeSanguin: Optional[str] = Field(examples=["A+"])
    dateDeProchainDon: Optional[date] = Field(examples=["2024-02-22"])
    dateDernierDon: Optional[date] = Field(examples=["2024-02-22"])
    datePossibleDon: Optional[date] = Field(examples=["2024-02-22"])
    nombreDeDons: Optional[int] = Field(examples=[0])
    accidentDon: Optional[str] = Field(examples=["{'reponse': 'non', periode: '', lieu: ''}"])
    dejaTransfuse: Optional[str] = Field(examples=["{'reponse': 'oui', periode: '', lieu: ''}"])
    isDelayed: bool = Field(examples=[False, True])
    isDelayedDate: Optional[date] = Field(default=None, examples=["2024-02-22"])
    is_don_done: Optional[bool] = Field(default=False, examples=[False, True])
    last_don_date: Optional[date] = Field(default=None, examples=["2024-02-22"])
    final_comment: Optional[str] = Field(default=None, examples=["commentaire"])
    nombreDeDonsGenyco: Optional[int] = Field(default=None,examples=[0])

class DonneurUsersUpdate(BaseModel):

    nom: Optional[str]  = Field(default=None, examples=["SAMANI SIEWE"])
    prenom: Optional[str] = Field(default=None, examples=["Darix"])
    dateDeNaissance: Optional[date] = Field(default=None, examples=["2000-01-15"])
    lieuDeNaissance: Optional[str] = Field(default=None,examples=["Bafang"])
    numeroCNI: Optional[str] = Field(default=None, examples=["123456789987654321"])
    passport: Optional[str] = Field(default=None, examples=["123456789987654321"])
    permisConduire: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_scolaire: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_elec: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_etudiant: Optional[str] = Field(default=None, examples=["123456789987654321"])
    dateDelivranceIdCard: Optional[date] = Field(default=None, examples=["2024-02-22"])
    villeResidence: Optional[str] = Field(default=None, examples=["Yatchika, Douala, Cameroun"])
    niveauEtude: Optional[str] = Field(default=None, examples=["Bac"])
    sexe: Optional[Sexe] = Field(default=None, examples=["HOMME"])
    profession: Optional[str] = Field(default=None, examples=["Developpeur Full Stack"])
    statusMatrimonial: Optional[StatusMatrimonial] = Field(default=None,examples=["Celibataire"])
    paysOrigine: Optional[str] = Field(default=None, examples=["Cameroun"])
    religion: Optional[Religion] = Field(default=None, examples=["MUSULMAN"])
    adresse: Optional[str] =  Field(default=None, examples=["Yatchika, Douala, Cameroun"])
    telephone: Optional[str] = Field(default=None, examples=["678655006"])
    email: Optional[str] = Field(default=None, examples=["samanidarix@gmail.com"])
    groupeSanguin: Optional[str] = Field(default=None, examples=["A+"])
    dateDeProchainDon: Optional[date] = Field(default=None, examples=["2024-02-22"])
    dateDernierDon: Optional[date] = Field(default=None, examples=["2024-02-22"])
    datePossibleDon: Optional[date] = Field(default=None, examples=["2024-02-22"])
    nombreDeDons:Optional[int] = Field(default=None, examples=[0])
    accidentDon: Optional[str] = Field(default=None,  examples=["{'reponse': 'non', periode: '', lieu: ''}"])
    dejaTransfuse: Optional[str] = Field(default=None, examples=["{'reponse': 'oui', periode: '', lieu: ''}"])
    isDelayed: Optional[bool] = Field(default=None, examples=[False, True])
    isDelayedDate: Optional[date] = Field(default=None, examples=["2024-02-22"])
    is_don_done: Optional[bool] = Field(default=None, examples=[False, True])
    last_don_date: Optional[date] = Field(default=None, examples=["2024-02-22"])
    final_comment: Optional[str] = Field(default=None, examples=["commentaire"])
    nombreDeDonsGenyco: Optional[int] = Field(default=None, examples=[0])



class DonneurUsersResponseModel(DonneurUsersCreate):
    id: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    userName: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    lieuDeNaissance: Optional[str] = None
    numeroCNI: Optional[str] = None
    carte_scolaire: Optional[str] = None
    carte_elec: Optional[str] = None
    carte_etudiant: Optional[str] = None
    dateDelivranceIdCard: Optional[date] = None
    villeResidence: Optional[str] = None
    niveauEtude: Optional[str] = None
    passport: Optional[str] = None
    permisConduire: Optional[str] = None
    sexe: Optional[Sexe] = None
    profession: Optional[str] = None
    statusMatrimonial: Optional[StatusMatrimonial] = None
    paysOrigine: Optional[str] = None
    religion: Optional[Religion] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    groupeSanguin: Optional[str] = None
    dateDeProchainDon: Optional[date] = None
    dateDernierDon: Optional[date] = None
    datePossibleDon: Optional[date] = None
    nombreDeDons: Optional[int] = None
    accidentDon: Optional[str] = None
    dejaTransfuse: Optional[str] = None
    isDelayed: Optional[bool] = None
    isDelayedDate: Optional[date] = None
    is_don_done: Optional[bool] = None
    last_don_date: Optional[date] = None
    final_comment: Optional[str] = None
    nombreDeDonsGenyco: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime
    donneurs: List[DonneurResponseModel]


class DonneurUsersWithoutDonneurResponseModel(DonneurUsersCreate):
    id: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    userName: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    lieuDeNaissance: Optional[str] = None
    numeroCNI: Optional[str] = None
    carte_scolaire: Optional[str] = None
    carte_elec: Optional[str] = None
    carte_etudiant: Optional[str] = None
    dateDelivranceIdCard: Optional[date] = None
    villeResidence: Optional[str] = None
    niveauEtude: Optional[str] = None
    passport: Optional[str] = None
    permisConduire: Optional[str] = None
    sexe: Optional[Sexe] = None
    profession: Optional[str] = None
    statusMatrimonial: Optional[StatusMatrimonial] = None
    paysOrigine: Optional[str] = None
    religion: Optional[Religion] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    groupeSanguin: Optional[str] = None
    dateDeProchainDon: Optional[date] = None
    dateDernierDon: Optional[date] = None
    datePossibleDon: Optional[date] = None
    nombreDeDons: Optional[int] = None
    accidentDon: Optional[str] = None
    dejaTransfuse: Optional[str] = None
    isDelayed: Optional[bool] = None
    isDelayedDate: Optional[date] = None
    is_don_done: Optional[bool] = None
    last_don_date: Optional[date] = None
    final_comment: Optional[str] = None
    nombreDeDonsGenyco: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime



class DonneurUsersWithDonneurResponseModel(DonneurUsersCreate):
    # class Config:
    #     from_attributes = True
    id: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    userName: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    lieuDeNaissance: Optional[str] = None
    numeroCNI: Optional[str] = None
    carte_scolaire: Optional[str] = None
    carte_elec: Optional[str] = None
    carte_etudiant: Optional[str] = None
    dateDelivranceIdCard: Optional[date] = None
    villeResidence: Optional[str] = None
    niveauEtude: Optional[str] = None
    passport: Optional[str] = None
    permisConduire: Optional[str] = None
    sexe: Optional[Sexe] = None
    profession: Optional[str] = None
    statusMatrimonial: Optional[StatusMatrimonial] = None
    paysOrigine: Optional[str] = None
    religion: Optional[Religion] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    groupeSanguin: Optional[str] = None
    dateDeProchainDon: Optional[date] = None
    dateDernierDon: Optional[date] = None
    datePossibleDon: Optional[date] = None
    nombreDeDons: Optional[int] = None
    accidentDon: Optional[str] = None
    dejaTransfuse: Optional[str] = None
    isDelayed: Optional[bool] = None
    isDelayedDate: Optional[date] = None
    is_don_done: Optional[bool] = None
    last_don_date: Optional[date] = None
    final_comment: Optional[str] = None
    nombreDeDonsGenyco: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime
    
    
