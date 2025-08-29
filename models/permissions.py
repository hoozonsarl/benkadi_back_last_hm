from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, UniqueConstraint, DateTime, Enum
from models.groupe_utilisateur import GroupeUtisateurHasPermissions
from datetime import datetime
from enum import Enum as PyEnum

class ActionEnum(str, PyEnum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class Permission(Base):

    __tablename__ = "permissions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    action: ActionEnum = Column(Enum(ActionEnum), nullable=False)
    subject: str = Column(String(50), nullable=False)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    groupe_utilisateurs = relationship("GroupeUtilisateur", secondary=GroupeUtisateurHasPermissions, back_populates="permissions")
    __table_args__ = (UniqueConstraint('action', 'subject', name='permission_unique'),)
    
    def __repr__(self):
        return f"<Permision id: {self.id} action: {self.action} subject {self.subject}...>"