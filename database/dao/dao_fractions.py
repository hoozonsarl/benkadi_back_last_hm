from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from models.fractions import Fraction
from schemas.fractions import FractionCreate, FractionUpdate
from random import randint
from datetime import datetime, timedelta
from models.fraction_type import FractionType
from models.poches_de_sangs import PocheDeSang
from models.prelevements import Prelevement
import json
from sqlalchemy import func
from collections import defaultdict

class DaoFraction():
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    
    def get_all_fractions(self, estDistribue: bool = False):
        fractions =  self.db.query(Fraction).filter(Fraction.estDistribue==estDistribue).filter(Fraction.dateAvailable<=datetime.today().date()).filter(Fraction.dateDeExpiration>=datetime.today().date()).order_by(Fraction.dateDeExpiration).all()
        return fractions
    

    def get_all_fractions_by_paginaton(self, skip:int = 0, limit: int = 0):
        fractions = self.db.query(Fraction).offset(skip).limit(limit).order_by(Fraction.dateDeExpiration).all()
        return fractions
    
    def get_fraction_by_id(self, id_fraction: int):
        fraction = self.db.query(Fraction).filter(Fraction.id==id_fraction).first()
        return fraction

    def get_fraction_by_code(self, code: str):
        fraction = self.db.query(Fraction).filter(Fraction.code==code).all()
        return fraction
    
    def get_all_frcation_not_distribue(self,):
        fractions = self.db.query(Fraction).filter(Fraction.estDistribue==True).all()
        return fractions
    
    def get_all_fraction_distribue(self,):
        fractions = self.db.query(Fraction).filter(Fraction.estArchive==False).all()
        return fractions
    
    def get_all_fraction_distribue_archive(self, estArchive: bool=False, estDistribue: bool=False):
        fractions = self.db.query(Fraction).filter(Fraction.estArchive==estArchive, Fraction.estDistribue==estDistribue)
        return fractions
    


    def etat_de_stock_non_qualifier(self):
        fraction_type_dict = {}
        d = defaultdict(lambda : defaultdict(int))
        frations = self.db.query(Fraction).filter(Fraction.estDistribue == False).filter(Fraction.is_ok_to_use == False).filter(Fraction.is_destroy == False).all()
       

        
        fractions_group_by_type_de_fraction = self.db.query(Fraction.id_fraction_type, func.count(Fraction.id)).filter(Fraction.estDistribue == False).filter(Fraction.is_ok_to_use == False).filter(Fraction.is_destroy == False).group_by(Fraction.id_fraction_type).all()
        print("fractions_group_by_type_de_fraction", fractions_group_by_type_de_fraction)
        fraction_types = self.db.query(FractionType).all()
        for fraction_type in fraction_types:
            fraction_type_dict[fraction_type.id] = fraction_type.nom
        fraction_type_dict_count = {}
        for id_fraction_type, count in fractions_group_by_type_de_fraction:
            fraction_type_dict_count[fraction_type_dict[id_fraction_type]] = count
        print("fraction type dict count", fraction_type_dict_count)

        for fraction in frations:
            d[fraction.poche_de_sang.groupeSanguin][fraction_type_dict[fraction.id_fraction_type]] += 1
        
        return {"par_type_de_fraction": fraction_type_dict_count, "par_group_sanguin": d}
    

    def etat_de_stock_destroy(self):
        fraction_type_dict = {}
        d = defaultdict(lambda : defaultdict(int))
        frations = self.db.query(Fraction).filter(Fraction.is_destroy==True).filter(Fraction.estDistribue == False).all()

        
        fractions_group_by_type_de_fraction = self.db.query(Fraction.id_fraction_type, func.count(Fraction.id)).filter(Fraction.estDistribue == False).filter(Fraction.is_destroy==True).group_by(Fraction.id_fraction_type).all()
        print("fractions_group_by_type_de_fraction", fractions_group_by_type_de_fraction)
        fraction_types = self.db.query(FractionType).all()
        for fraction_type in fraction_types:
            fraction_type_dict[fraction_type.id] = fraction_type.nom
        fraction_type_dict_count = {}
        for id_fraction_type, count in fractions_group_by_type_de_fraction:
            fraction_type_dict_count[fraction_type_dict[id_fraction_type]] = count
        print("fraction type dict count", fraction_type_dict_count)

        for fraction in frations:
            d[fraction.poche_de_sang.groupeSanguin][fraction_type_dict[fraction.id_fraction_type]] += 1
        
        return {"par_type_de_fraction": fraction_type_dict_count, "par_group_sanguin": d}
    

    def etat_de_stock_quarantaine(self):
        fraction_type_dict = {}
        d = defaultdict(lambda : defaultdict(int))
        frations = self.db.query(Fraction).filter(Fraction.estDistribue == False).filter(Fraction.dateAvailable>datetime.today().date()).filter(Fraction.dateDeExpiration>=datetime.today().date()).all()

        
        fractions_group_by_type_de_fraction = self.db.query(Fraction.id_fraction_type, func.count(Fraction.id)).filter(Fraction.estDistribue == False).filter(Fraction.dateAvailable>datetime.today().date()).filter(Fraction.dateDeExpiration>=datetime.today().date()).group_by(Fraction.id_fraction_type).all()
        print("fractions_group_by_type_de_fraction", fractions_group_by_type_de_fraction)
        fraction_types = self.db.query(FractionType).all() 
        for fraction_type in fraction_types:
            fraction_type_dict[fraction_type.id] = fraction_type.nom
        fraction_type_dict_count = {}
        for id_fraction_type, count in fractions_group_by_type_de_fraction:
            fraction_type_dict_count[fraction_type_dict[id_fraction_type]] = count
        print("fraction type dict count", fraction_type_dict_count)

        for fraction in frations:
            d[fraction.poche_de_sang.groupeSanguin][fraction_type_dict[fraction.id_fraction_type]] += 1
        
        return {"par_type_de_fraction": fraction_type_dict_count, "par_group_sanguin": d}
    

    
    def etat_de_stock(self):
        fraction_type_dict = {}
        d = defaultdict(lambda : defaultdict(int))
        frations = self.db.query(Fraction).filter(Fraction.estDistribue == False).filter(Fraction.dateAvailable<=datetime.today().date()).filter(Fraction.dateDeExpiration>=datetime.today().date()).filter(Fraction.is_ok_to_use==True).all()
        
        fractions_group_by_type_de_fraction = self.db.query(Fraction.id_fraction_type, func.count(Fraction.id)).filter(Fraction.estDistribue == False).filter(Fraction.dateAvailable<=datetime.today().date()).filter(Fraction.dateDeExpiration>=datetime.today().date()).filter(Fraction.is_ok_to_use==True).group_by(Fraction.id_fraction_type).all()
        print("fractions_group_by_type_de_fraction", fractions_group_by_type_de_fraction)
        fraction_types = self.db.query(FractionType).all()
        for fraction_type in fraction_types:
            fraction_type_dict[fraction_type.id] = fraction_type.nom
        fraction_type_dict_count = {}
        for id_fraction_type, count in fractions_group_by_type_de_fraction:
            fraction_type_dict_count[fraction_type_dict[id_fraction_type]] = count
        print("fraction type dict count", fraction_type_dict_count)

        for fraction in frations:
            d[fraction.poche_de_sang.groupeSanguin][fraction_type_dict[fraction.id_fraction_type]] += 1
        
        return {"par_type_de_fraction": fraction_type_dict_count, "par_group_sanguin": d}
        
    
    def create_new_fraction(self,id_poche_de_sang: int, fraction_create: FractionCreate):
        fraction_type = self.db.query(FractionType).filter(FractionType.id == fraction_create.id_fraction_type).first()
        poche_de_sang = self.db.query(PocheDeSang).filter(PocheDeSang.id == id_poche_de_sang).first()
        prelevement = self.db.query(Prelevement).filter(Prelevement.id == poche_de_sang.id_prelevement).first()
        code_bar = "static/" + f"{json.loads(prelevement.code_diff)[fraction_type.nom]}" + ".png" if json.loads(prelevement.code_diff).get(fraction_type.nom) else prelevement.codeBar
        fraction = Fraction(id_poche_de_sang=id_poche_de_sang , 
                            dateDePrelevement=fraction_create.dateDePrelevement, 
                            dateDeExpiration=fraction_create.dateDePrelevement + timedelta(days=fraction_type.nombreDeJourExpiration),
                              volume=fraction_create.volume, 
                              poids=fraction_create.poids, 
                              id_fraction_type=fraction_create.id_fraction_type,
                                updatedAt=datetime.now(),
                                  code_bar=code_bar,
                                    numero_code_bar=code_bar, 
                                    is_valid=fraction_create.is_valid,
                                    is_analyse_done=fraction_create.is_analyse_done,
                                    is_ok_to_use=fraction_create.is_ok_to_use,
                                    is_destroy=fraction_create.is_destroy,
                                    dateAvailable=datetime.today().date()+timedelta(days=fraction_type.quarantaine))
        self.db.add(fraction)
        self.db.commit()
        self.db.refresh(fraction)
        return fraction
    
    def update_fraction(self, id_fraction:int, fraction_update: FractionUpdate):

        result = False
        try:
            fraction_update_dict = fraction_update.model_dump()
            print(fraction_update_dict)

            self.db.query(Fraction).filter(Fraction.id==id_fraction).update(fraction_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during update fraction", e)
        return result
    
    def archive_fraction(self, id_fraction:int):

        result = False
        try:
            fraction_update_dict = {}
            fraction_update_dict.update({"updatedAt": datetime.now()})
            fraction_update_dict.update({"estDistribue": True})
            self.db.query(Fraction).filter(Fraction.id==id_fraction).update(fraction_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during update(archive) fraction", e)
        return result

    def de_archive_fraction(self, id_fraction:int):

        result = False
        try:
            fraction_update_dict = {}
            fraction_update_dict.update({"updatedAt": datetime.now()})
            fraction_update_dict.update({"estArchive": False})
            print(fraction_update_dict)
            self.db.query(Fraction).filter(Fraction.id==id_fraction).update(fraction_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during update(dearchive) fraction", e)
        return result
    
    def delete_fraction(self, fraction: Fraction):
        self.db.delete(fraction)
        self.db.commit()

