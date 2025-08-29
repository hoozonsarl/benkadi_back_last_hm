from sqlalchemy import Integer, String, ForeignKey, DateTime, Column
from database.database import Base
from datetime import datetime

class Sms(Base):

    __tablename__ = "smss"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    contenue: str  = Column(String,)
    id_user: int  = Column(Integer, ForeignKey("users.id"))
    id_donneur: int = Column(Integer, ForeignKey("donneurs.id"))
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    