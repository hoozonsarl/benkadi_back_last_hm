from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PermissionsCreate(BaseModel):
    action: str
    subject: str


class PermissionsUpdate(BaseModel):
    action: Optional[str]
    subject: Optional[str]


class PermissionResponseModel(BaseModel):
    id:int 
    action: str
    subject: str
    createdAt: datetime
    updatedAt: datetime 