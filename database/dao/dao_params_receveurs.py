from models.params_receveurs import ParamsReceveur
from schemas.params_receveurs import ParamsReceveurCreate, ParamsReceveurUpdate
from sqlalchemy.orm import Session
from pydantic import EmailStr
from passlib.context import CryptContext
from schemas.receveurs import ReceveurCreate, ReceveurUpdate
from models.receveurs import Receveur
from datetime import datetime


class DaoParamsReceveur():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_params_receveurs(self):
        params_receveurs = self.db.query(ParamsReceveur).all()
        return params_receveurs
    
    def get_params_receveurs_by_pagination(self, skip:int, limit:int):
        params_receveurs = self.db.query(ParamsReceveur).skip(skip).limit(limit).all()
        return params_receveurs
    
    

    def get_params_receveur_by_id(self, id_params_receveur: int):
        params_receveur = self.db.query(ParamsReceveur).filter(ParamsReceveur.id==id_params_receveur).first()
        return params_receveur
    


    def create_new_params_receveur(self, id_user:int, params_receveur: ParamsReceveurCreate):
        params_receveur_db = ParamsReceveur(temps=params_receveur.temps,            
                               temperature=params_receveur.temperature, 
                               pression_arterielle =params_receveur.pression_arterielle, 
                               rythme_respiratoire=params_receveur.rythme_respiratoire, 
                               saturation_en_oxygene=params_receveur.saturation_en_oxygene, 
                               pouls=params_receveur.pouls, 
                               ta=params_receveur.ta, 
                               etat_du_malade=params_receveur.etat_du_malade, 
                               frissons=params_receveur.frissons, 
                               sueurs=params_receveur.sueurs, 
                               id_user=id_user,
                               id_bon_de_sang=params_receveur.id_bon_de_sang, 
                               updatedAt=datetime.now())
        self.db.add(params_receveur_db)
        self.db.commit()
        self.db.refresh(params_receveur_db)
        return params_receveur_db

    def get_params_receveurs_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(ParamsReceveur).offset(skip).limit(limit).all()


    def update_params_receveur(self, id_params_receveur: int, params_receveur_update: ParamsReceveurUpdate):
        result = True
        try:
            params_receveur_update_dict = params_receveur_update.model_dump()
            filtered = {k:v for k, v in params_receveur_update_dict.items() if v is not None}
            params_receveur_update_dict.clear()
            params_receveur_update_dict.update(filtered)
            self.db.query(ParamsReceveur).filter(ParamsReceveur.id==id_params_receveur).update(values=params_receveur_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update params receveur", e)
            result = False
        return result
    

    def delete_params_receveur(self, params_receveur: ParamsReceveur):

        self.db.delete(params_receveur)
        self.db.commit()



    