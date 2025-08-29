from sqlalchemy.orm import Session
from models.poches_de_sangs import PocheDeSang
from schemas.poches_de_sangs import PocheDeSangCreate, PocheDeSangUpdate
from datetime import datetime
from sqlalchemy import and_

class DaoPocheDeSang():
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def get_all_poche_de_sangs(self, estFractionne = False, is_phenotype_done = False, estDetruire = False):
        poche_de_sangs = self.db.query(PocheDeSang).filter(and_(PocheDeSang.estFractionne == estFractionne, PocheDeSang.is_phenotype_done==is_phenotype_done, PocheDeSang.estDetruire==estDetruire)).all()
        return poche_de_sangs
    

    #get poche of a donneur
    def get_poche_of_a_donneur(self, id_donneur: int):
        poche_de_sangs = self.db.query(PocheDeSang).filter(PocheDeSang.id_donneur == id_donneur).first()
        print("poche_de_sangs",poche_de_sangs)
        return poche_de_sangs
    
    def get_all_poche_de_sangs_without_analyse_done(self):
        poche_de_sangs = self.db.query(PocheDeSang).filter(PocheDeSang.isAnalyseDone == False ).all()
        return poche_de_sangs
    
    def get_all_poche_de_sangs_destroy(self):
        poche_de_sangs = self.db.query(PocheDeSang).filter(PocheDeSang.estDetruire == True ).all()
        return poche_de_sangs
    
    def get_all_poche_de_sangs_with_analyse_done(self):
        poche_de_sangs = self.db.query(PocheDeSang).filter(PocheDeSang.isAnalyseDone == True , PocheDeSang.estDetruire == False , PocheDeSang.estvalide == False).all()
        return poche_de_sangs
    
    def get_poche_de_sangs_by_pagination(self, estFractionne: False, estDetruire = False, skip = 0, limit = 100):
        poche_de_sangs = self.db.query(PocheDeSang).filter(and_(PocheDeSang.estFractionne == estFractionne, estDetruire=estDetruire)).offset(skip).limit(limit).all()
        return poche_de_sangs

    def get_poche_de_sang_by_id(self, id_poche_de_sang:int):
        poche_de_sang = self.db.query(PocheDeSang).filter(PocheDeSang.id==id_poche_de_sang).first()
        return poche_de_sang
    
    def get_poche_de_sang_by_numero_code_bar(self, numero_code_bar: str):
        poche_de_sang = self.db.query(PocheDeSang).filter(PocheDeSang.numero_code_bar==numero_code_bar).first()
        return poche_de_sang
    
    def  create_new_poche_de_sang(self,id_user:int, poche_de_sang_create: PocheDeSangCreate):
        poche_de_sang = PocheDeSang(groupeSanguin=poche_de_sang_create.groupeSanguin, 
                                    phenotype=poche_de_sang_create.phenotype, 
                                    dateAnalyse=poche_de_sang_create.dateAnalyse, 
                                    estvalide=poche_de_sang_create.estvalide, 
                                    id_prelevement=poche_de_sang_create.id_prelevement, 
                                    id_donneur=poche_de_sang_create.id_donneur, 
                                    id_user=id_user, 
                                    motifDestruction=poche_de_sang_create.motifDestruction, 
                                    observation= poche_de_sang_create.observation, 
                                    updatedAt=datetime.now(), 
                                    is_phenotype_done=poche_de_sang_create.is_phenotype_done,
                                    examens=poche_de_sang_create.examens)
        self.db.add(poche_de_sang)
        self.db.commit()
        self.db.refresh(poche_de_sang)
        return poche_de_sang
    
    def update_poche_de_sang(self,id_poche_de_sang:int, poche_de_sang_update: PocheDeSangUpdate ):
        result = True
        try:
            poche_de_sang_update_dict = poche_de_sang_update.model_dump()
            filtered = {k: v for k, v in poche_de_sang_update_dict.items() if v is not None}
            poche_de_sang_update_dict.clear()
            poche_de_sang_update_dict.update(filtered)
            self.db.query(PocheDeSang).filter(PocheDeSang.id==id_poche_de_sang).update(values=poche_de_sang_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update Permission", e)
            result = False
        return result
    
    def delete_poche_de_sang(self, poche_de_sang: PocheDeSang):
        self.db.delete(poche_de_sang)
        self.db.commit()

