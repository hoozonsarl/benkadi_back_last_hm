
from sqlalchemy.orm import Session
from sqlalchemy  import String, DateTime, Integer, Column, Enum, Date, Boolean, ForeignKey,Time
from sqlalchemy.orm import relationship
from database.database import Base
from enum import Enum as PyEnum
from datetime import date, datetime, time
from pydantic import EmailStr
from models.receveurs import Sexe
from models.receveurs import GroupeSanguin
from typing import Optional

class Religion(str, PyEnum):
    MUSULMAN = "MUSULMAN"
    CHRETIEN = "CHRETIEN"
    JEHOVAH = "JEHOVAH"
    ANEMIST = "ANEMIST"
    TRADITIONNALIST = "TRADITIONNALIST"
    AUTRE = "AUTRE"
    NON_SPECIFIE = "NON  SPECIFIE"

class StatusMatrimonial(str, PyEnum):
    CELIBATAIRE = "Celibataire"
    MARIE = "Marie(e)"
    DIVORCE = "Divorce"
    VEUVE = "veuf(ve)"

class Donneur(Base):

    __tablename__ = "donneurs"
    id: int = Column(Integer, autoincrement=True, index=True, primary_key=True)
    nom: str = Column(String(50),)
    prenom: str = Column(String(50))
    dateDeNaissance: date = Column(Date,)
    lieuDeNaissance: str  = Column(String(50))
    userName: str = Column(String(80), nullable=False)
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
    isDelayed: bool = Column(Boolean, default=False)
    isDelayedDate: date = Column(Date, nullable=True)
    nombreDeDons: int = Column(Integer, default=0)
    accidentDon: str  = Column(String, nullable=True)
    dejaTransfuse: str = Column(String, nullable=True)
    isDonneur: bool = Column(Boolean, default=False)
    isValideMedecin: Optional[bool] = Column(Boolean, default=False)
    isValideAnalyseTDR: Optional[bool] = Column(Boolean, default=False)
    lu_approve: bool = Column(Boolean, default=False)
    dateAccueil: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    heureAccueil: time = Column(Time, nullable=True, default= lambda : datetime.now().time())
    dateConsultation: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    heureConsultation: time = Column(Time, nullable=True, default= lambda : datetime.now().time())
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_user: int = Column(Integer, ForeignKey("users.id"))
    parametres = relationship("Parametre", back_populates="donneur",cascade="all, delete")
    quartier = Column(String)
    is_tdr_done: bool = Column(Boolean, default=False)
    is_ok_prelevement: bool = Column(Boolean, default=False)
    is_rejected: bool = Column(Boolean, default=False)
    is_prelevement_done: bool = Column(Boolean, default=False)
    is_don_done: bool = Column(Boolean, default=False)
    last_don_date: date = Column(Date, nullable=True, default= lambda : datetime.now().date())
    final_comment: str = Column(String, nullable=True)

    # Add foreign key to reference donneursUsers table
    id_donneurUser: int = Column(Integer, ForeignKey("donneursUsers.id"))
    
    # Add the relationship to DonneursUsers - each Donneurs belongs to one DonneursUsers
    donneurUser = relationship("DonneursUsers", back_populates="donneurs")

    def __repr__(self):
        return  f"<Donneur id: {self.id} numeroCNI: {self.numeroCNI}...>"



