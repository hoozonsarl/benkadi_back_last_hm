from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SMSCreate(BaseModel):
    contenue: str

class SMSUpdate(BaseModel):
    contenue: Optional[str]


class SMSResponseModel(SMSCreate):
    id:int
    createdAt: datetime
    updatedAt: datetime
