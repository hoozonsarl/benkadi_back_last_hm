from pydantic import BaseModel, Field
from datetime import datetime, date, time
from typing import Optional, List



class ReactifCreate(BaseModel):

    nom: Optional[str]  = Field(default=None, examples=["new"])
    reference: Optional[str] = Field(default=None, examples=["Darix"])
    date_expiration: Optional[date] = Field(default=None, examples=["2000-01-15"])
    date_production: Optional[date] = Field(default=None, examples=["2000-01-15"])
    quantite: Optional[int] = Field(default=None, examples=[1])
    numero_lot: Optional[str] = Field(default=None, examples=["1234567890"])
    valeur_seuil: Optional[float] = Field(default=None, examples=[10])
    is_deleted: bool = Field(default=False)
  


class ReactifUpdate(BaseModel):

    nom: Optional[str]  = Field(default=None, examples=["new"])
    reference: Optional[str] = Field(default=None, examples=["Darix"])
    date_expiration: Optional[date] = Field(default=None, examples=["2000-01-15"])
    date_production: Optional[date] = Field(default=None, examples=["2000-01-15"])
    quantite: Optional[int] = Field(default=None, examples=[1])
    numero_lot: Optional[str] = Field(default=None, examples=["1234567890"])
    valeur_seuil: Optional[float] = Field(default=None, examples=[10])
    is_deleted: bool = Field(default=False)


class ReactifResponseModel(BaseModel):

    id: int
    nom: Optional[str]  = None
    reference: Optional[str] = None
    date_expiration: Optional[date] = None
    date_production: Optional[date] = None
    quantite: Optional[int] = None
    numero_code_bar: Optional[str] = None
    codeBar: Optional[str] = None
    numero_lot: Optional[str] = None
    valeur_seuil: Optional[float] = None
    is_deleted: bool = False
    id_user: int
    createdAt: datetime
    updatedAt: datetime                                                                 