from models.receveurs import Sexe
from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional, List
from schemas.params_receveurs import ParamsReceveurResponseModel
#from schemas.receveurs import ReceveurResponseModel



class BonDeSangCreate(BaseModel):
    poids: Optional[int] = Field(default=None, examples=[70, 90])
    nom: Optional[str] = Field(default=None, examples=["John"])
    prenom: Optional[str] = Field(default=None, examples=["Doe"])
    dateDeNaissance: Optional[date] = Field(default=None, examples=["2024/01/02"])
    telephone: Optional[str] = Field(default=None, examples=["0700000000"])
    sexe: Optional[Sexe] = Field(default=None, examples=["HOMME"])
    email: Optional[str] = Field(default=None, examples=["john.doe@example.com"])
    patient_interne: Optional[bool] = Field(default=False, examples=[True])
    chambre: Optional[str] =  Field(default=None, examples=["chambre01"])
    lit: Optional[str] =  Field(default=None, examples=["lit01"])
    heure_demande: Optional[time] = Field(default=None, examples=["10:30"])
    antecedent_medicaux: Optional[str] = Field(default=None, examples=["drepanocytose", "thalassemie", "hemophile"])
    indication: Optional[str] =  Field(default=None, examples=["thombopenie severe a 47000"])
    statusVIH: Optional[bool] = Field(default=False, examples=[True, False])
    statusVHB: Optional[bool] = Field(default=False, examples=[True, False])
    statusVHC: Optional[bool] = Field(default=False, examples=[True, False])
    groupe_sanguin: Optional[str] = Field(default=None, examples=["A+"])
    groupe_sanguin_nouveau_ne:  Optional[str] = Field(default=None, examples=["A+"])
    groupe_sanguin_receveur: Optional[str] = Field(default=None, examples=["A+"])
    phenotype: Optional[str] = Field(default=None, examples=["A+"])
    nature_du_produit_sanguin: Optional[str] = Field(default=None, examples=["CGR,CPS,CPF"])
    nombre_de_poches: Optional[int] = Field(default=None, examples=[35])
    antecedent_transfusionnel: Optional[int] = Field(default=None, examples=[2])
    taux_hemoglobine: Optional[float] = Field(default=None, examples=[15])
    RAI_positif: Optional[bool] = Field(default=False, examples=[True])
    programme: Optional[date] = Field(default=None, examples=["2024/01/02"])
    heure: Optional[time] = Field(default=None, examples=["10:30"])
    hospital: Optional[str] = Field(default=None, examples=["CHU"])
    service: Optional[str] = Field(default=None, examples=["service01"])
    medecin_demandeur: Optional[str] = Field(default=None, examples=["Dr. John Doe"])
    specialité: Optional[str] = Field(default=None, examples=["Cardiologie"])
    examens: Optional[str] = Field(default=None, examples=["examens01"])
    estAnalyse: Optional[bool] = Field(default=None, examples=[True])
    date_transfusion: Optional[date] = Field(default=None, examples=["2024/01/02"])
    date_reception: Optional[date] = Field(default=None, examples=["2024/01/02"])
    date_retour_poche: Optional[date] = Field(default=None, examples=["2024/01/02"])
    motif: Optional[str] = Field(default=None, examples=["motif01"])
    test_compatibilite: Optional[str] = Field(default=None, examples=["test01"])
    is_phenotype_done: Optional[bool] = Field(default=None, examples=[True])
    is_test_compatibilite_done: Optional[bool] = Field(default=None, examples=[True])
    estDistribue: Optional[bool] = Field(default=None, examples=[True])



