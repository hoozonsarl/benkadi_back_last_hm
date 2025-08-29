from sqlalchemy.orm import Session
from models.distributions import Distribution
from schemas.distributions import DistributionCreate, DistributionUpdate 
from datetime import datetime

class DaoDistribution():
    db: Session

    def __init__(self, db: Session):
        self.db = db 

    def get_all_distributions(self,):
        distributions = self.db.query(Distribution).all()
        return distributions
    
    def get_distribution_by_id(self, id_distribution: int):
        distribution = self.db.query(Distribution).filter(Distribution.id==id_distribution).first()
        return distribution
    
    def update_distribution(self, id_distribution, distribution_update: DistributionUpdate):
        result = False
        try:

            distribution_update_dict =  distribution_update.model_dump()
            print(distribution_update_dict)
            self.db.query(Distribution).filter(Distribution.id==id_distribution).update(values=distribution_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during the update distribution", e)
        
        return result

    
    def create_distribution(self, id_user:int, distribution_create : DistributionCreate): 
        distributions = []
        for id_fraction in distribution_create.id_fractions:
            distribution = Distribution(nom_hospital_destinataire=distribution_create.nom_hospital_destinataire, telephoneTransporteur=distribution_create.telephoneTransporteur, nomTransporteur= distribution_create.nomTransporteur, cniTransporteur= distribution_create.cniTransporteur, service = distribution_create.service, is_interne = distribution_create.is_interne, updatedAt=datetime.now(), id_fraction=id_fraction, id_bon_de_sang = distribution_create.id_bon_de_sang, id_user=id_user)
            self.db.add(distribution)
            self.db.commit()
            self.db.refresh(distribution)
            distributions.append(distribution)
        return distributions



    def delete_distribution(self, distribution: Distribution):
        self.db.delete(distribution)
        self.commit()
