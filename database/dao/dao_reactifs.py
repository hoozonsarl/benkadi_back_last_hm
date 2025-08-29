from random import randint
from database.utils import calculate_checksum
from models.reactifs import Reactif
from schemas.reactifs import ReactifCreate, ReactifUpdate
from sqlalchemy.orm import Session
from datetime import date, datetime
from barcode import EAN13
from barcode.writer import ImageWriter



class DaoReactif():
    db: Session


    def __init__(self, db: Session) -> None:
        self.db=db

    def get_all_reactifs(self):
        reactfis  =  self.db.query(Reactif).all()
        return reactfis
    
    def get_reactif_by_id(self, id_reactif:int):
        reactif = self.db.query(Reactif).filter(Reactif.id==id_reactif).first()
        return reactif
    
    def get_reactif_by_code_bar(self, numero_code_bar: str):
        reactif = self.db.query(Reactif).filter(Reactif.numero_code_bar==numero_code_bar).first()
        return reactif

    def get_reactif_by_name(self, nom: str):
        reactif = self.db.query(Reactif).filter(Reactif.nom==nom).first()
        return reactif
    
    def create_new_reactif(self, id_user: int, reactif_create: ReactifCreate):

        numero_code_bar = str(date.today()).replace("-","")[2:] + str(randint(10000,99999)) + "0"
        numero_code_bar = numero_code_bar + str(calculate_checksum(value=numero_code_bar))
        with open(f"static/{numero_code_bar}.png", "wb") as f:
            EAN13(numero_code_bar, writer=ImageWriter()).write(f)




        reactif = Reactif(nom= reactif_create.nom, 
                          reference=reactif_create.reference,
                          quantite=reactif_create.quantite,
                          numero_lot=reactif_create.numero_lot,
                          numero_code_bar=numero_code_bar,
                          codeBar=f"/static/{numero_code_bar}.png",
                          date_production=reactif_create.date_production, 
                          date_expiration=reactif_create.date_expiration, 
                          valeur_seuil=reactif_create.valeur_seuil,
                          id_user=id_user)
        self.db.add(reactif)
        self.db.commit()
        self.db.refresh(reactif)
        return reactif
    
    def update_reactif(self, id_reactif:int, reactif_update: ReactifUpdate):
        result = False
        try:
            reactif_update_dict = reactif_update.model_dump()
            self.db.query(Reactif).filter(Reactif.id==id_reactif).update(reactif_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during update reactfif", e)

        return result
    
    def delete_reactif(self, reactif: Reactif):
        self.db.delete(reactif)
        self.db.commit()