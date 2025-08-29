from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Relationship
from database.database import Base
from datetime import datetime

class Hospital(Base):

    __tablename__ = "hospitals"
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    nom: str = Column(String)
    ville: str  = Column(String)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_user:int = Column(Integer, ForeignKey("users.id"))
    # receveurs = Relationship("Receveur", back_populates="hospital", cascade="all, delete")
    __table_args__ = (UniqueConstraint('nom', 'ville', name='hospital_unique'),)

    def __repr__(self,):
        return f"<Hospital id: {self.id} nom: {self.nom} ...>"