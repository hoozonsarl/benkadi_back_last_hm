from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Any, Dict, Optional
from datetime import date
from enum import Enum as PyEnum
from pydantic import EmailStr
# from .receveurs import ReceveurResponseModel

class HospitalCreate(BaseModel):
        nom: Optional[str] = None
        ville: Optional[str] = None

class HospitalUpdate(HospitalCreate):
        pass


class GroupeSanguin(str, PyEnum):
    Aplus = "A+"
    Amoins = "A-"

    ABplus = "AB+"
    ABmoins = "AB-"

    Oplus = "O+"
    Omoins = "O-"

    Bplus = "B+"
    Bmoins = "B-"



class HospitalResponseModel(HospitalCreate):
    id : int
    id_user: int
    updatedAt: datetime
    createdAt: datetime
#     receveurs: List[ReceveurResponseModel]
