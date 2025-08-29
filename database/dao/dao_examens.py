# from sqlalchemy.orm import Session
# from models.examens import Examen
# from schemas.examens import ExamenCreate, ExamenUpdate
# from datetime import datetime

# class DaoExamen():
#     db: Session


#     def __init__(self, db: Session):
#         self.db = db

#     def get_all_examens(self):
#         examens = self.db.query(Examen).all()
#         return examens
    
#     def get_examen_by_id(self, id_examen: int):
#         examen = self.db.query(Examen).filter(Examen.id==id_examen).first()
#         return examen
    
#     def create_new_examen(self, id_user:int, examen_create: ExamenCreate):
#         examen = Examen(nom=examen_create.nom,id_user = id_user)
#         self.db.add(examen)
#         self.db.commit()
#         self.db.refresh(examen)
#         return examen
    
#     def update_examen(self, id_examen, examen_update: ExamenUpdate):
#         result = False
#         try:
#             examen_update_dict = examen_update.model_dump()
#             print(examen_update_dict)
#             self.db.query(Examen).filter(Examen.id==id_examen).update(examen_update_dict)
#             self.db.commit()
#             result = True

#         except Exception as e:
#             print("Error during the update Examen", e)
#         return result
    
#     def delete_examen(self, examen: Examen):
#         self.db.delete(examen)
#         self.db.commit()
    


