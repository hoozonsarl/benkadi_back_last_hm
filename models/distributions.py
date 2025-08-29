from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey, Date, Time
from database.database import Base
from datetime import datetime, date, time



class Distribution(Base):

    __tablename__ = "distributions"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    
    dateDeDistribution: datetime = Column(DateTime, default=datetime.now)

    telephoneTransporteur: str  = Column(String, default="" , nullable=True)
    nomTransporteur: str  = Column(String, default="" , nullable=True)
    cniTransporteur: str = Column(String, default="" , nullable=True)

    nom_hospital_destinataire: str = Column(String, default="" , nullable=True)
    service: str = Column(String, default="" , nullable=True)
    is_interne: bool = Column(Boolean, default=False)

    id_fraction: int  = Column(Integer, ForeignKey("fractions.id"))
    id_user:int = Column(Integer, ForeignKey("users.id"))
    id_bon_de_sang: int = Column(Integer,ForeignKey("bon_de_sangs.id"))

    createdAt: datetime  = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    



