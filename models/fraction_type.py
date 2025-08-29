from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey
from database.database import Base
from datetime import datetime
from sqlalchemy.orm import Relationship

class FractionType(Base):

    __tablename__ = "fractionTypes"

    id: int  = Column(Integer, autoincrement=True, primary_key=True)
    nom: str = Column(String, nullable=False, unique=True, index=True)
    nombreDeJourExpiration: int = Column(Integer, default=0)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_default_selected: bool = Column(Boolean, default=False)
    code: str = Column(String, unique=True)
    fraction = Relationship("Fraction", back_populates="type_de_fraction", uselist=False)
    quarantaine: int = Column(Integer, default=0)
    is_total: bool = Column(Boolean, default=False)

    def __repr__(self, ):
        return f"<FractionType id: {self.id} nom: {self.nom} nombreDeJourExpiration:{self.nombreDeJourExpiration}...>"