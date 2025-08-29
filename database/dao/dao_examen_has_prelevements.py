from sqlalchemy.orm import Session
from models.examens import ExamenHasPrelevement
from schemas.examen_has_prelevements import ExamenHasPrelevementCreate, ExamenHasPrelevementUpdate

class DaoExamenHasPrelevement():
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_examen_has_prelevement(self):
        examen_has_prelevements = self.db.query(ExamenHasPrelevement).all()
        return examen_has_prelevements
    
    def get_all_examen_has_prelevements(self, id_examen:int, id_prelevement:int):
        examen_has_prelevement = self.db.query(ExamenHasPrelevement).filter(ExamenHasPrelevement.id_examen==id_examen, ExamenHasPrelevement.id_prelevement==id_prelevement).first()
        return examen_has_prelevement

    def get_all_examen_has_prevelement_by_prelevement_id(self, id_prelevement: int):
        examen_has_prelevements_by_prelevement_id = self.query(ExamenHasPrelevement).filter(ExamenHasPrelevement.id_prelevement==id_prelevement).all()
        return examen_has_prelevements_by_prelevement_id
    
    def get_all_examen_has_prevelement_by_examen_id(self, id_examen: int):
        examen_has_prelevements_by_examen_id = self.query(ExamenHasPrelevement).filter(ExamenHasPrelevement.id_examen==id_examen).all()
        return examen_has_prelevements_by_examen_id
    
    def create_new_examen_has_prelevement(self, examen_has_prelevement: ExamenHasPrelevementCreate):
        examen_has_prelevement = ExamenHasPrelevement(id_examen=examen_has_prelevement.id_examen, id_prelevement=examen_has_prelevement.id_prelevement, valeur=examen_has_prelevement.valeur, isReactif=examen_has_prelevement.isReactif)
        self.db.add(examen_has_prelevement)
        self.db.commit()
        self.db.refresh(examen_has_prelevement)
        return examen_has_prelevement
    
    def update_examen_has_prelevement(self, id_examen, id_prelevement, examen_has_prelevement_update: ExamenHasPrelevementUpdate):
        result =  False
        try:
            examen_has_prelevement_update_dict = examen_has_prelevement_update.model_dump()
            print(examen_has_prelevement_update_dict)

            self.db.query(ExamenHasPrelevement).filter(ExamenHasPrelevement.id_examen==id_examen, ExamenHasPrelevement.id_prelevement==id_prelevement).update(examen_has_prelevement_update_dict)
            self.db.commit()
            result = True

        except Exception as e:
            print("Error durint the update Examen Has Prelevement", e)
        return result
    
    def delete_examen_has_prelevement(self, examen_has_prelevement: ExamenHasPrelevement):
        self.db.delete(examen_has_prelevement)
        self.db.commit()