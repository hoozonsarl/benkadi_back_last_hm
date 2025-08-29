from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FractionTypeCreate(BaseModel):
    nom: str = Field(examples = ["concentre de glogule rouge", "plaquette", "plasma"])
    nombreDeJourExpiration: int = Field(examples=[36, 1095, 5]) 
    is_default_selected: bool = Field(default=False, examples=[True, False])
    code: str = Field(examples=["001", "011", "111"])
    quarantaine: int = Field(examples=[0, 120])
    is_total: bool = Field(default=False, examples=[False, True])

class FractionTypeUpdate(BaseModel):
    nom: Optional[str]
    nombreDeJourExpiration: Optional[int]
    code: Optional[str]
    quarantaine: Optional[int]
    is_total: Optional[bool]


class FractionTypeResponseModel(FractionTypeCreate):
    id:int
    createdAt: datetime
    updatedAt: datetime
