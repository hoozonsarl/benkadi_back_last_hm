from pydantic import EmailStr, BaseModel, Field
from datetime import datetime, date, time
from models.receveurs import Sexe
from models.donneurs import StatusMatrimonial, Religion
from models.receveurs import GroupeSanguin
from typing import Optional, List
from enum import Enum
from .parametres import ParametreResponseModel

class DonneurCreate(BaseModel):
    nom: Optional[str]  = Field(examples=["SAMANI SIEWE"])
    prenom: Optional[str] = Field(examples=["Darix"])
    dateDeNaissance: Optional[date] = Field(examples=["2000-01-15"])
    lieuDeNaissance: Optional[str] = Field(examples=["Bafang"])
    numeroCNI: Optional[str] = Field(examples=["123456789987654321"])
    dateDelivranceIdCard: Optional[date] = Field(examples=["2024-02-22"])
    villeResidence: Optional[str] = Field(examples=["Yatchika, Douala, Cameroun"])
    niveauEtude: Optional[str] = Field(examples=["Bac"])
    passport: Optional[str] = Field(default=None, examples=["123456789987654321"])
    permisConduire: Optional[str] = Field(default=None,examples=["123456789987654321"])
    carte_scolaire: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_elec: Optional[str] = Field(default=None, examples=["123456789987654321"])
    carte_etudiant: Optional[str] = Field(default=None, examples=["123456789987654321"])
    sexe: Optional[Sexe] = Field(examples=["HOMME"])
    profession: Optional[str] = Field(examples=["Developpeur Full Stack"])
    statusMatrimonial: Optional[StatusMatrimonial] = Field(examples=["Celibataire"])
    paysOrigine: Optional[str] = Field(examples=["Cameroun"])
    religion: Optional[Religion] = Field(examples=["MUSULMAN"])
    adresse: Optional[str] =  Field(examples=["Yatchika, Douala, Cameroun"])
    telephone: Optional[str] = Field(examples=["678655006"])
    email: Optional[str] = Field(examples=["samanidarix@gmail.com"])
    groupeSanguin: Optional[str] = Field(examples=["A+"])
    dateDeProchainDon: Optional[date] = Field(examples=["2024-02-22"])
    dateDernierDon: Optional[date] = Field(examples=["2024-02-22"])
    isDelayed: Optional[bool] = Field(examples=[False, True])
    isDelayedDate: Optional[date] = Field(examples=["2024-02-22"])
    datePossibleDon: Optional[date] = Field(examples=["2024-02-22"])
    nombreDeDons: Optional[int] = Field(examples=[0])
    accidentDon: Optional[str] = Field(examples=["{'reponse': 'non', periode: '', lieu: ''}"])
    dejaTransfuse: Optional[str] = Field(examples=["{'reponse': 'oui', periode: '', lieu: ''}"])
    quartier: Optional[str] = Field(examples=["Yassa", "ndokoti"])
    lu_approve: Optional[bool] = Field(examples=[True, False])
    dateAccueil: Optional[date] = Field(examples=["2024-02-22"])
    heureAccueil: Optional[time] = Field(examples=["10:00:00"])
    dateConsultation: Optional[date] = Field(examples=["2024-02-22"])
    heureConsultation: Optional[time] = Field(examples=["10:00:00"])
    is_tdr_done: Optional[bool] = Field(default=False, examples=[False, True])
    is_ok_prelevement: Optional[bool] = Field(default=False, examples=[False, True])
    is_rejected: Optional[bool] = Field(default=False, examples=[False, True])
    is_prelevement_done: Optional[bool] = Field(default=False, examples=[False, True])
    is_don_done: Optional[bool] = Field(default=False, examples=[False, True])
    last_don_date: Optional[date] = Field(default=None, examples=["2024-02-22"])
    final_comment: Optional[str] = Field(default=None, examples=["commentaire"])
    nombreDeDonsGenyco: Optional[int] = Field(default=None,examples=[0])

class DonneurUpdate(BaseModel):

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
    isDelayed: Optional[bool] = Field(default=None, examples=[False, True])
    isDelayedDate: Optional[date] = Field(default=None, examples=["2024-02-22"])
    nombreDeDons:Optional[int] = Field(default=None, examples=[0])
    accidentDon: Optional[str] = Field(default=None,  examples=["{'reponse': 'non', periode: '', lieu: ''}"])
    dejaTransfuse: Optional[str] = Field(default=None, examples=["{'reponse': 'oui', periode: '', lieu: ''}"])
    isDonneur: Optional[bool] = Field(default=None, examples=[True])
    quartier: Optional[str] = Field(default=None, examples=["Yassa", "ndokoti"])
    isValideMedecin: Optional[bool] = Field(default=None, examples=[True, False])
    dateAccueil: Optional[date] = Field(default=None, examples=["2024-02-22"])
    heureAccueil: Optional[time] = Field(default=None, examples=["10:00:00"])
    dateConsultation: Optional[date] = Field(default=None, examples=["2024-02-22"])
    heureConsultation: Optional[time] = Field(default=None, examples=["10:00:00"])
    isValideAnalyseTDR: Optional[bool] = Field(default=None, examples=[True, False])
    is_tdr_done: Optional[bool] = Field(default=None, examples=[False, True])
    is_ok_prelevement: Optional[bool] = Field(default=None, examples=[False, True])
    is_rejected: Optional[bool] = Field(default=None, examples=[False, True])
    is_prelevement_done: Optional[bool] = Field(default=None, examples=[False, True])
    is_don_done: Optional[bool] = Field(default=None, examples=[False, True])
    last_don_date: Optional[date] = Field(default=None, examples=["2024-02-22"])
    final_comment: Optional[str] = Field(default=None, examples=["commentaire"])
    nombreDeDonsGenyco: Optional[int] = Field(default=None,examples=[0])



class DonneurResponseModel(DonneurCreate):
    id: int
    isDonneur: bool
    createdAt: datetime
    updatedAt: datetime
    isValideMedecin: Optional[bool] = None
    isValideAnalyseTDR: Optional[bool] = None
    is_tdr_done: Optional[bool] = None
    is_ok_prelevement: Optional[bool] = None    
    is_rejected: Optional[bool] = None
    is_prelevement_done: Optional[bool] = None
    is_don_done: Optional[bool] = None
    last_don_date: Optional[date] = None
    final_comment: Optional[str] = None
    lu_approve: Optional[bool] = None
    parametres: List[ParametreResponseModel]
    
