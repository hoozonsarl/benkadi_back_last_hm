from pydantic import BaseModel, Field
from datetime import datetime, date, time
from typing import Optional, List
from schemas.fractions import FractionResponseModel


class DistributionCreate(BaseModel):

    id_fractions: List[int]
    id_bon_de_sang: int
    telephoneTransporteur: Optional[str] = Field(default=None)
    nomTransporteur: Optional[str] = Field(default=None)
    cniTransporteur: Optional[str] = Field(default=None)
    nom_hospital_destinataire: Optional[str] = Field(default=None)
    service: Optional[str] = Field(default=None)
    is_interne: Optional[bool] = Field(default=False)


class DistributionUpdate(BaseModel):

    fractions: List[int]
    id_bon_de_sang: int
    telephoneTransporteur: Optional[str]
    nomTransporteur: Optional[str]
    cniTransporteur: Optional[str]
    nom_hospital_destinataire: Optional[str] 
    service: Optional[str]
    is_interne: Optional[bool]



class DistributionResponseModel(BaseModel):

    id: int
    dateDeDistribution: datetime
    telephoneTransporteur: str
    nomTransporteur: str
    cniTransporteur: str
    nom_hospital_destinataire: str
    service: str
    is_interne: bool
    id_fraction: int
    id_user: int
    id_bon_de_sang: int
    createdAt: datetime
    updatedAt: datetime                                                                 
    id_fraction: Optional[int] = Field(examples=[1])
    id_receveur: Optional[int] = None