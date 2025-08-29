from fastapi import APIRouter, status, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from auth.deps import get_db, get_current_user
from models.users import User
from typing import List
from schemas.prelevements import PrelevementCreate, PrelevementDonneurResponseModel, PrelevementUpdate, PrelevementResponseModel
from database.dao.dao_prelevements import DaoPrelevement
from database.dao.dao_donneurs import DaoDonneur
from database.dao.dao_parametres import DaoParametre
from datetime import datetime, timedelta
from tasks import celery_app, scheduled_sms_task
from celery.schedules import crontab
import logging

PrevelementRouter = APIRouter()

@PrevelementRouter.get("", description="get all prelevement", response_model=List[PrelevementResponseModel])
def get_all_prelevements(estAnalyser: bool = False, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PrelevementResponseModel]:

    dao_prelevement = DaoPrelevement(db=db)

    return dao_prelevement.get_prelevements(estAnalyser= estAnalyser)

@PrevelementRouter.get("/without_phenotype_done", description="get all prelevement without phenotype done", response_model=List[PrelevementResponseModel])
def get_all_prelevements_without_phenotype_done(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PrelevementResponseModel]:

    dao_prelevement = DaoPrelevement(db=db)

    return dao_prelevement.get_prelevements_without_phenotype_done()


@PrevelementRouter.get("/with_donneur", description="get all prelevement with donneur", response_model=List[PrelevementDonneurResponseModel])
def get_all_prelevements_with_donneur(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PrelevementDonneurResponseModel]:

    dao_prelevement = DaoPrelevement(db=db)

    return dao_prelevement.get_prelevements_with_donneur()


@PrevelementRouter.get("/without_analyse_done", description="get all prelevement without analyse done", response_model=List[PrelevementResponseModel])
def get_all_prelevements_without_analyse_done(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PrelevementResponseModel]:

    dao_prelevement = DaoPrelevement(db=db)

    return dao_prelevement.get_prelevements_without_analyse_done()


@PrevelementRouter.get("/pagination", description="get all prelevement by pagination", response_model=List[PrelevementResponseModel])
def get_all_prelevements_by_pagination(estAnalyser: bool = False, skip:int =0, limit:int = 10, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[PrelevementResponseModel]:

    dao_prelevement = DaoPrelevement(db=db)

    return dao_prelevement.get_prelevements_by_pagination(estAnalyser= estAnalyser, skip=skip, limit=limit)


@PrevelementRouter.post("", response_model= PrelevementResponseModel, status_code=status.HTTP_201_CREATED)
def create_new_prelevement(prelevement_create: PrelevementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> PrelevementResponseModel:
    
    dao_prelevement = DaoPrelevement(db=db)
    dao_donneur = DaoDonneur(db=db)
    dao_parametre = DaoParametre(db=db)

    parametre_exist =  dao_parametre.get_parametre_by_id(parametre_id=prelevement_create.id_parametre)

    if not parametre_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Prelevement with {prelevement_create.id_parametre} you want to update don't exist")

    prelevement =  dao_prelevement.create_new_prelevement(prelevement=prelevement_create, id_user=user.id)

    dao_donneur.update_after_prelevment(id_donneur=prelevement.id_donneur) # update two field to null after his don
    
    donneur = dao_donneur.get_donneur_by_id(prelevement.id_donneur)
    message  = "Nous vous remercions pour votre don De sang, si vous avez des soucis veuillez contacter ce numéro 237691439424"

    scheduled_sms_task.apply_async(args=(donneur.telephone, message), eta=datetime.now() + timedelta(days=1))
    scheduled_sms_task.apply_async(args=(donneur.telephone, message), eta=datetime.now() + timedelta(days=2))


    return prelevement

@PrevelementRouter.put("/{id_prelevement}", description="update prevelement", response_model=PrelevementResponseModel)
def update_prelevement(id_prelevement:int,prelevement_update: PrelevementUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> PrelevementResponseModel:

    dao_prelevement = DaoPrelevement(db=db)

    prelevement_exist = dao_prelevement.get_prelevement_by_id(id_prelevement=id_prelevement)

    if not prelevement_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Prelevement with {id_prelevement} you want to update don't exist")

    result = dao_prelevement.update_prelevement(id_prelevement=id_prelevement, prevelement_update=prelevement_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Prelevement")

    return dao_prelevement.get_prelevement_by_id(id_prelevement=id_prelevement)


@PrevelementRouter.delete("/{id_prelevement}", description= "delete prelevement")
def delete_prelevement(id_prelevement: int, db: Session = Depends(get_db), user: User =Depends(get_current_user)):

    dao_prelevement = DaoPrelevement(db=db)

    prelevement_exist = dao_prelevement.get_prelevement_by_id(id_prelevement=id_prelevement)

    if not prelevement_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"prevelement with id {id_prelevement} don't exist in database")

    dao_prelevement.delete_prelevement(prelevement_exist)

    return HTTPException(status_code=status.HTTP_200_OK, detail=f"prelevement with id {prelevement_exist.id} successfully deleted")


@PrevelementRouter.post("/{id_prelevement}/archive", description="archive prevelement", response_model=PrelevementResponseModel)
def archive_prelevement(id_prelevement:int, estArchive: bool = Body(...), db: Session = Depends(get_db), user: User = Depends(get_current_user))-> PrelevementResponseModel:

    dao_prelevement = DaoPrelevement(db=db)

    prelevement_exist = dao_prelevement.get_prelevement_by_id(prelevement_id=id_prelevement)

    if not prelevement_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Prelevement with {id_prelevement} you want to update don't exist")

    result = dao_prelevement.update_prelevement_archive(id_prelevement=id_prelevement, estArchive=estArchive)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Prelevement")

    return dao_prelevement.get_prelevement_by_id(prelevement_id=id_prelevement)

@PrevelementRouter.get("/{id_prelevement}/examens", description="get all emamen of prelevement")
def get_all_examen_of_prelevement(id_prelevement:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_prelevement = DaoPrelevement(db=db)

    prelevement_exist = dao_prelevement.get_prelevement_by_id(prelevement_id=id_prelevement)

    if not prelevement_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Prelevement with {id_prelevement} you want to update don't exist")

    return prelevement_exist.examens