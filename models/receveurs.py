from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import Relationship
from database.database import Base
from sqlalchemy.orm import relationship
from datetime import date
from enum import Enum as PyEnum
from datetime import datetime


class Sexe(str, PyEnum):
    HOMME = "HOMME"
    FEMME = "FEMME"

class GroupeSanguin(str, PyEnum):
    Aplus = "A+"
    Amoins = "A-"

    ABplus = "AB+"
    ABmoins = "AB-"

    Oplus = "O+"
    Omoins = "O-"

    Bplus = "B+"
    Bmoins = "B-"

class Receveur(Base):

    __tablename__ = "receveurs"


    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom: str = Column(String(50), nullable=False)
    prenom: str =  Column(String(50), nullable=True)
    userName: str = Column(String(80), nullable=False)
    dateDeNaissance: date = Column(Date)
    telephone: str = Column(String(100))
    email: str = Column(String(100))
    sexe: Sexe = Column(Enum(Sexe), default=Sexe.HOMME)
    groupe_sanguin: str = Column(String, nullable=True, default=None)
    groupe_sanguin_receveur: str = Column(String, nullable=True, default=None)
    phenotype: str = Column(String)
    id_user: int  = Column(Integer, ForeignKey("users.id"))
    createdAt: datetime  = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    hospital: str = Column(String, nullable=True)
    service : str = Column(String, nullable=True)
    bon_de_sangs = relationship("BonDeSang", back_populates="receveur", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Receveur id: {self.id} nom: {self.nom} prenom: {self.prenom} ...>"