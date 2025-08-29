from database.utils import generate_username
from sqlalchemy.orm import Session
from pydantic import EmailStr
from passlib.context import CryptContext
from schemas.receveurs import ReceveurCreate, ReceveurUpdate
from models.receveurs import Receveur
from datetime import datetime


class DaoReceveur():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_receveurs(self):
        receveurs = self.db.query(Receveur).all()
        return receveurs
    
    def get_receveurs_by_pagination(self, skip:int, limit:int):
        receveurs = self.db.query(Receveur).skip(skip).limit(limit).all()
        return receveurs


    def get_receveur_by_email(self, email: EmailStr):
        receveur = self.db.query(Receveur).filter(Receveur.email==email).first()
        return receveur
    
    def get_receveur_by_telephone(self, telephone: str):
        receveur = self.db.query(Receveur).filter(Receveur.telephone==telephone).first()
        return receveur
    
    def get_receveur_by_userName_and_dateDeNaissance(self, userName: str, dateDeNaissance: datetime):
        receveur = self.db.query(Receveur).filter(Receveur.userName==userName, Receveur.dateDeNaissance==dateDeNaissance).first()
        return receveur
    
    def get_all_receveurs_by_userName_and_dateDeNaissance(self, userName: str, dateDeNaissance: datetime):
        receveurs = self.db.query(Receveur).filter(Receveur.userName==userName, Receveur.dateDeNaissance==dateDeNaissance).order_by(Receveur.id.desc()).all()
        return receveurs
    

    def get_receveur_by_id(self, reveveur_id: int):
        receveur = self.db.query(Receveur).filter(Receveur.id==reveveur_id).first()
        return receveur
    


    def create_new_receveur(self, id_user:int, receveur: ReceveurCreate):
        userName = generate_username(receveur.nom, receveur.prenom)
        receveur_db = Receveur(
            nom=receveur.nom,
            prenom=receveur.prenom, 
            userName=userName,
            dateDeNaissance=receveur.dateDeNaissance, 
            telephone=receveur.telephone, 
            email=receveur.email, 
            sexe=receveur.sexe, 
            groupe_sanguin=receveur.groupe_sanguin,
            groupe_sanguin_receveur=receveur.groupe_sanguin_receveur,
            phenotype=receveur.phenotype,
            id_user=id_user,
            hospital=receveur.hospital,
            service=receveur.service, 
            updatedAt=datetime.now())
        self.db.add(receveur_db)
        self.db.commit()
        self.db.refresh(receveur_db)
        return receveur_db

    def get_receveurs_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(Receveur).offset(skip).limit(limit).all()


    def update_receveur(self, id_receveur: int, receveur_update: ReceveurUpdate):
        result = True
        try:
            receveur_update_dict = receveur_update.model_dump()
            filtered = {k:v for k, v in receveur_update_dict.items() if v is not None}
            receveur_update_dict.clear()
            receveur_update_dict.update(filtered)
            self.db.query(Receveur).filter(Receveur.id==id_receveur).update(values=receveur_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update receveur", e)
            result = False
        return result
    

    def delete_receveur(self, receveur: Receveur):

        self.db.delete(receveur)
        self.db.commit()



    