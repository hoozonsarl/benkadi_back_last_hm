from sqlalchemy  import String, DateTime, Integer, Column, Enum, Date, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base
from enum import Enum as PyEnum
from datetime import date, datetime
from pydantic import EmailStr


class Parametre(Base):

    __tablename__ = "parametres"
    id: int = Column(Integer, autoincrement=True, index=True, primary_key=True)

    ## Reservé au personnel de la banque de sang
    
    tensionArterielleBs: str = Column(String)
    tensionArterielleMd: str = Column(String,nullable=True)
    tensionArterielleF: str = Column(String,nullable=True)


    rythmeCardiaque: int = Column(Integer)
    poids: int = Column(Integer)
    hemoglobine: float = Column(Float)
    taille: Float = Column(Float)
    commentaire: str =  Column(String, nullable=True, default="")
    quantite: int = Column(Integer, nullable=True, default=0)
    remarques: str = Column(String, nullable=True, default="")
    depistageVIH: bool = Column(Boolean)
    id_donneur:int = Column(Integer, ForeignKey("donneurs.id", ondelete='CASCADE'))
    createdAt: datetime = Column(DateTime, default=datetime.now)
    updatedAt: datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    ## Questionnaire médical
    
    # 1. Pourquoi donnez-vous votre sang ?
    raisonDon: str  = Column(String) # default: "{"reponse": "autre", details: ""}"
    # 2. Etes-vous en jeûne ? (ne pas avoir mangé ni bu depuis au moins 3 heures)
    raisonDon_aide: str = Column(String)
    raisonDon_remplacer: str = Column(String)
    raisonDon_famille: str = Column(String)
    jeune: str  = Column(String) # default: "{"reponse": "non", details: ""}"
    # 3. Avez-vous une des affections suivantes ? (cocher la ou les cases correspondantes)
    affections: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 4. Avez-vous déjà contracté une infection sexuellement transmissible, ou été traité pour cela ?
    infectionSexulle: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 5. Avez-vous déjà été hospitalisé(e) ou opéré ? 
    hospitalisation: str = Column(String) # default: "{"reponse": "non", motif: "", periode: ""}"
    # 6. Etes-vous en bonne santé ?
    bonneSante: str = Column(String) # default: "{"reponse": "oui", details: ""}"
    # 7. Durant ces dernière 4 mois ou depuis votre dernier don, avez-vous éte malade ?
    malade: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 8. Avez-vous présenté une fièvre au cours des 15 derniers jours ?
    fievre: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 9. Prenez-vous des médicaments actuellement ?
    medicaments: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 10. Avez-vous été vacciné ? 
    vaccine: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 11. Avez-vous eu d’autres antécédents médicaux/chirurgicaux/allergiques/médicamenteux ?
    antecedents: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 12. Avez-vous été victime d’un accident avec écoulement abondant de sang ? 
    accident: str  = Column(String) # default: "{"reponse": "non", details: ""}"
    # 13. Êtes-vous allé chez le dentiste ces deux dernières semaines?
    dentiste: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 14. Avez-vous subi une endoscopie récemment? 
    endoscopie: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 15. Avez-vous été traité par acupuncture et/ou par mésothérapie ? 
    acupuncture: str  = Column(String) # default: "{"reponse": "non", details: ""}"
    # 16. Avez-vous été tatoué, scarifié ou subi un piercing ?
    tatouage: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 17. Êtes-vous exposé professionnellement au VIH ou virus de l’hépatite ?
    exposition: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 18. Avez-vous déjà fait un test du VIH ou de l’hépatite ?
    testVIH: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 19. Y a-t-il eu quelqu’un dans votre entourage atteint de jaunisse ou de maladie infectieuse ?
    entourageMalade: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 20. Avez-vous eu des rapports sexuels avec plus d’un partenaire ces 4 derniers mois ?
    rapportSexuel: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 21. Utiliser vous un préservatif lors de vos rapports sexuels? 
    preservatif: str  = Column(String) # default: "{"reponse": "non", details: ""}"
    # 22. Avez-vous déjà consommé de la cocaïne ou des drogues? 
    drogue: str = Column(String) # default: "{"reponse": "non", periode: ""}"
    # 23. Avez-vous voyagé à l'étranger ?
    voyageEtranger: str = Column(String) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 24.  Si vous êtes un homme, avez-vous eu des rapports sexuels avec un autre homme? 
    rapportSexuelHomme: str = Column(String)  # default: "{"reponse": "non", details: ""}"
    
    # Questions réservées aux femmes :
    # 25. Êtes-vous enceinte ou avez-vous accouché au cours des 6 derniers mois ?
    grossesse: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 26.  Allaitez-vous ?
    allaitez: str = Column(String) # default: "{"reponse": "non", details: ""}"
    # 27. Avez-vous déjà subi des fausses couches ou un avortement ?
    fausseCouche: str = Column(String) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 28. A quand remontent vos dernières règles (menstrues) ?
    regles: str = Column(String) # default: "{"reponse": "non", periode: "", lieu: ""}"
    benevole: bool = Column(Boolean)


    #nom du patient optionnel
    nomPatient: str = Column(String, nullable=True)
    prenomPatient: str = Column(String, nullable=True)
    hopital: str = Column(String, nullable=True)
    serviceSanitaire: str = Column(String, nullable=True)

    donneur = relationship("Donneur", back_populates="parametres")
    poche_de_sang = relationship("Prelevement", back_populates="parametres")

    examen_tdr: str = Column(String, default="")




    def __repr__(self):
        return f"<Parametre id: {self.id} ...>"