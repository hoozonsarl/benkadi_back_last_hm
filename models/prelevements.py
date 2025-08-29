from database.database import Base
from sqlalchemy import Integer, String, Date, DateTime,ForeignKey, Column, Time, Enum, Boolean
from datetime import datetime, time
from enum import Enum as PyEnum
from uuid import uuid4, UUID
from sqlalchemy.orm import Relationship, relationship
from datetime import date
from cachetools import TTLCache
from database.database import SessionLocal
from sqlalchemy import and_, cast

class VolumePrevele(int, PyEnum):
    VOLUME1 = 250
    VOLUME2 = 450




class Prelevement(Base):

    __tablename__ = "prelevements"

    _id_cache = TTLCache(maxsize=1, ttl=86400)  # Cache for 24 hours
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    numero_code_bar: str  = Column(String, unique=True)
    codeBar: str = Column(String, nullable=False, unique=True)
    dateDePrelevement: date = Column(Date,)
    heureDebut: time =  Column(Time)
    heureFin: time = Column(Time)
    poidsDePoche: int = Column(Integer)
    volumePrevele: int = Column(Integer)
    remarques: str  = Column(String)
    effetsIndesirables: str = Column(String)
    estAnalyser: bool = Column(Boolean, default=False)
    id_donneur: int =  Column(Integer, ForeignKey("donneurs.id", ondelete='CASCADE'))
    id_parametre: int = Column(Integer, ForeignKey("parametres.id", ondelete='CASCADE'))
    id_user: int  = Column(Integer, ForeignKey("users.id"))
    parametres = relationship("Parametre", back_populates="poche_de_sang", cascade='all, delete')
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # examens = Relationship("Examen", secondary="examenHasPrelevements", cascade='all, delete')
    poche_de_sang = Relationship("PocheDeSang", back_populates='prelevement', cascade='all, delete', uselist=False)
    code_diff: str = Column(String)
    is_phenotype_done: bool = Column(Boolean, default=False)


    def __init__(self, **kwargs):
        db = SessionLocal()
        today = date.today()
        if today not in self._id_cache :
            last_id = db.query(Prelevement).filter(cast(Prelevement.createdAt, Date) == today).count() # Count for today's records
            self._id_cache[today] = int(f"{today.strftime('%Y%m%d')}{last_id + 1}")
        self.id = self._id_cache[today]
        self._id_cache[today] += 1
        super().__init__(**kwargs)

    def __repr__(self):

        return f"<Prelevement id : {self.id}, dateDePrelevement: {self.dateDePrelevement} heureDebut: {self.heureDebut} heureFin: {self.heureDebut} poidsDePoche: {self.poidsDePoche} "



