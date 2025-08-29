from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from models.bon_de_sang import BonDeSang
from schemas.bon_de_sang import BonDeSangCreate, BonDeSangUpdate, BonDeSangResponseModel


class DaoBonDeSang():
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    
    def get_all_bon_de_sangs(self):
        bon_de_sangs = self.db.query(BonDeSang).all()
        return bon_de_sangs

    def get_list_bon_de_sangs(self, estDistribue: Optional[bool] = None, estAnalyse: Optional[bool] = None, is_phenotype_done: Optional[bool] = None, is_test_compatibilite_done: Optional[bool] = None):
        bon_de_sangs = self.db.query(BonDeSang).filter(BonDeSang.estDistribue==estDistribue, BonDeSang.estAnalyse==estAnalyse, BonDeSang.is_phenotype_done==is_phenotype_done, BonDeSang.is_test_compatibilite_done==is_test_compatibilite_done).all()
        return bon_de_sangs


    def get_bon_de_sang_by_id(self, id_bon_de_sang: int):
        bon_de_sang = self.db.query(BonDeSang).filter(BonDeSang.id==id_bon_de_sang).first()
        return bon_de_sang
    
    def update_bon_de_sang(self, id_bon_de_sang: int, bon_de_sang_update: BonDeSangUpdate):
        result = False
        try:
            bon_de_sang_update_dict =  bon_de_sang_update.model_dump()
            filtered = {k:v for k, v in bon_de_sang_update_dict.items() if v is not None}
            bon_de_sang_update_dict.clear()
            bon_de_sang_update_dict.update(filtered)
            self.db.query(BonDeSang).filter(BonDeSang.id==id_bon_de_sang).update(values=bon_de_sang_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during the update distribution", e)

        return result
    
    def create_bon_de_sang(self, id_user: int, bon_de_sang_create: BonDeSangCreate, id_receveur: int, userName: str):

        if bon_de_sang_create.patient_interne == False:
            bon_de_sang_create.estAnalyse = True
        else:
            bon_de_sang_create.estAnalyse = False

        bon_de_sang = BonDeSang(poids=bon_de_sang_create.poids, 
                                nom=bon_de_sang_create.nom, 
                                prenom=bon_de_sang_create.prenom, 
                                dateDeNaissance=bon_de_sang_create.dateDeNaissance, 
                                userName=userName,
                                telephone=bon_de_sang_create.telephone, 
                                sexe=bon_de_sang_create.sexe, 
                                email=bon_de_sang_create.email,
                                patient_interne=bon_de_sang_create.patient_interne,
                                chambre=bon_de_sang_create.chambre, 
                                lit=bon_de_sang_create.lit, 
                                heure_demande=bon_de_sang_create.heure_demande,
                                antecedent_medicaux=bon_de_sang_create.antecedent_medicaux, 
                                indication=bon_de_sang_create.indication, 
                                statusVIH=bon_de_sang_create.statusVIH, 
                                statusVHB=bon_de_sang_create.statusVHB, 
                                statusVHC=bon_de_sang_create.statusVHC, 
                                groupe_sanguin=bon_de_sang_create.groupe_sanguin, 
                                groupe_sanguin_receveur=bon_de_sang_create.groupe_sanguin_receveur,
                                groupe_sanguin_nouveau_ne=bon_de_sang_create.groupe_sanguin_nouveau_ne, 
                                phenotype=bon_de_sang_create.phenotype, 
                                nature_du_produit_sanguin=bon_de_sang_create.nature_du_produit_sanguin, 
                                nombre_de_poches=bon_de_sang_create.nombre_de_poches,  
                                antecedent_transfusionnel=bon_de_sang_create.antecedent_transfusionnel, 
                                taux_hemoglobine=bon_de_sang_create.taux_hemoglobine, 
                                RAI_positif=bon_de_sang_create.RAI_positif, 
                                programme=bon_de_sang_create.programme, 
                                heure=bon_de_sang_create.heure, 
                                hospital=bon_de_sang_create.hospital, 
                                service=bon_de_sang_create.service, 
                                medecin_demandeur=bon_de_sang_create.medecin_demandeur, 
                                specialité=bon_de_sang_create.specialité, 
                                examens=bon_de_sang_create.examens, 
                                estAnalyse=bon_de_sang_create.estAnalyse, 
                                date_transfusion=bon_de_sang_create.date_transfusion, 
                                date_reception=bon_de_sang_create.date_reception, 
                                date_retour_poche=bon_de_sang_create.date_retour_poche, 
                                motif=bon_de_sang_create.motif, 
                                test_compatibilite=bon_de_sang_create.test_compatibilite, 
                                is_phenotype_done=bon_de_sang_create.is_phenotype_done, 
                                is_test_compatibilite_done=bon_de_sang_create.is_test_compatibilite_done, 
                                estDistribue=bon_de_sang_create.estDistribue,
                                id_receveur=id_receveur,
                                id_user=id_user)
        self.db.add(bon_de_sang)
        self.db.commit()
        self.db.refresh(bon_de_sang)
        return bon_de_sang


    def put_distribute(self, id_bon_de_sang):

        result = False
        try:

            bon_de_sang_update = {"estDistribue": True}
            self.db.query(BonDeSang).filter(BonDeSang.id==id_bon_de_sang).update(values=bon_de_sang_update)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during archive bon de sang", e)
        return result
        

    def delete(self, bon_de_sang: BonDeSang):
        self.db.delete(bon_de_sang)
        self.db.commit()