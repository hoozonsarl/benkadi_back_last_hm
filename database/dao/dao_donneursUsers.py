from database.utils import generate_username
from models.donneurs_users import DonneursUsers
from schemas.donneursUsers import DonneurUsersCreate, DonneurUsersUpdate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from pydantic import EmailStr
from passlib.context import CryptContext
from schemas.donneurs import DonneurCreate, DonneurUpdate
from models.donneurs import Donneur
from database.database import SessionLocal
from datetime import datetime

class DaoDonneurUsers():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db


    
    def get_all_donneursUsers(self):
        donneursUsers = self.db.query(DonneursUsers).all()
        return donneursUsers
    

    def get_all_donneursUsers_storage(self, skip: int = 0, limit: int = 100):
        donneursUsers = self.db.query(DonneursUsers).offset(skip).limit(limit).all()
        return donneursUsers
    

    #get all donneursUsers by  userName and dateDeNaissance
    def get_all_donneursUsers_by_userName_and_dateDeNaissance(self, userName: str, dateDeNaissance: datetime):
        donneursUsers = self.db.query(DonneursUsers).filter(DonneursUsers.userName==userName, DonneursUsers.dateDeNaissance==dateDeNaissance).order_by(DonneursUsers.id.desc()).all()
        return donneursUsers
    

     #get donneurUsers by userName and dateDeNaissance
    def get_donneurUsers_by_userName_and_dateDeNaissance(self, userName: str, dateDeNaissance: datetime):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.userName==userName, DonneursUsers.dateDeNaissance==dateDeNaissance).first()
        return donneurUsers


    #get donneurUsers by userName
    def get_donneurUsers_by_userName(self, userName: str):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.userName==userName).first()
        return donneurUsers

    
    def get_donneursUsers_by_pagination(self, skip:int, limit:int):
        donneursUsers = self.db.query(DonneursUsers).offset(skip).limit(limit).all()
        return donneursUsers
    


    def get_donneurUsers_by_email(self, email: EmailStr):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.email==email).first()
        return donneurUsers
    
    def get_donneurUsers_by_numero_cni(self, numeroCNI:int):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.numeroCNI==numeroCNI).first()
        return donneurUsers
    
    def get_donneurUsers_by_telephone(self, telephone: str):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.telephone==telephone).first()
        return donneurUsers
    
    

    def get_donneurUsers_by_id(self, donneurUsers_id: int):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.id==donneurUsers_id).first()
        return donneurUsers

    
            

    def create_new_donneurUsers(self, id_user:int, donneurUsers: DonneurUsersCreate):

        userName = generate_username(donneurUsers.nom, donneurUsers.prenom)

        donneurUsers_db = DonneursUsers(nom=donneurUsers.nom, 
                                   prenom=donneurUsers.prenom, 
                                   userName=userName,
                             dateDeNaissance=donneurUsers.dateDeNaissance, 
                             lieuDeNaissance=donneurUsers.lieuDeNaissance, 
                             numeroCNI=donneurUsers.numeroCNI, 
                             passport=donneurUsers.passport,
                             permisConduire=donneurUsers.permisConduire,
                             carte_scolaire=donneurUsers.carte_scolaire,
                             carte_elec=donneurUsers.carte_elec,
                             carte_etudiant=donneurUsers.carte_etudiant,
                             dateDelivranceIdCard=donneurUsers.dateDelivranceIdCard,
                             villeResidence=donneurUsers.villeResidence,
                             sexe=donneurUsers.sexe, 
                             profession=donneurUsers.profession, 
                             statusMatrimonial=donneurUsers.statusMatrimonial, 
                             paysOrigine=donneurUsers.paysOrigine, 
                             religion=donneurUsers.religion, 
                             adresse=donneurUsers.adresse, 
                             telephone=donneurUsers.telephone, 
                             email=donneurUsers.email, 
                             groupeSanguin=donneurUsers.groupeSanguin, 
                             dateDeProchainDon=donneurUsers.dateDeProchainDon, 
                             dateDernierDon=donneurUsers.dateDernierDon,
                             datePossibleDon=donneurUsers.datePossibleDon,
                             nombreDeDons=donneurUsers.nombreDeDons, 
                             accidentDon=donneurUsers.accidentDon, 
                             dejaTransfuse=donneurUsers.dejaTransfuse, 
                             niveauEtude=donneurUsers.niveauEtude,
                             updatedAt=datetime.now(), 
                             isDelayed=donneurUsers.isDelayed,
                             isDelayedDate=donneurUsers.isDelayedDate,
                             is_don_done=donneurUsers.is_don_done,
                             last_don_date=donneurUsers.last_don_date,
                             final_comment=donneurUsers.final_comment,
                             nombreDeDonsGenyco=donneurUsers.nombreDeDonsGenyco,
                             id_user=id_user, 
                            )
        self.db.add(donneurUsers_db)
        self.db.commit()
        self.db.refresh(donneurUsers_db)
        return donneurUsers_db



    def update_donneurUsers(self, id_donneurUsers: int, donneurUsers_update: DonneurUsersUpdate):
        result = True
        try:
            donneurUsers_update_dict = donneurUsers_update.model_dump()
            filtered = {k: v for k, v in donneurUsers_update_dict.items() if v is not None}
            donneurUsers_update_dict.clear()
            donneurUsers_update_dict.update(filtered) 
            print(donneurUsers_update_dict)
            self.db.query(DonneursUsers).filter(DonneursUsers.id==id_donneurUsers).update(values=donneurUsers_update_dict)
            #self.db.commit()
        except Exception as e:
            print("error in update donneur", e)
            result = False
        return result
    
    # def update_donneurUsers_is_don_done(self, id_donneurUsers: int, groupeSanguin: str , date_prochain_don: datetime):
    #     donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.id==id_donneurUsers).first()
    #     donneurUsers.groupeSanguin = groupeSanguin
    #     donneurUsers.is_don_done = True
    #     donneurUsers.last_don_date = datetime.today().date()
    #     donneurUsers.dateDeProchainDon = date_prochain_don.date()
    #     donneurUsers.nombreDeDonsGenyco = donneurUsers.nombreDeDonsGenyco + 1
    #     donneurUsers.final_comment = "il a effectue un don de sang avec succes"
    #     donneurUsers.isDelayed = False
    #     donneurUsers.isDelayedDate = None
    #     #self.db.commit()
    #     self.db.refresh(donneurUsers)
    #     return donneurUsers

    def update_donneurUsers_is_don_done(self, id_donneurUsers: int, groupeSanguin: str, date_prochain_don: datetime):
        # First, verify the donor user exists
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.id == id_donneurUsers).first()
        if not donneurUsers:
            print(f"Warning: Donor user with ID {id_donneurUsers} not found")
            return None
        
        # Update donor user information
        print("donneurUsers.groupeSanguin", donneurUsers.groupeSanguin)
        donneurUsers.groupeSanguin = groupeSanguin
        donneurUsers.is_don_done = True
        donneurUsers.last_don_date = datetime.today().date()
        donneurUsers.dateDeProchainDon = date_prochain_don.date()
        
        # Handle the None case for donation count
        if donneurUsers.nombreDeDonsGenyco is None:
            donneurUsers.nombreDeDonsGenyco = 1
        else:
            donneurUsers.nombreDeDonsGenyco += 1
        
        donneurUsers.final_comment = "Il a effectué un don de sang avec succès"
        donneurUsers.isDelayed = False
        donneurUsers.isDelayedDate = None
        
        # Don't commit here, but do refresh to load any other changes
        self.db.refresh(donneurUsers)
        return donneurUsers
    


    def update_donneursUsers_is_not_don_done(self, id_donneurUsers: int):
        donneurUsers = self.db.query(DonneursUsers).filter(DonneursUsers.id==id_donneurUsers).first()
        donneurUsers.is_don_done = False
        donneurUsers.last_don_date = datetime.now().date()
        donneurUsers.final_comment = "il y avait un probleme avec le don"
        donneurUsers.isDelayed = False
        donneurUsers.isDelayedDate = None
        #self.db.commit()
        self.db.refresh(donneurUsers)
        return donneurUsers


    def delete_donneurUsers(self, donneurUsers: DonneursUsers):

        self.db.delete(donneurUsers)
        self.db.commit()


    def get_donneur_by_donneurUsers_id(self, id_donneurUsers: int):
        donneurs = self.db.query(Donneur).filter(Donneur.id_donneurUser==id_donneurUsers).order_by(Donneur.id.desc()).all()
        return donneurs



    