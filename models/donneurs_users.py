
from models.donneurs import Religion, StatusMatrimonial
from sqlalchemy.orm import Session
from sqlalchemy  import String, DateTime, Integer, Column, Enum, Date, Boolean, ForeignKey,Time
from sqlalchemy.orm import relationship
from database.database import Base
from enum import Enum as PyEnum
from datetime import date, datetime, time
from pydantic import EmailStr
from models.receveurs import Sexe


class DonneursUsers(Base):

    __tablename__ = "donneursUsers"
    id: int = Column(Integer, autoincrement=True, index=True, primary_key=True)
    nom: str = Column(String(50),)
    prenom: str = Column(String(50))
    userName: str = Column(String(80), nullable=False)
    dateDeNaissance: date = Column(Date,)
    lieuDeNaissance: str  = Column(String(50))
    numeroCNI: str = Column(String(80), nullable=True, unique=False, index=True)
    passport: str = Column(String(80), nullable=True, unique=False, index=True)
    carte_scolaire: str = Column(String(80), nullable=True, unique=False, index=True)
    carte_elec: str = Column(String(80), nullable=True, unique=False, index=True)
    carte_etudiant: str = Column(String(80), nullable=True, unique=False, index=True)
    dateDelivranceIdCard: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    villeResidence: str = Column(String(80), nullable=True)
    niveauEtude: str = Column(String(80), nullable=True)
    permisConduire: str = Column(String(80), nullable=True, unique=False, index=True)
    sexe: Sexe = Column(Enum(Sexe))
    profession: str = Column(String(50))
    statusMatrimonial: StatusMatrimonial = Column(Enum(StatusMatrimonial))
    paysOrigine: str = Column(String(100))
    religion: Religion = Column(Enum(Religion))
    adresse: str  = Column(String(100))
    telephone: str = Column(String(20))
    email: str = Column(String(30), nullable=True)
    groupeSanguin: str = Column(String, nullable=True, default=None)
    dateDeProchainDon: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    dateDernierDon: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    datePossibleDon: date  = Column(Date, nullable=True)
    nombreDeDons: int = Column(Integer, default=0)
    accidentDon: str  = Column(String, nullable=True)
    dejaTransfuse: str = Column(String, nullable=True)
    isDelayed: bool = Column(Boolean, default=False)
    isDelayedDate: date = Column(Date, nullable=True)
    is_don_done: bool = Column(Boolean, default=False)
    last_don_date: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    final_comment: str = Column(String, nullable=True)
    nombreDeDonsGenyco: int = Column(Integer, default=0)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_user: int = Column(Integer, ForeignKey("users.id"))

     # Add the relationship to Donneurs - one DonneursUsers can have many Donneurs
    donneurs = relationship("Donneur", back_populates="donneurUser", cascade="all, delete-orphan")

    def __repr__(self):
        return  f"<DonneurUsers id: {self.id} userName: {self.userName} numeroCNI: {self.numeroCNI}...>"



