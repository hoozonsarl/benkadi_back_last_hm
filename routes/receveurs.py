from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.deps import get_db, get_current_user
from models.users import User
from fastapi import HTTPException, status
from database.dao.dao_receveurs import DaoReceveur
from schemas.receveurs import ReceveurCreate, ReceveurResponseModel, ReceveurUpdate, ReceveurWithBonDeSangResponseModel
from typing import List


ReceveurRouter = APIRouter()



@ReceveurRouter.post("", description="Create New Receveur", status_code=status.HTTP_201_CREATED)
def get_all_receveur(receveur_create: ReceveurCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ReceveurResponseModel:

    dao_receveur = DaoReceveur(db=db)

    # receveur_exist_email = dao_receveur.get_receveur_by_email(email=receveur_create.email)
    # if receveur_exist_email:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Receveur with this email: {receveur_create.email} exist in database")
    
    # receveur_exist_telephone = dao_receveur.get_receveur_by_telephone(telephone=receveur_create.telephone)
    
    # if receveur_exist_telephone:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Receveur with this telephone: {receveur_create.email} exist in database")
    
    receveur = dao_receveur.create_new_receveur(id_user=user.id, receveur=receveur_create)

    return receveur


    


@ReceveurRouter.get("")
def get_all_receveur(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ReceveurWithBonDeSangResponseModel]:

    dao_receveur = DaoReceveur(db=db)

    receveurs = dao_receveur.get_receveurs()

    return receveurs


@ReceveurRouter.get("/pagination")
def get_all_receveur(skip:int = 0, limit:int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ReceveurResponseModel]:

    dao_receveur = DaoReceveur(db=db)

    receveurs = dao_receveur.get_receveurs_by_pagination(skip=skip, limit=limit)

    return receveurs




@ReceveurRouter.put("/{id_receveur}", description="Update Reveveur")
def update_receveur(id_receveur:int, receveur_update: ReceveurUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_receveur = DaoReceveur(db=db)

    receveur_exist = dao_receveur.get_receveur_by_id(reveveur_id=id_receveur)

    if not receveur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reveur with id: {id_receveur} don't exist in database")
    
    result = dao_receveur.update_receveur(id_receveur=id_receveur, receveur_update=receveur_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Permission")

    return dao_receveur.get_receveur_by_id(reveveur_id=id_receveur)


@ReceveurRouter.delete("/{id_receveur}", description="delete receveur")
def delete_receveur(id_receveur:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_receveur = DaoReceveur(db=db)

    receveur_exist = dao_receveur.get_receveur_by_id(reveveur_id=id_receveur)

    if not receveur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Receveur with id: {id_receveur} don't exist in database")

    dao_receveur.delete_receveur(receveur=receveur_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"permision with id {id_receveur} successfully deleted")