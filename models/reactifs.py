from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey, Date, Time, Float
from database.database import Base
from datetime import datetime, date, time



class Reactif(Base):

    __tablename__ = "reactifs"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    nom: str = Column(String(50))
    reference: str = Column(String(50), nullable=True)
    quantite: int = Column(Integer, nullable=True)
    valeur_seuil: float = Column(Float, nullable=True)
    numero_code_bar: str  = Column(String, unique=True)
    codeBar: str = Column(String, nullable=False, unique=True)
    numero_lot: str = Column(String, nullable=True)
    date_expiration: date = Column(Date, nullable=True)
    date_production: date = Column(Date, nullable=True)
    is_deleted: bool = Column(Boolean, default=False)
    id_user: int = Column(Integer, ForeignKey("users.id"))

    createdAt: datetime  = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    



