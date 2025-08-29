from pydantic import Field, BaseModel, EmailStr
from enum import Enum as PyEnum
from typing import Union, Optional
from datetime import date, datetime






    

class ParamsReceveurCreate(BaseModel):
    temps: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    pression_arterielle: Optional[str] = Field(default=None)
    rythme_respiratoire: Optional[int] = Field(default=None)
    saturation_en_oxygene: Optional[int] = Field(default=None)
    pouls: Optional[int] = Field(default=None)
    ta: Optional[str] = Field(default=None)
    etat_du_malade: Optional[str] = Field(default=None)
    frissons: Optional[str] = Field(default=None)
    sueurs: Optional[str] = Field(default=None) 
    id_bon_de_sang: Optional[int] = Field(default=None)



class ParamsReceveurUpdate(BaseModel):
    temps: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    pression_arterielle: Optional[str] = Field(default=None)
    rythme_respiratoire: Optional[int] = Field(default=None)
    saturation_en_oxygene: Optional[int] = Field(default=None)
    pouls: Optional[int] = Field(default=None)
    ta: Optional[str] = Field(default=None)
    etat_du_malade: Optional[str] = Field(default=None)
    frissons: Optional[str] = Field(default=None)
    sueurs: Optional[str] = Field(default=None)
    id_bon_de_sang: Optional[int] = Field(default=None)








class ParamsReceveurResponseModel(ParamsReceveurUpdate):
    id: int
    temps: Optional[str]
    temperature: Optional[float]
    pression_arterielle: Optional[str]
    rythme_respiratoire: Optional[int]
    saturation_en_oxygene: Optional[int]
    pouls: Optional[int]
    ta: Optional[str]
    etat_du_malade: Optional[str]
    frissons: Optional[str]
    sueurs: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    id_user: int

