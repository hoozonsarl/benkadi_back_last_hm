from pydantic import Field, BaseModel
from datetime import date, datetime, time
from typing import Optional
from models.receveurs import Sexe
from enum import Enum as PyEnum
from pydantic import EmailStr
from models.receveurs import GroupeSanguin

class Religion(str, PyEnum):
    MUSULMAN = "MUSULMAN"
    CHRETIEN = "CHRETIEN"
    JEHOVAH = "JEHOVAH"
    ANEMIST = "ANEMIST"
    TRADITIONNALIST = "TRADITIONNALIST"
    AUTRE = "AUTRE"
    NON_SPECIFIE = "NON  SPECIFIE"

class StatusMatrimonial(str, PyEnum):
    CELIBATAIRE = "Celibataire"
    MARIE = "Marie(e)"
    DIVORCE = "Divorce"
    VEUVE = "veuf(ve)"


class ParametreCreate(BaseModel):

    tensionArterielleBs: Optional[str] = Field(examples=["0"],default=None)
    tensionArterielleMd: Optional[str] = Field(examples=["0"],default=None)
    tensionArterielleF: Optional[str] = Field(examples=["0"],default=None)

    rythmeCardiaque: int = Field(examples=[0])
    poids: int =  Field(examples=[80])
    hemoglobine: float = Field(examples=[15.0])
    taille: float = Field(examples=[1.74])
    depistageVIH: bool = Field(examples=[False])

    commentaire: str =  Field(examples=[""])
    quantite: int = Field(examples=[0])
    remarques: str = Field(examples=[""])
    
    ## Questionnaire médical
    
    # 1. Pourquoi donnez-vous votre sang ?
    raisonDon: str = Field(examples=["{'reponse': 'autre', details: ''}"])  # default: "{"reponse": "autre", details: ""}"
    # 2. Etes-vous en jeûne ? (ne pas avoir mangé ni bu depuis au moins 3 heures)
    raisonDon_aide: str = Field(examples=["aider un proche"])
    raisonDon_remplacer: str = Field(examples=["remplacer un don de sang"])
    raisonDon_famille: str = Field(examples=["Pour un membre de la famille"])
    jeune: str   =Field(examples=["{'reponse': 'non', details: ''}"])# default: "{"reponse": "non", details: ""}"
    # 3. Avez-vous une des affections suivantes ? (cocher la ou les cases correspondantes)
    affections: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 4. Avez-vous déjà contracté une infection sexuellement transmissible, ou été traité pour cela ?
    infectionSexulle: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 5. Avez-vous déjà été hospitalisé(e) ou opéré ? 
    hospitalisation: str = Field(examples=["{'reponse': 'non', motif: '', periode: ''}"])  # default: "{"reponse": "non", motif: "", periode: ""}"
    # 6. Etes-vous en bonne santé ?
    bonneSante: str = Field(examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "oui", details: ""}"
    # 7. Durant ces dernière 4 mois ou depuis votre dernier don, avez-vous éte malade ?
    malade: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 8. Avez-vous présenté une fièvre au cours des 15 derniers jours ?
    fievre: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 9. Prenez-vous des médicaments actuellement ?
    medicaments: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 10. Avez-vous été vacciné ? 
    vaccine: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 11. Avez-vous eu d’autres antécédents médicaux/chirurgicaux/allergiques/médicamenteux ?
    antecedents: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 12. Avez-vous été victime d’un accident avec écoulement abondant de sang ? 
    accident: str = Field(examples=["{'reponse': 'non', details: ''}"])    # default: "{"reponse": "non", details: ""}"
    # 13. Êtes-vous allé chez le dentiste ces deux dernières semaines?
    dentiste: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 14. Avez-vous subi une endoscopie récemment? 
    endoscopie: str = Field(examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 15. Avez-vous été traité par acupuncture et/ou par mésothérapie ? 
    acupuncture: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 16. Avez-vous été tatoué, scarifié ou subi un piercing ?
    tatouage: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 17. Êtes-vous exposé professionnellement au VIH ou virus de l’hépatite ?
    exposition: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 18. Avez-vous déjà fait un test du VIH ou de l’hépatite ?
    testVIH: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 19. Y a-t-il eu quelqu’un dans votre entourage atteint de jaunisse ou de maladie infectieuse ?
    entourageMalade: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 20. Avez-vous eu des rapports sexuels avec plus d’un partenaire ces 4 derniers mois ?
    rapportSexuel: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 21. Utiliser vous un préservatif lors de vos rapports sexuels? 
    preservatif: str = Field(examples=["{'reponse': 'non', details: ''}"])    # default: "{"reponse": "non", details: ""}"
    # 22. Avez-vous déjà consommé de la cocaïne ou des drogues? 
    drogue: str = Field(examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", periode: ""}"
    # 23. Avez-vous voyagé à l'étranger ?
    voyageEtranger: str = Field(examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 24.  Si vous êtes un homme, avez-vous eu des rapports sexuels avec un autre homme? 
    rapportSexuelHomme: str  = Field(examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", details: ""}"
    
    # Questions réservées aux femmes :
    # 25. Êtes-vous enceinte ou avez-vous accouché au cours des 6 derniers mois ?
    grossesse: str  = Field(examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", details: ""}"
    # 26.  Allaitez-vous ?
    allaitez: str  = Field(examples=["{'reponse': 'non', details: ''}"])# default: "{"reponse": "non", details: ""}"
    # 27. Avez-vous déjà subi des fausses couches ou un avortement ?
    fausseCouche: str = Field(examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 28. A quand remontent vos dernières règles (menstrues) ?
    regles: str = Field(examples=["{'reponse': 'non', periode: '', lieu: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"

    benevole: Optional[bool] = Field(default=None, examples=[False, True])

    nomPatient: Optional[str] = Field(examples=["Nom du patient"])
    hopital: Optional[str] = Field(examples=["Hopital"])
    prenomPatient: Optional[str] = Field(examples=["Prenom du patient"])

    serviceSanitaire: Optional[str] = Field(examples=["Service sanitaire"])



class ParametreUpdate(BaseModel):

    # tensionArterielle: Optional[str] = Field(default=None, examples=[0])
    tensionArterielleBs: Optional[str] = Field(examples=["0"], default=None)
    tensionArterielleMd: Optional[str]= Field(examples=["0"], default=None)
    tensionArterielleF: Optional[str] = Field(examples=["0"] ,default=None)
    rythmeCardiaque: Optional[int] = Field(default=None, examples=[0])
    poids: Optional[int] =  Field(default=None, examples=[80])
    hemoglobine: Optional[float] = Field(default=None, examples=[15.0])
    taille: Optional[float] = Field(default=None, examples=[1.74])
    depistageVIH: Optional[int] = Field(default=None, examples=[False])


    commentaire: Optional[str] =  Field(default=None, examples=[""])
    quantite: Optional[int] = Field(default=None, examples=[0])
    remarques: Optional[str] = Field(default=None, examples=[""])
    
    ## Questionnaire médical
    
    # 1. Pourquoi donnez-vous votre sang ?
    raisonDon: Optional[str] = Field(default=None, examples=["{'reponse': 'autre', details: ''}"])
    # 2. Etes-vous en jeûne ? (ne pas avoir mangé ni bu depuis au moins 3 heures)
    raisonDon_aide: Optional[str] = Field(default=None,  examples=["aider un proche"])
    raisonDon_remplacer: Optional[str] = Field(default=None,  examples=["remplacer un don de sang"])
    raisonDon_famille: Optional[str] = Field(default=None, examples=["Pour un membre de la famille"])
    jeune: Optional[str]   = Field(default=None, examples=["{'reponse': 'non', details: ''}"])# default: "{"reponse": "non", details: ""}"
    # 3. Avez-vous une des affections suivantes ? (cocher la ou les cases correspondantes)
    affections: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 4. Avez-vous déjà contracté une infection sexuellement transmissible, ou été traité pour cela ?
    infectionSexulle: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 5. Avez-vous déjà été hospitalisé(e) ou opéré ? 
    hospitalisation: Optional[str] = Field(default=None, examples=["{'reponse': 'non', motif: '', periode: ''}"])  # default: "{"reponse": "non", motif: "", periode: ""}"
    # 6. Etes-vous en bonne santé ?
    bonneSante: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "oui", details: ""}"
    # 7. Durant ces dernière 4 mois ou depuis votre dernier don, avez-vous éte malade ?
    malade: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 8. Avez-vous présenté une fièvre au cours des 15 derniers jours ?
    fievre: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 9. Prenez-vous des médicaments actuellement ?
    medicaments: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 10. Avez-vous été vacciné ? 
    vaccine: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 11. Avez-vous eu d’autres antécédents médicaux/chirurgicaux/allergiques/médicamenteux ?
    antecedents: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 12. Avez-vous été victime d’un accident avec écoulement abondant de sang ? 
    accident: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])    # default: "{"reponse": "non", details: ""}"
    # 13. Êtes-vous allé chez le dentiste ces deux dernières semaines?
    dentiste: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 14. Avez-vous subi une endoscopie récemment? 
    endoscopie: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])  # default: "{"reponse": "non", details: ""}"
    # 15. Avez-vous été traité par acupuncture et/ou par mésothérapie ? 
    acupuncture: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 16. Avez-vous été tatoué, scarifié ou subi un piercing ?
    tatouage: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 17. Êtes-vous exposé professionnellement au VIH ou virus de l’hépatite ?
    exposition: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 18. Avez-vous déjà fait un test du VIH ou de l’hépatite ?
    testVIH: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 19. Y a-t-il eu quelqu’un dans votre entourage atteint de jaunisse ou de maladie infectieuse ?
    entourageMalade: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 20. Avez-vous eu des rapports sexuels avec plus d’un partenaire ces 4 derniers mois ?
    rapportSexuel: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", details: ""}"
    # 21. Utiliser vous un préservatif lors de vos rapports sexuels? 
    preservatif: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])    # default: "{"reponse": "non", details: ""}"
    # 22. Avez-vous déjà consommé de la cocaïne ou des drogues? 
    drogue: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"])   # default: "{"reponse": "non", periode: ""}"
    # 23. Avez-vous voyagé à l'étranger ?
    voyageEtranger: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 24.  Si vous êtes un homme, avez-vous eu des rapports sexuels avec un autre homme? 
    rapportSexuelHomme: Optional[str]  = Field(default=None, examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", details: ""}"
    
    # Questions réservées aux femmes :
    # 25. Êtes-vous enceinte ou avez-vous accouché au cours des 6 derniers mois ?
    grossesse: Optional[str]  = Field(default=None, examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", details: ""}"
    # 26.  Allaitez-vous ?
    allaitez: Optional[str]  = Field(default=None, examples=["{'reponse': 'non', details: ''}"])# default: "{"reponse": "non", details: ""}"
    # 27. Avez-vous déjà subi des fausses couches ou un avortement ?
    fausseCouche: Optional[str] = Field(default=None, examples=["{'reponse': 'non', details: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"
    # 28. A quand remontent vos dernières règles (menstrues) ?
    regles: Optional[str] = Field(default=None, examples=["{'reponse': 'non', periode: '', lieu: ''}"]) # default: "{"reponse": "non", periode: "", lieu: ""}"

    examen_tdr: Optional[str] = Field(default=None, examples=[""])

    benevole: Optional[bool] = Field(default=None, examples=[False, True])

    nomPatient: Optional[str] = Field(default=None, examples=["Nom du patient"])
    prenomPatient: Optional[str] = Field(default=None, examples=["Prenom du patient"])
    hopital: Optional[str] = Field(default=None, examples=["Hopital"])
    serviceSanitaire: Optional[str] = Field(default=None, examples=["Service sanitaire"])

class DonneurResponseModel(BaseModel):
    id: int 
    nom: Optional[str] = None   
    prenom: Optional[str] = None
    dateDeNaissance: Optional[date] = None
    lieuDeNaissance: Optional[str] = None
    numeroCNI: Optional[str] = None
    passport: Optional[str] = None
    permisConduire: Optional[str] = None
    dateDelivranceIdCard: Optional[date] = None
    villeResidence: Optional[str] = None
    niveauEtude: Optional[str] = None
    sexe: Sexe
    profession: str 
    statusMatrimonial: StatusMatrimonial 
    paysOrigine: str 
    religion: Religion
    adresse: str  
    telephone: str 
    email: Optional[str] = None
    groupeSanguin: Optional[str] = None
    dateDeProchainDon: Optional[date] = None
    dateDernierDon: Optional[date] = None
    datePossibleDon: Optional[date] = None
    isDelayed: bool
    isDelayedDate: Optional[date] = None
    nombreDeDons: int 
    accidentDon: str  
    dejaTransfuse: str 
    isDonneur: bool 
    dateAccueil: Optional[date] = None
    heureAccueil: Optional[time] = None
    dateConsultation: Optional[date] = None
    heureConsultation: Optional[time] = None
    createdAt: datetime 
    updatedAt: datetime 
    id_user: int
    isDonneur: bool
    isValideMedecin: Optional[bool] = False
    isValideAnalyseTDR: Optional[bool] = False 
    lu_approve: bool
    is_tdr_done: bool
    is_ok_prelevement: bool
    is_prelevement_done: bool


class ParametreResponseModel(ParametreCreate):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    donneur: DonneurResponseModel
    examen_tdr: str