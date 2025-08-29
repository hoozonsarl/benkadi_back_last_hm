from sqlalchemy.orm import Session
from schemas.hostipals import HospitalCreate, HospitalResponseModel, HospitalUpdate
from models.hospitals import Hospital
from datetime import datetime

class DaoHospital():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_hospitals(self):
        groupe_utilisateurs = self.db.query(Hospital).all()
        return groupe_utilisateurs
    
    def get_hospital_by_name(self, nom: str):
        hospital = self.db.query(Hospital).filter(Hospital.nom==nom).first()
        return hospital


    def get_hospital_by_id(self, hospital_id: int):
        hospital = self.db.query(Hospital).filter(Hospital.id==hospital_id).first()
        return hospital

    def update_hospital(self, id_hospital:int,  hospital_update: HospitalUpdate ):
        result = False
        try:

            hospital_update_dict = hospital_update.model_dump()
            self.db.query(Hospital).filter(Hospital.id==id_hospital).update(hospital_update_dict)
            self.db.commit()
            result = True

        except Exception as e:
            print("Error durint update hospital ", e)
        return result

    def create_new_hospital(self, id_user:int, hospital: HospitalCreate):
        hospital_db = Hospital(nom=hospital.nom, ville= hospital.ville, id_user=id_user, updatedAt=datetime.utcnow())
        self.db.add(hospital_db)
        self.db.commit()
        self.db.refresh(hospital_db)
        return hospital_db

    def get_groupe_hospitals_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(Hospital).offset(skip).limit(limit).all()


    def delete_hospital(self, hospital: Hospital):
        self.db.delete(hospital)
        self.db.commit()