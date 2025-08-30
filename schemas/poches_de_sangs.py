from pydantic import BaseModel, Field
from datetime import datetime, date, time
from models.receveurs import GroupeSanguin
from typing import Optional

from schemas.parametres import DonneurResponseModel, ParametreResponseModel

class PocheDeSangCreate(BaseModel):
    groupeSanguin: GroupeSanguin = Field(examples=["A+", "A-", "O+"])
    phenotype:  Optional[str] = Field(default=None, examples=["string", "string string"])
    dateAnalyse: datetime = Field()
    estvalide: bool = Field(default=False)
    id_prelevement: int = Field(examples=[1])
    id_donneur: int = Field(examples=[1])
    motifDestruction: str = Field(default="", examples=["string string string"])
    observation: str = Field(examples=["test test test test"])
    examens: str = Field(examples=["string string string"])
    is_phenotype_done: bool = Field(default=False)


class PocheDeSangUpdate(BaseModel):
    groupeSanguin: Optional[GroupeSanguin] = Field(default=None, examples=["A+", "A-", "O+"])
    phenotype: Optional[str] = Field(default=None, examples=["string", "string string"])
    dateAnalyse: Optional[datetime] = Field(default=None,)
    estvalide: Optional[bool] = Field(default=None)
    estFractionne: Optional[bool] = Field(default=None)
    id_prelevement: Optional[int] = Field(default=None, examples=[1])
    id_donneur: Optional[int] = Field(default=None, examples=[1])
    motifDestruction: Optional[str] = Field(default=None, examples=["string string string"])
    observation: Optional[str] = Field(default=None, examples=["test test test test"])
    estDetruire: Optional[bool] = Field(default=None, examples=[True])
    isAnalyseDone: Optional[bool] = Field(default=None, examples=[True])
    examens: Optional[str] = Field(default=None, examples=[""])
    is_phenotype_done: Optional[bool] = Field(default=None, examples=[True])


class PrelevementResponseModel(BaseModel):
    id: int
    numero_code_bar: str
    codeBar: str
    dateDePrelevement: date
    heureDebut: time
    heureFin: time
    poidsDePoche: int
    effetsIndesirables: str
    estAnalyser: bool
    id_donneur: int
    id_parametre: int
    id_user: int
    volumePrevele: int
    remarques: str
    parametres: ParametreResponseModel
    createdAt: datetime
    updatedAt: datetime
    code_diff: str 

    
class PocheDeSangResponseModel(PocheDeSangCreate):
    id: int
    createdAt: datetime
    updatedAt: datetime
    id_user: int
    estFractionne: bool
    estDetruire: bool
    prelevement: PrelevementResponseModel
    examens: str



    
    
    
    
    