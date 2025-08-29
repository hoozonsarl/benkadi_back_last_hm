from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey, Enum, Date
from database.database import Base
from datetime import datetime, date
from sqlalchemy.orm import Relationship

class Fraction(Base):

    __tablename__ = "fractions"

    id: int  = Column(Integer, autoincrement=True, primary_key=True)
    id_poche_de_sang:int = Column(Integer, ForeignKey("pocheDeSangs.id"))
    dateDePrelevement: date = Column(Date)
    dateDeExpiration: date = Column(Date)
    volume: int = Column(Integer)
    poids: int  = Column(Integer)
    estDistribue: bool = Column(Boolean, default=False)
    is_valid: bool = Column(Boolean, default=False)
    is_analyse_done: bool = Column(Boolean, default=False)
    estArchive: bool = Column(Boolean, default=False)
    id_fraction_type: int = Column(Integer, ForeignKey("fractionTypes.id"))
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    poche_de_sang = Relationship("PocheDeSang", back_populates="fractions")
    type_de_fraction = Relationship("FractionType", back_populates="fraction", uselist=False)
    numero_code_bar: str = Column(String)
    code_bar: str = Column(String)
    dateAvailable: date = Column(Date)
    is_ok_to_use: bool = Column(Boolean, default=False)
    is_destroy: bool = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Fraction id: {self.id} code: {self.code_bar} ...>"

