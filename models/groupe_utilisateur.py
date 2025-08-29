from database.database import Base
from sqlalchemy import String, Integer, DateTime, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.users import User


GroupeUtisateurHasPermissions = Table(
    "GroupeUtisateurHasPermissions",
    Base.metadata,
    Column("group_utilisateur_id", ForeignKey("groupeUtilisateurs.id"), nullable=False, primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), nullable=False, primary_key=True),

)


class GroupeUtilisateur(Base):

    __tablename__ = "groupeUtilisateurs"

    id: int  = Column(Integer, primary_key=True, autoincrement=True)
    nom: str = Column(String, nullable=False, unique=True)
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    permissions = relationship("Permission", secondary=GroupeUtisateurHasPermissions, back_populates="groupe_utilisateurs")
    users = relationship("User", back_populates="groupe_utilisateur",cascade="all, delete")


    def __repr__(self):
        return f"<GroupeUtilissteur id: {self.id} nom: {self.nom} ...>"