class BonDeSangUpdate(BaseModel):
    poids: Optional[int] = Field(default=None, examples=[70, 90])
    chambre: Optional[str] =  Field(default=None, examples=["chambre01"])
    nom: Optional[str] = Field(default=None, examples=["John"])
    prenom: Optional[str] = Field(default=None, examples=["Doe"])
    dateDeNaissance: Optional[date] = Field(default=None, examples=["2024/01/02"])
    telephone: Optional[str] = Field(default=None, examples=["0700000000"])
    email: Optional[str] = Field(default=None, examples=["john.doe@example.com"])
    sexe: Optional[Sexe] = Field(default=None, examples=["HOMME"])
    patient_interne: Optional[bool] = Field(default=None, examples=[True])
    lit: Optional[str] =  Field(default=None, examples=["lit01"])
    heure_demande: Optional[time] = Field(default=None, examples=["10:30"])
    antecedent_medicaux: Optional[str] = Field(default=None, examples=["drepanocytose", "thalassemie", "hemophile"])
    indication: Optional[str] =  Field(default=None, examples=["thombopenie severe a 47000"])
    statusVIH: Optional[bool] = Field(default=None, examples=[True, False])
    statusVHB: Optional[bool] = Field(default=None, examples=[True, False])
    statusVHC: Optional[bool] = Field(default=None, examples=[True, False])
    groupe_sanguin: Optional[str] = Field(default=None, examples=["A+"])
    groupe_sanguin_receveur: Optional[str] = Field(default=None, examples=["A+"])
    groupe_sanguin_nouveau_ne: Optional[str] = Field(default=None , examples=["A+"])
    phenotype: Optional[str] = Field(default=None, examples=[""])
    nature_du_produit_sanguin: Optional[str] = Field(default=None, examples=["CGR,CPS,CPF"])
    nombre_de_poches: Optional[int] = Field(default=None, examples=[35])
    antecedent_transfusionnel: Optional[int] = Field(default=None, examples=[2])
    RAI_positif: Optional[bool] = Field(default=None, examples=[True])
    taux_hemoglobine: Optional[float] = Field(default=None, examples=[15])
    programme: Optional[date] = Field(default=None, examples=["2024/01/02"])
    heure: Optional[time] = Field(default=None, examples=["10:30"])
    hospital: Optional[str] = Field(default=None, examples=["CHU"])
    service: Optional[str] = Field(default=None, examples=["service01"])
    medecin_demandeur: Optional[str] = Field(default=None, examples=["Dr. John Doe"])
    specialité: Optional[str] = Field(default=None, examples=["Cardiologie"])
    examens: Optional[str] = Field(default=None)
    estAnalyse: Optional[bool] = Field(default=None)
    date_transfusion: Optional[date] = Field(default=None, examples=["2024/01/02"])
    date_reception: Optional[date] = Field(default=None, examples=["2024/01/02"])
    date_retour_poche: Optional[date] = Field(default=None, examples=["2024/01/02"])
    motif: Optional[str] = Field(default=None, examples=["motif01"])
    test_compatibilite: Optional[str] = Field(default=None, examples=["test01"])
    is_phenotype_done: Optional[bool] = Field(default=None, examples=[True])
    is_test_compatibilite_done: Optional[bool] = Field(default=None, examples=[True])
    estDistribue: Optional[bool] = Field(default=None, examples=[True])



class BonDeSangResponseModel(BonDeSangUpdate):
    id: int
    id_user: int
    nom: Optional[str]
    prenom: Optional[str]
    dateDeNaissance: Optional[date]
    email: Optional[str]
    telephone: Optional[str]
    sexe: Optional[Sexe]
    patient_interne: Optional[bool]
    poids: Optional[int]
    chambre: Optional[str]
    lit: Optional[str]
    heure_demande: Optional[time]
    antecedent_medicaux: Optional[str]
    indication: Optional[str]
    statusVIH: Optional[bool]
    statusVHB: Optional[bool]
    statusVHC: Optional[bool]
    groupe_sanguin: Optional[str]
    groupe_sanguin_receveur: Optional[str]
    groupe_sanguin_nouveau_ne: Optional[str]
    phenotype: Optional[str]
    nature_du_produit_sanguin: Optional[str]
    nombre_de_poches: Optional[int]
    antecedent_transfusionnel: Optional[int]
    RAI_positif: Optional[bool]
    taux_hemoglobine: Optional[float]
    programme: Optional[date]
    heure: Optional[time]
    hospital: Optional[str]
    service: Optional[str]
    medecin_demandeur: Optional[str]
    specialité: Optional[str]
    examens: Optional[str]
    estAnalyse: Optional[bool]
    date_transfusion: Optional[date]
    date_reception: Optional[date]
    date_retour_poche: Optional[date]
    motif: Optional[str]
    test_compatibilite: Optional[str]
    params_receveurs: List[ParamsReceveurResponseModel]
    estDistribue: Optional[bool]
    is_phenotype_done: Optional[bool]
    is_test_compatibilite_done: Optional[bool]
    createdAt: datetime
    updatedAt: datetime
    examens: str