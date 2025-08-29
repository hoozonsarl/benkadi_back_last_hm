from sqlalchemy.orm import Session
from schemas.parametres import ParametreCreate, ParametreUpdate
from models.parametres import Parametre
from datetime import datetime
from fastapi.encoders import jsonable_encoder

class DaoParametre():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_parametre(self):
        parametres = self.db.query(Parametre).all()
        return parametres
    
    def get_parametres_by_pagination(self, skip:int, limit:int):
        parametres = self.db.query(Parametre).skip(skip).limit(limit).all()
        return parametres
    

    def get_parametre_by_id(self, parametre_id: int):
        parametre = self.db.query(Parametre).filter(Parametre.id==parametre_id).first()
        return parametre
    
    def get_parametre_by_donneur_id(self, id_donneur: int):
        parametres = self.db.query(Parametre).filter(Parametre.id_donneur==id_donneur).all()
        return parametres

    def create_new_parametre(self, id_donneur:int, parametre: ParametreCreate):
        parametre_db = Parametre(tensionArterielleBs=parametre.tensionArterielleBs,
                                 tensionArterielleMd=parametre.tensionArterielleMd,
                                 tensionArterielleF=parametre.tensionArterielleF,
                                 nomPatient=parametre.nomPatient,
                                 prenomPatient=parametre.prenomPatient,
                                 serviceSanitaire=parametre.serviceSanitaire,
                                 rythmeCardiaque=parametre.rythmeCardiaque, 
                                 poids=parametre.poids, 
                                 hemoglobine= parametre.hemoglobine, 
                                 depistageVIH=parametre.depistageVIH, 
                                 taille= parametre.taille, 
                                 id_donneur=id_donneur,
                                 updatedAt=datetime.now(), 
                                 raisonDon=parametre.raisonDon, 
                                 raisonDon_aide=parametre.raisonDon_aide, 
                                 raisonDon_remplacer=parametre.raisonDon_remplacer, 
                                 raisonDon_famille= parametre.raisonDon_famille, 
                                 jeune=parametre.jeune, 
                                 affections=parametre.affections, 
                                 hopital=parametre.hopital,
                                 infectionSexulle=parametre.infectionSexulle,
                                   hospitalisation=parametre.hospitalisation, 
                                   bonneSante=parametre.bonneSante, 
                                   malade=parametre.malade, 
                                   fievre=parametre.fievre, 
                                   medicaments=parametre.medicaments, 
                                   vaccine=parametre.vaccine, 
                                   antecedents=parametre.antecedents, 
                                   accident=parametre.accident, 
                                   dentiste=parametre.dentiste, 
                                   endoscopie=parametre.endoscopie, 
                                   acupuncture=parametre.acupuncture, 
                                   tatouage=parametre.tatouage, 
                                   exposition=parametre.exposition, 
                                   testVIH=parametre.testVIH, 
                                   entourageMalade=parametre.entourageMalade, 
                                   rapportSexuel=parametre.rapportSexuel, 
                                   preservatif=parametre.preservatif, 
                                   drogue=parametre.drogue, 
                                   voyageEtranger=parametre.voyageEtranger, 
                                   rapportSexuelHomme=parametre.rapportSexuelHomme, 
                                   grossesse=parametre.grossesse, 
                                   allaitez=parametre.allaitez, 
                                   fausseCouche=parametre.fausseCouche, 
                                   regles=parametre.regles, 
                                   commentaire=parametre.commentaire, 
                                   quantite=parametre.quantite, 
                                   remarques=parametre.remarques, 
                                   benevole=parametre.benevole)
        self.db.add(parametre_db)
        self.db.commit() 
        self.db.refresh(parametre_db)
        return parametre_db

    def get_parametres_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(Parametre).offset(skip).limit(limit).all()


    def update_parametre(self, id_parametre: int, parametre_update: ParametreUpdate):
        result = True
        try:
            parametre_update_dict = parametre_update.model_dump()
            filtered = {k: v for k, v in parametre_update_dict.items() if v is not None}
            parametre_update_dict.clear()
            parametre_update_dict.update(filtered)
            print(parametre_update_dict)
            self.db.query(Parametre).filter(Parametre.id==id_parametre).update(values=parametre_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update Parametre", e)
            result = False
        return result
    

    def delete_parametre(self, parametre: Parametre):

        self.db.delete(parametre)
        self.db.commit()



    