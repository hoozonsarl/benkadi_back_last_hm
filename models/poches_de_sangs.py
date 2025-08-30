from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Relationship, relationship
from database.database import Base
from datetime import datetime
from models.receveurs import GroupeSanguin

class PocheDeSang(Base):

    __tablename__ = "pocheDeSangs"

    id: int = Column(Integer, primary_key=True, unique=True)
    groupeSanguin: GroupeSanguin = Column(Enum(GroupeSanguin))
    phenotype: str = Column(String, default=None)
    dateAnalyse: datetime = Column(DateTime)
    estvalide: bool = Column(Boolean, default=False)
    estFractionne: bool = Column(Boolean, default=False)
    estDetruire: bool = Column(Boolean, default=False)
    id_prelevement: int = Column(Integer, ForeignKey("prelevements.id", ondelete='CASCADE'), )
    id_donneur:int = Column(Integer, ForeignKey("donneurs.id"))
    id_user: int = Column(Integer, ForeignKey("users.id"))
    motifDestruction: str  = Column(String)
    observation: str = Column(String)
    isAnalyseDone: bool = Column(Boolean, default=False)
    createdAt: datetime  = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    examens: str  = Column(String)
    prelevement = relationship("Prelevement", back_populates='poche_de_sang', cascade="all, delete")
    fractions = relationship("Fraction", back_populates="poche_de_sang", cascade="all, delete")
    is_phenotype_done: bool = Column(Boolean, default=False)

