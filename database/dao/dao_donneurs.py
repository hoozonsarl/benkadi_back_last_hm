from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import EmailStr
from passlib.context import CryptContext
from schemas.donneurs import DonneurCreate, DonneurUpdate
from models.donneurs import Donneur
from database.database import SessionLocal
from datetime import datetime
from typing import Optional

class DaoDonneur():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_donneurs(self, isValideMedecin: Optional[bool]= None , isValideAnalyseTDR: Optional[bool] = None, is_tdr_done: Optional[bool] = None, is_ok_prelevement: Optional[bool] = None):
        donneurs = self.db.query(Donneur).filter(and_(Donneur.isValideMedecin==isValideMedecin, Donneur.isValideAnalyseTDR==isValideAnalyseTDR, Donneur.is_tdr_done==is_tdr_done, Donneur.is_ok_prelevement==is_ok_prelevement)).filter(Donneur.dateDeProchainDon<=datetime.today().date()).all()
        return donneurs
    
    def get_all_donneurs(self):
        donneurs = self.db.query(Donneur).filter(Donneur.isValideMedecin==False, Donneur.isDelayed==False , Donneur.is_rejected==False).all()
        return donneurs
    
    def get_temp_donneurs(self):
        donneurs = self.db.query(Donneur).filter(Donneur.is_tdr_done==False, Donneur.isDelayed==True).all()
        return donneurs


    def get_donneurs_by_is_tdr_done(self):
        donneurs = self.db.query(Donneur).filter(Donneur.is_tdr_done==True, Donneur.is_rejected==False , Donneur.is_ok_prelevement==False).all()
        return donneurs
    
    def get_donneurs_by_is_ok_prelevement(self):
        donneurs = self.db.query(Donneur).filter(Donneur.is_tdr_done==True, Donneur.is_ok_prelevement==True, Donneur.is_rejected==False , Donneur.is_prelevement_done==False).all()
        return donneurs
    
    def get_donneurs_by_is_rejected(self):
        donneurs = self.db.query(Donneur).filter(Donneur.is_ok_prelevement==False, Donneur.is_rejected==True ).all()
        return donneurs
    
    def get_donneurs_by_pagination(self, isDonneur: bool, skip:int, limit:int):
        donneurs = self.db.query(Donneur).filter(Donneur.isDonneur == isDonneur).offset(skip).limit(limit).all()
        return donneurs
    


    def get_donneur_by_email(self, email: EmailStr):
        donneur = self.db.query(Donneur).filter(Donneur.email==email).first()
        return donneur
    
    def get_donneur_by_numero_cni(self, numeroCNI:int):
        donneur = self.db.query(Donneur).filter(Donneur.numeroCNI==numeroCNI).first()
        return donneur
    
    def get_donneur_by_telephone(self, telephone: str):
        donneur = self.db.query(Donneur).filter(Donneur.telephone==telephone).first()
        return donneur
    
    

    def get_donneur_by_id(self, donneur_id: int):
        donneur = self.db.query(Donneur).filter(Donneur.id==donneur_id).first()
        return donneur
    
            

    def create_new_donneur(self, id_user:int, donneur: DonneurCreate, id_donneurUser:int , userName: str):
        donneur_db = Donneur(nom=donneur.nom, prenom=donneur.prenom, 
                             dateDeNaissance=donneur.dateDeNaissance, 
                             userName=userName,
                             lieuDeNaissance=donneur.lieuDeNaissance, 
                             numeroCNI=donneur.numeroCNI, 
                             passport=donneur.passport,
                             permisConduire=donneur.permisConduire,
                             carte_scolaire=donneur.carte_scolaire,
                             carte_elec=donneur.carte_elec,
                             carte_etudiant=donneur.carte_etudiant,
                             dateDelivranceIdCard=donneur.dateDelivranceIdCard,
                             villeResidence=donneur.villeResidence,
                             sexe=donneur.sexe, 
                             profession=donneur.profession, 
                             statusMatrimonial=donneur.statusMatrimonial, 
                             paysOrigine=donneur.paysOrigine, 
                             religion=donneur.religion, 
                             adresse=donneur.adresse, 
                             telephone=donneur.telephone, 
                             email=donneur.email, 
                             groupeSanguin=donneur.groupeSanguin, 
                             dateDeProchainDon=donneur.dateDeProchainDon, 
                             dateDernierDon=donneur.dateDernierDon,
                             datePossibleDon=donneur.datePossibleDon,
                             isDelayed=donneur.isDelayed,
                             isDelayedDate=donneur.isDelayedDate,
                             nombreDeDons=donneur.nombreDeDons, 
                             accidentDon=donneur.accidentDon, 
                             dejaTransfuse=donneur.dejaTransfuse, 
                             niveauEtude=donneur.niveauEtude,
                             dateAccueil=donneur.dateAccueil,
                             heureAccueil=donneur.heureAccueil,
                             dateConsultation=donneur.dateConsultation,
                             heureConsultation=donneur.heureConsultation,
                             updatedAt=datetime.now(), 
                             id_user=id_user, 
                             quartier=donneur.quartier, 
                             is_tdr_done=donneur.is_tdr_done,
                             is_ok_prelevement=donneur.is_ok_prelevement,
                             is_rejected=donneur.is_rejected,
                             is_prelevement_done=donneur.is_prelevement_done,
                             lu_approve=donneur.lu_approve,
                             is_don_done=donneur.is_don_done,
                             last_don_date=donneur.last_don_date,
                             final_comment=donneur.final_comment,
                             id_donneurUser=id_donneurUser)
        self.db.add(donneur_db)
        self.db.commit()
        self.db.refresh(donneur_db)
        return donneur_db

    def get_receveurs_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(Donneur).offset(skip).limit(limit).all()


    def update_donneur(self, id_donneur: int, donneur_update: DonneurUpdate):
        result = True
        try:
            donneur_update_dict = donneur_update.model_dump()
            filtered = {k: v for k, v in donneur_update_dict.items() if v is not None}
            donneur_update_dict.clear()
            donneur_update_dict.update(filtered) 
            print(donneur_update_dict)
            self.db.query(Donneur).filter(Donneur.id==id_donneur).update(values=donneur_update_dict)
            #self.db.commit()
        except Exception as e:
            print("error in update donneur", e)
            result = False
        return result
    
    def update_after_prelevment(self, id_donneur:int):
        data = {"isValideMedecin": None, "isValideAnalyseTDR": None}
        self.db.query(Donneur).filter(Donneur.id==id_donneur).update(values=data)
        self.db.commit()
    

    def delete_donneur(self, donneur: Donneur):

        self.db.delete(donneur)
        self.db.commit()



    