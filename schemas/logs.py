from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Any, Dict, Optional
from datetime import date
from enum import Enum as PyEnum
from pydantic import EmailStr
# from .receveurs import ReceveurResponseModel

class LogsCreate(BaseModel):
    action: Optional[str] = None
    nom_utilisateur: Optional[str] = None
    date_action: Optional[datetime] = None
    ressource: Optional[str] = None
    status: Optional[str] = None
    id_utilisateur: Optional[int] = None

class LogsUpdate(BaseModel):
    action: Optional[str] = None
    nom_utilisateur: Optional[str] = None
    date_action: Optional[datetime] = None
    ressource: Optional[str] = None
    status: Optional[str] = None
    id_utilisateur: Optional[int] = None

class LogsResponseModel(LogsCreate):
    id : int
    nom_utilisateur: Optional[str] = None
    date_action: Optional[datetime] = None
    ressource: Optional[str] = None
    status: Optional[str] = None
    id_utilisateur: Optional[int] = None
    updatedAt: datetime
    createdAt: datetime
