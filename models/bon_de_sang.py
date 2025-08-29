from models.receveurs import Sexe
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime, Time, Boolean, Float
from sqlalchemy.orm import Relationship
from database.database import Base
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from datetime import time, date, datetime


class BonDeSang(Base):

    __tablename__ = "bon_de_sangs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nom: str = Column(String(50), nullable=False)
    prenom: str =  Column(String(50), nullable=True)
    userName: str = Column(String(80), nullable=False)
    dateDeNaissance: date = Column(Date)
    telephone: str = Column(String(100), nullable=True)
    sexe: Sexe = Column(Enum(Sexe), default=Sexe.HOMME)
    email: str = Column(String(100), nullable=True)
    patient_interne: bool = Column(Boolean, default=False)
    poids: int  = Column(Integer, nullable=True)
    chambre: str = Column(String, nullable=True)
    lit: str = Column(String, nullable=True)
    heure_demande: time = Column(Time, nullable=True)
    antecedent_medicaux: str = Column(String, nullable=True)
    indication: str = Column(String, nullable=True)
    statusVIH: bool = Column(Boolean, default=False)
    statusVHB: bool = Column(Boolean, default=False)
    statusVHC: bool = Column(Boolean, default=False)
    groupe_sanguin: str = Column(String, nullable=True)
    groupe_sanguin_receveur: str = Column(String, nullable=True)
    groupe_sanguin_nouveau_ne: str = Column(String, nullable=True)
    phenotype: str = Column(String, nullable=True)
    nature_du_produit_sanguin: str = Column(String, nullable=True)
    nombre_de_poches: int = Column(Integer, nullable=True)
    antecedent_transfusionnel: int = Column(Integer, nullable=True)
    RAI_positif: bool = Column(Boolean, default=False)
    taux_hemoglobine: float = Column(Float, nullable=True)
    programme: date = Column(Date, nullable=True)
    heure: time = Column(Time, nullable=True)
    hospital: str = Column(String, nullable=True)
    service: str = Column(String, nullable=True)
    medecin_demandeur: str = Column(String, nullable=True)
    specialité: str = Column(String, nullable=True)
    estDistribue: bool = Column(Boolean, default=False)
    id_user: int  = Column(Integer, ForeignKey("users.id"))
    examens: str = Column(String, default="")
    estAnalyse: bool = Column(Boolean, default=False)
    is_phenotype_done: bool = Column(Boolean, default=False)
    is_test_compatibilite_done: bool = Column(Boolean, default=False)
    date_transfusion: date = Column(Date, nullable=True)
    date_reception: date = Column(Date, nullable=True)
    date_retour_poche: date = Column(Date, nullable=True)
    motif: str = Column(String, nullable=True)
    test_compatibilite: str = Column(String, nullable=True)
    params_receveurs = relationship("ParamsReceveur", back_populates="bon_de_sang", 
                                  cascade="all, delete-orphan")
    
    id_receveur = Column(Integer, ForeignKey("receveurs.id"))
    receveur = relationship("Receveur", back_populates="bon_de_sangs")
    


    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now) 

    


