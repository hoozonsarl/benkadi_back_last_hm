from datetime import datetime
from database.dao.dao_logs import DaoLogs
from database.dao.dao_params_receveurs import DaoParamsReceveur
from fastapi import APIRouter, Depends
from schemas.logs import LogsCreate
from schemas.params_receveurs import ParamsReceveurCreate, ParamsReceveurResponseModel, ParamsReceveurUpdate
from sqlalchemy.orm import Session
from auth.deps import get_db, get_current_user
from models.users import User
from fastapi import HTTPException, status
from database.dao.dao_receveurs import DaoReceveur
from schemas.receveurs import ReceveurCreate, ReceveurResponseModel, ReceveurUpdate
from typing import List


ParamsReceveurRouter = APIRouter()



@ParamsReceveurRouter.post("", description="Create New Params Receveur", status_code=status.HTTP_201_CREATED)
def get_all_params_receveur(params_receveur_create: ParamsReceveurCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ParamsReceveurResponseModel:

    dao_params_receveur = DaoParamsReceveur(db=db)

    # receveur_exist_email = dao_receveur.get_receveur_by_email(email=receveur_create.email)
    # if receveur_exist_email:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Receveur with this email: {receveur_create.email} exist in database")
    
    # receveur_exist_telephone = dao_receveur.get_receveur_by_telephone(telephone=receveur_create.telephone)
    
    # if receveur_exist_telephone:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Receveur with this telephone: {receveur_create.email} exist in database")
    
    params_receveur = dao_params_receveur.create_new_params_receveur(id_user=user.id, params_receveur=params_receveur_create)

    return params_receveur


    


@ParamsReceveurRouter.get("")
def get_all_params_receveur(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ParamsReceveurResponseModel]:

    dao_params_receveur = DaoParamsReceveur(db=db)

    params_receveurs = dao_params_receveur.get_params_receveurs()

    return params_receveurs


@ParamsReceveurRouter.get("/pagination")
def get_all_params_receveur(skip:int = 0, limit:int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ParamsReceveurResponseModel]:

    dao_params_receveur = DaoParamsReceveur(db=db)

    params_receveurs = dao_params_receveur.get_params_receveurs_by_pagination(skip=skip, limit=limit)

    return params_receveurs




@ParamsReceveurRouter.put("/{id_params_receveur}", description="Update Params Receveur")
def update_params_receveur(id_params_receveur:int, params_receveur_update: ParamsReceveurUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_params_receveur = DaoParamsReceveur(db=db)
    dao_logs = DaoLogs(db=db)

    params_receveur_exist = dao_params_receveur.get_params_receveur_by_id(id_params_receveur=id_params_receveur)

    if not params_receveur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Params Receveur with id: {id_params_receveur} don't exist in database")
    
    result = dao_params_receveur.update_params_receveur(id_params_receveur=id_params_receveur, params_receveur_update=params_receveur_update)
    dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
        action="update des parametres du receveur",
        nom_utilisateur=user.nom+" "+user.prenom,
        date_action=datetime.now(),
        ressource="params receveur",
        status="success",
        id_utilisateur=user.id
    ))
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Permission")

    return dao_params_receveur.get_params_receveur_by_id(id_params_receveur=id_params_receveur)


@ParamsReceveurRouter.delete("/{id_params_receveur}", description="delete params receveur")
def delete_params_receveur(id_params_receveur:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_params_receveur = DaoParamsReceveur(db=db)

    params_receveur_exist = dao_params_receveur.get_params_receveur_by_id(id_params_receveur=id_params_receveur)

    if not params_receveur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Params Receveur with id: {id_params_receveur} don't exist in database")

    dao_params_receveur.delete_params_receveur(params_receveur=params_receveur_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"params receveur with id {id_params_receveur} successfully deleted")