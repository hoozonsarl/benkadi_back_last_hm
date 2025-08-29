from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime, date
from models.receveurs import GroupeSanguin
class FractionCreate(BaseModel):
    id_poche_de_sang: int = Field(examples=[1, 2])
    dateDePrelevement: date = Field(examples=["2024-02-22"])    
    id_fraction_type: int = Field(examples=[1])
    is_valid: bool = Field(default=False)
    is_analyse_done: bool = Field(default=False)
    volume: int = Field(examples=[10, 25])
    poids: int = Field(examples=[4, 5])
    is_ok_to_use: bool = Field(default=False)
    is_destroy: Optional[bool] = Field(default=False)


class FractionUpdate(BaseModel):
    dateDePrelevement: Optional[date] = Field(examples=["2024-02-22"])
    dateDeExpiration: Optional[date] = Field(examples=["2024-02-22"])
    id_fraction_type: Optional[int] = Field(examples=[1])
    volume: Optional[int] = Field(examples=[10, 25])
    poids: Optional[int] = Field(examples=[4, 10])
    is_valid: Optional[bool] = Field(default=False)
    is_analyse_done: Optional[bool] = Field(default=False)
    is_ok_to_use: Optional[bool] = Field(default=False)
    is_destroy: Optional[bool] = Field(default=False)

class PocheDeSangResponseModel(BaseModel):
    id: int
    groupeSanguin: GroupeSanguin
    phenotype: str
    dateAnalyse: datetime
    estvalide: bool
    estFractionne: bool
    id_prelevement: int
    id_donneur: int
    id_user: int
    motifDestruction: str
    observation: str 
    createdAt: datetime
    updatedAt: datetime


class TypeDeFractionResponseModel(BaseModel):
    id: int
    nom: str
    nombreDeJourExpiration: int
    createdAt: datetime
    updatedAt: datetime
    is_default_selected: bool
    quarantaine: int 
    code: str
    


class FractionResponseModel(FractionCreate):
    id: int
    estDistribue: bool
    dateDeExpiration: date
    estArchive: bool
    createdAt: datetime
    updatedAt: datetime
    numero_code_bar: str
    code_bar: str
    is_valid: bool
    is_analyse_done: bool
    is_ok_to_use: bool
    dateAvailable: date
    poche_de_sang: PocheDeSangResponseModel
    type_de_fraction: TypeDeFractionResponseModel

