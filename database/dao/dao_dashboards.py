from sqlalchemy.orm import Session
from models.fractions import Fraction
from models.donneurs import Donneur
from models.receveurs import Receveur
from models.bon_de_sang import BonDeSang
from models.distributions import Distribution
from models.poches_de_sangs import PocheDeSang
from models.prelevements import Prelevement
from sqlalchemy import func
from datetime import datetime, timedelta, date
from sqlalchemy import and_

class DaoDashboards():

    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db


    def full_dashbord(self,) -> dict:

        data = {}

        current_year = datetime.now().year
        today = date.today()

        week_day = today.weekday()

        start_of_week =  today - timedelta(days=week_day)

        end_of_week = start_of_week + timedelta(days=6)


        donneurs_by_weekday = self.db.query(func.extract('dow', Donneur.createdAt).label('weekday'),
                                            func.count('*').label('count')).\
                                            filter(Donneur.createdAt.between(start_of_week, end_of_week)) \
                                            .group_by(func.extract('dow', Donneur.createdAt)).all()
                                                      
        receveurs_by_weekday = self.db.query(func.extract('dow', Receveur.createdAt).label('weekday'),
                                            func.count('*').label('count')).\
                                            filter(Receveur.createdAt.between(start_of_week, end_of_week)) \
                                            .group_by(func.extract('dow', Receveur.createdAt)).all()
                                                      
        categories_donneur_weekday = ["L", "M", "M", "J", "V", "S", "D"]

        categories_receveur_weekday = ["L", "M", "M", "J", "V", "S", "D"]
        
        series_donneur_by_weekday = [0 for _ in range (7)]

        for week_day, count in donneurs_by_weekday:
            series_donneur_by_weekday[int(week_day)-1] = count
        
        data["donneurs_by_weekday"] = {"categories": categories_donneur_weekday, "series": series_donneur_by_weekday}

        series_receveur_by_weekday = [0 for _ in range (7)]

        for week_day, count in receveurs_by_weekday:
            series_receveur_by_weekday[int(week_day)-1] = count
            
        data["receveurs_by_weekday"] = {"categories": categories_receveur_weekday, "series": series_receveur_by_weekday}
        

        donneurs_by_month  = self.db.query(func.extract("month", Donneur.createdAt).label('month'), func.count(Donneur.id)) \
                                            .filter(func.extract('year', Donneur.createdAt) == current_year) \
                                            .group_by(func.extract("month", Donneur.createdAt)) \
                                            .all()
        series_donnueur_by_month = [0 for i in range(12)]
        categories_donneur_month = ['Jan','Feb', 'Mar','Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]


        for month, count in donneurs_by_month:
            series_donnueur_by_month[int(month)-1] = count
        data["donneurs_by_month"] = {"categories": categories_donneur_month, "series": series_donnueur_by_month}

        receveurs_by_month  = self.db.query(func.extract("month", Receveur.createdAt).label('month'), func.count(Receveur.id)) \
                                            .filter(func.extract('year', Receveur.createdAt) == current_year) \
                                            .group_by(func.extract("month", Receveur.createdAt)) \
                                            .all()
       

        categories_receveur_by_month = ['Jan','Feb', 'Mar','Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        series_receveur_by_month = [0 for _ in range(12)]
        for month, count in receveurs_by_month:
            series_receveur_by_month[int(month)-1] = count
        data["receveurs_by_month"] = {"categories": categories_receveur_by_month, "series": series_receveur_by_month}

        # nombre de poche de sang qualifiees: retouner tous les fractions de poche de sang donc la date de disponibilite est superieure a la date d'aujourdhui

        data["fractions_qualifiees"] = len(self.db.query(Fraction).filter(Fraction.estDistribue==False).filter(Fraction.dateDeExpiration>=datetime.today().date()).all())

        # total des candidats au don: est un donneurs qui n'a pas ete valide par le medecin et qui n'a pas encore faire de TDR

        data["candidat_au_don"] = len(self.db.query(Donneur).filter(and_(Donneur.is_tdr_done==False, Donneur.isValideAnalyseTDR==False, Donneur.dateDeProchainDon==Donneur.dateDernierDon)).all())

        # total des candidats rejected par le medecin

        data["candidat_au_don_reject_medecin"] = len(self.db.query(Donneur).filter(Donneur.isValideMedecin==False).all())

        # total des candidats rejected par le medecin

        data["candidat_au_don_reject_TDR"] = len(self.db.query(Donneur).filter(Donneur.isValideAnalyseTDR==False, Donneur.is_tdr_done==True).all())

        # total des Donneurs: un donneur est un candidat au don dont les resultats du medecin et l'analyse TDR sont validees

        data["Donneurs_valides"] = len(self.db.query(Donneur).filter(and_(Donneur.isValideMedecin==True, Donneur.isValideAnalyseTDR==True)).all())

         # total poches de sang non distribuees

        data["poches_de_sang_non_distribues"] = len(self.db.query(Fraction).filter(Fraction.estDistribue==False).all())


        # total poches de sang distribuees

        data["poches_de_sang_distribues"] = len(self.db.query(Fraction).filter(Fraction.estDistribue==True).all())

        # total receveur enregistrees

        data["receveurs"] = len(self.db.query(Receveur).filter(Fraction.estDistribue==True).all())
        

        return data
