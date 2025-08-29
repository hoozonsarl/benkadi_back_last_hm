from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Relationship
from database.database import Base
from datetime import datetime

class Logs(Base):

    __tablename__ = "logs"
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    action: str = Column(String,nullable=True)
    nom_utilisateur: str = Column(String,nullable=True)
    date_action: datetime = Column(DateTime, default=datetime.now)
    ressource: str = Column(String,nullable=True)
    status: str = Column(String,nullable=True)
    id_utilisateur: int = Column(Integer,nullable=True)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self,):
        return f"<Logs id: {self.id} action: {self.action} ...>"