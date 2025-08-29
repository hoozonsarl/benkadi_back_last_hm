from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime, Float 
from sqlalchemy.orm import Relationship
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import date
from enum import Enum as PyEnum
from pydantic import EmailStr
from datetime import datetime




class ParamsReceveur(Base):

    __tablename__ = "params_receveurs"


    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    temps: str = Column(String)
    temperature: float = Column(Float)
    pression_arterielle: str = Column(String)
    rythme_respiratoire: int = Column(Integer)
    saturation_en_oxygene: int = Column(Integer)
    pouls: int = Column(Integer)
    ta: str = Column(String)
    etat_du_malade: str = Column(String)
    frissons: str = Column(String)
    sueurs: str = Column(String)
    id_user: int  = Column(Integer, ForeignKey("users.id"))
    createdAt: datetime  = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_bon_de_sang = Column(Integer, ForeignKey("bon_de_sangs.id", ondelete='CASCADE'))
    bon_de_sang = relationship("BonDeSang", back_populates="params_receveurs")
    
    def __repr__(self):
        return f"<ParamsReceveur id: {self.id} temps: {self.temps} temperature: {self.temperature} ...>"