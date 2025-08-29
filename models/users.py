from database.database import Base
from pydantic import EmailStr
from sqlalchemy import Column, String, Integer, Enum, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import date, datetime

class Gender(str, PyEnum):
    MALE = "MALE"
    FEMALE  = "FEMALE"
    NONBINARY = "NONBINARY"
    UNKNOWN = "UNKNOWN"


class User(Base):
    __tablename__ = "users"


    id: int = Column(Integer, primary_key=True, index=True)
    email : EmailStr = Column(String(50), index=True, unique=True, nullable=False)
    gender : Gender = Column(Enum(Gender), default=Gender.UNKNOWN)
    password: str = Column(String(), nullable=False)
    dateNaissance: date = Column(Date)
    intituleDuPoste: str = Column(String(100))
    telephone: str = Column(String(100))
    nom: str = Column(String(50))
    prenom: str = Column(String(50))
    nationality: str = Column(String(50))
    createdAt: datetime= Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_groupe_utilisateur: int = Column(Integer, ForeignKey("groupeUtilisateurs.id", ondelete='CASCADE'), nullable=False)
    groupe_utilisateur = relationship("GroupeUtilisateur", back_populates="users")
    





    def __repr__(self):
        return f"<User id: {self.id} email:{self.email} ...>"