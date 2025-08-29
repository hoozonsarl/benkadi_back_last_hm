from models.receveurs import Sexe
from pydantic import Field, BaseModel
from typing import List
from datetime import date, time, datetime
from typing import Optional
from uuid import UUID

from schemas.donneurs import DonneurResponseModel

class PrelevementCreate(BaseModel):
    id_donneur: int =  Field()
    dateDePrelevement: date = Field()
    heureDebut: time =  Field(examples=["10:10"])
    heureFin: time = Field(examples=["10:30"])
    poidsDePoche: int = Field()
    volumePrevele: int = Field()
    remarques: str  = Field() 
    effetsIndesirables: str = Field()
    # estAnalyser: Optional[bool] = Field(examples=[False])
    id_parametre: int = Field(examples=[1])
    # is_phenotype_done: Optional[bool] = Field(examples=[False])


class PrelevementUpdate(BaseModel):
    dateDePrelevement: Optional[date] = Field()
    heureDebut: Optional[time] =  Field(examples=["10:10"])
    heureFin: Optional[time] = Field(examples=["10:30"])
    poidsDePoche: Optional[int] = Field()
    volumePrevele: Optional[int] = Field()
    remarques: Optional[str]  = Field()
    effetsIndesirables: Optional[str] = Field()
    id_parametre: Optional[int] = Field(examples=[1])
    #is_phenotype_done: Optional[bool] = Field(examples=[False])
    #estAnalyser: Optional[bool] = Field(examples=[False])


class ParametreResponseModel(BaseModel):
    examen_tdr: str

class PrelevementResponseModel(PrelevementCreate):
    id: int
    id_user:int
    numero_code_bar: str  
    codeBar: str 
    createdAt: datetime
    updatedAt: datetime 
    code_diff: str
    parametres: ParametreResponseModel



class DonneurPrelevementResponseModel(BaseModel):
    id: int
    nom: Optional[str]
    prenom: Optional[str]
    sexe: Optional[Sexe]
    telephone: Optional[str]
    commentaire: Optional[str]

    


class PrelevementDonneurResponseModel(PrelevementCreate):
    id: int
    id_user:int
    numero_code_bar: str  
    codeBar: str 
    createdAt: datetime
    updatedAt: datetime 
    code_diff: str
    donneur: DonneurPrelevementResponseModel
    #parametres: ParametreResponseModel
    
