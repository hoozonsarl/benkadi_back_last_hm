from sqlalchemy.orm import Session
from pydantic import EmailStr
from schemas.prelevements import PrelevementCreate, PrelevementUpdate
from models.prelevements import Prelevement
from models.fraction_type import FractionType
from datetime import date, datetime
from barcode import EAN13
from barcode.writer import ImageWriter
from random import randint
import json
from database.utils import calculate_checksum
from models.donneurs import Donneur

class DaoPrelevement():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_prelevements(self, estAnalyser: bool = False):
        receveurs = self.db.query(Prelevement).filter(Prelevement.estAnalyser == estAnalyser).all()
        return receveurs
    
    def get_prelevements_without_phenotype_done(self):
        prelevements = self.db.query(Prelevement).filter(Prelevement.is_phenotype_done==False).all()
        return prelevements
    

    def get_prelevements_with_donneur(self):
        prelevements = self.db.query(Prelevement).join(Donneur, Prelevement.id_donneur == Donneur.id
                                                       ).filter(
        Donneur.is_tdr_done == True,
        Donneur.is_ok_prelevement == True, 
        Donneur.is_rejected == False,
        Donneur.is_prelevement_done == False
       ).add_entity(Donneur).all()
        result = []
        for prelevement, donneur in prelevements:
            prelevement_dict = {
                "id": prelevement.id,
                "numero_code_bar": prelevement.numero_code_bar,
                "codeBar": prelevement.codeBar,
                "dateDePrelevement": prelevement.dateDePrelevement,
                "heureDebut": prelevement.heureDebut,
                "heureFin": prelevement.heureFin,
                "poidsDePoche": prelevement.poidsDePoche,
                "volumePrevele": prelevement.volumePrevele,
                "remarques": prelevement.remarques,
                "effetsIndesirables": prelevement.effetsIndesirables,
                "estAnalyser": prelevement.estAnalyser,
                "id_donneur": prelevement.id_donneur,
                "id_parametre": prelevement.id_parametre,
                "id_user": prelevement.id_user,
                "createdAt": prelevement.createdAt,
                "updatedAt": prelevement.updatedAt,
                "code_diff": prelevement.code_diff,
                "is_phenotype_done": prelevement.is_phenotype_done,
                "donneur": {
                    "id": donneur.id,
                    "nom": donneur.nom,
                    "prenom": donneur.prenom,
                    "sexe": donneur.sexe,
                    "telephone": donneur.telephone,
                    "commentaire": donneur.parametres[0].commentaire
                }
            }
            result.append(prelevement_dict)
        return result
    

    def get_prelevements_without_analyse_done(self):
        prelevements = self.db.query(Prelevement).filter(Prelevement.estAnalyser==False).all()
        return prelevements
    
    def get_prelevements_by_pagination(self, estAnalyser: bool = False, skip:int = 0, limit:int = 100):
        prelevements = self.db.query(Prelevement).filter(Prelevement.estAnalyser == estAnalyser).skip(skip).limit(limit).all()
        return prelevements
    

    #count all prelevements of the month
    def count_prelevements_of_the_month(self):
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Calculate the first day of the current month
        start_date = datetime(current_year, current_month, 1)
        
        # Calculate the first day of the next month
        if current_month == 12:
            next_month_start = datetime(current_year + 1, 1, 1)
        else:
            next_month_start = datetime(current_year, current_month + 1, 1)
        
        print("actuelle mois", current_month)
        
        # Filter prelevements created within the current month
        prelevements = self.db.query(Prelevement).filter(
            Prelevement.createdAt >= start_date,
            Prelevement.createdAt < next_month_start
        ).count()

        print("nbr_prelevements", prelevements)
        
        return prelevements
    
    
    def get_prelevement_by_id(self, id_prelevement: int):
        prelevement = self.db.query(Prelevement).filter(Prelevement.id==id_prelevement).first()
        return prelevement
    
    def get_prelevements_donneurs(self, id_donneur:int ):
        prelevements = self.db.query(Prelevement).filter(Prelevement.id_donneur==id_donneur).all()
        return prelevements

    
    def make_analyse(self, id_prelevement: int):
        prelevement = self.db.query(Prelevement).filter(Prelevement.id == id_prelevement).first()
        prelevement.estAnalyser = True
        #self.db.commit()
        self.db.refresh(prelevement)
        return prelevement
    

    def make_phenotype_done(self, id_prelevement: int):
        prelevement = self.db.query(Prelevement).filter(Prelevement.id == id_prelevement).first()
        prelevement.is_phenotype_done = True
        #self.db.commit()
        self.db.refresh(prelevement)
        return prelevement

    def create_new_prelevement(self, id_user: int, prelevement: PrelevementCreate, nbr_poches: int):
        # Format date as DDMMYY
        today = date.today()
        date_part = today.strftime("%d%m%y")
        print("date_part", date_part)
        print("nbr_poches", nbr_poches)
        
        # Format nbr_poches with leading zeros to make it 6 digits
        poche_part = str(nbr_poches).zfill(6)
        
        # Create the base barcode without checksum
        numero_code_bar_base = date_part + poche_part
        
        # Add the checksum
        numero_code_bar = numero_code_bar_base + str(calculate_checksum(value=numero_code_bar_base))
        
        # Generate barcode image
        with open(f"static/{numero_code_bar}.png", "wb") as f:
            EAN13(numero_code_bar, writer=ImageWriter()).write(f)
        
        # Handle fraction types
        fraction_types = self.db.query(FractionType).all()
        code_diff = {
            fraction_type.nom.strip(): numero_code_bar[:-2] + fraction_type.code + 
            str(calculate_checksum(value=numero_code_bar[:-2] + fraction_type.code)) 
            for fraction_type in fraction_types if not fraction_type.is_total
        }

        # Generate barcode images for fraction types
        for code in code_diff.values():
            with open(f"static/{code}.png", "wb") as f:
                EAN13(code, writer=ImageWriter()).write(f)
        
        # Create prelevement database object
        prelevement_db = Prelevement(
            dateDePrelevement=prelevement.dateDePrelevement, 
            heureDebut=prelevement.heureDebut,
            heureFin=prelevement.heureFin, 
            poidsDePoche=prelevement.poidsDePoche, 
            volumePrevele=prelevement.volumePrevele, 
            remarques=prelevement.remarques, 
            effetsIndesirables=prelevement.effetsIndesirables, 
            id_donneur=prelevement.id_donneur,
            id_user=id_user, 
            updatedAt=datetime.now(),
            numero_code_bar=numero_code_bar, 
            codeBar=f"/static/{numero_code_bar}.png", 
            code_diff=json.dumps(code_diff), 
            id_parametre=prelevement.id_parametre
        )
        
        self.db.add(prelevement_db)
        return prelevement_db

    def get_prelevements_by_pagination(self, skip: int = 0, limit: int = 100):
        return self.db.query(Prelevement).offset(skip).limit(limit).all()

    def update_prelevement(self, id_prelevement: int, prevelement_update: PrelevementUpdate):
        result = True
        try:
            prelevement_update_dict = prevelement_update.model_dump()
            print(prelevement_update_dict)
            self.db.query(Prelevement).filter(Prelevement.id==id_prelevement).update(prelevement_update_dict)
            self.db.commit()
        except Exception as e:
            print("error during the update prelevement", e)
            result = False
        return result
    
    def update_prelevement_archive(self, id_prelevement:int, estArchive: bool):
        result = True
        try:
            prelevement_update_dict = {}
            prelevement_update_dict.update({"updatedAt": datetime.now()})
            prelevement_update_dict.update({"estArchive": estArchive})
            self.db.query(Prelevement).filter(Prelevement.id==id_prelevement).update(prelevement_update_dict)
            self.db.commit()
        except Exception as e:
            print("Error during the update Prelevement estArchive")
            result = False
        return result

    

    def delete_prelevement(self, prelevement: Prelevement):

        self.db.delete(prelevement)
        self.db.commit()



    