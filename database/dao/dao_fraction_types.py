from sqlalchemy.orm import Session
from schemas.fraction_types import FractionTypeResponseModel, FractionTypeCreate, FractionTypeUpdate 
from models.fraction_type import FractionType
from datetime import datetime






class DaoFractionType():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_fraction_types(self):
        fraction_types = self.db.query(FractionType).all()
        return fraction_types

    def get_fraction_type_by_id(self, fraction_type_id: int):
        fraction_type = self.db.query(FractionType).filter(FractionType.id==fraction_type_id).first()
        return fraction_type
    
    def get_fraction_type_by_name(self, nom: str):
        fraction_type = self.db.query(FractionType).filter(FractionType.nom==nom).first()
        return fraction_type

    def update_fraction_type(self, id_fraction_type:int, fraction_type_update: FractionTypeUpdate):
        result = False
        try:

            fraction_type_update_dict = fraction_type_update.model_dump()
            self.db.query(FractionType).filter(FractionType.id==id_fraction_type).update(fraction_type_update_dict)
            self.db.commit()
            result = True

        except Exception as e:
            print("Error durint update group user ", e)
        return result

    def create_new_fraction_type(self, fraction_type: FractionTypeCreate):
        fraction_type_db = FractionType(nom=fraction_type.nom, nombreDeJourExpiration=fraction_type.nombreDeJourExpiration, updatedAt=datetime.now(), is_default_selected=fraction_type.is_default_selected, code=fraction_type.code, quarantaine = fraction_type.quarantaine, is_total = fraction_type.is_total)
        self.db.add(fraction_type_db)
        self.db.commit()
        self.db.refresh(fraction_type_db)
        return fraction_type_db

    def get_groupe_utilisateurs_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(FractionType).offset(skip).limit(limit).all()


    def delete_fraction_type(self, fraction_type: FractionType):
        self.db.delete(fraction_type)
        self.db.commit()



    