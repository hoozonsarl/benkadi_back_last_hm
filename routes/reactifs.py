from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from schemas.reactifs import ReactifCreate, ReactifUpdate, ReactifResponseModel
from typing import List
from database.dao.dao_reactifs import DaoReactif

from auth.deps import get_db, get_current_user
from models.users import User


ReactifRouter = APIRouter()


@ReactifRouter.get("", description="get all Reactif", response_model=List[ReactifResponseModel])
def get_all_Reactif(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ReactifResponseModel]:

    dao_Reactif = DaoReactif(db=db)
    Reactifs = dao_Reactif.get_all_reactifs()
    return Reactifs

@ReactifRouter.get("/{numero_code_bar}", description="get Reactif by numero_code_bar", response_model=ReactifResponseModel)
def get_Reactif_by_numero_code_bar(numero_code_bar: str, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ReactifResponseModel:

    dao_Reactif = DaoReactif(db=db)
    Reactif = dao_Reactif.get_reactif_by_code_bar(numero_code_bar=numero_code_bar)

    if not Reactif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reactif with code bar {numero_code_bar} not found"
        )

    return Reactif

@ReactifRouter.get("/{nom}", description="get Reactif by nom", response_model=ReactifResponseModel)
def get_Reactif_by_nom(nom: str, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ReactifResponseModel:

    dao_Reactif = DaoReactif(db=db)
    reactif = dao_Reactif.get_reactif_by_name(nom=nom)
    
    if not reactif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reactif with name {nom} not found"
        )
        
    return reactif

@ReactifRouter.post("", description="create a Reactif", response_model=ReactifResponseModel)
def create_new_Reactif(Reactif_create: ReactifCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> ReactifResponseModel:

    dao_Reactif = DaoReactif(db=db)

    Reactif_exist = dao_Reactif.get_reactif_by_name(nom=Reactif_create.nom)

    if Reactif_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reactif with nom: {Reactif_create.nom} already exist in database")


    Reactifs= dao_Reactif.create_new_reactif(id_user=user.id, reactif_create=Reactif_create)
            
    return Reactifs

@ReactifRouter.put("/{id_Reactif}", description="Update Reactif", response_model=ReactifResponseModel)
def update_Reactif(id_Reactif: int, Reactif_update: ReactifUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ReactifResponseModel:

    dao_Reactif = DaoReactif(db=db)

    Reactif_exist = dao_Reactif.get_reactif_by_id(id_reactif=id_Reactif)

    if not Reactif_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reactif with id{id_Reactif} don't exist in database")


    result = dao_Reactif.update_reactif(id_reactif=id_Reactif, reactif_update=Reactif_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error dring the update Reactif")

    return dao_Reactif.get_reactif_by_id(id_reactif=id_Reactif)

@ReactifRouter.delete("/{id_Reactif}", description=f"Delete de Reactif", status_code=status.HTTP_204_NO_CONTENT)
def delete_Reactif(id_Reactif: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_Reactif = DaoReactif(db=db)

    Reactif_exist = dao_Reactif.get_reactif_by_id(id_reactif=id_Reactif)

    if not Reactif_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reactif with id: {id_Reactif} you want to update don't exist")
    dao_Reactif.delete_reactif(reactif=Reactif_exist)

    
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Reactif with id: {id_Reactif} successfully deleted")



#soft delete
@ReactifRouter.delete("/soft_delete/{id_Reactif}", description=f"Delete de Reactif", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_Reactif(id_Reactif: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_Reactif = DaoReactif(db=db)

    Reactif_exist = dao_Reactif.get_reactif_by_id(id_reactif=id_Reactif)
    
    if not Reactif_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reactif with id: {id_Reactif} you want to update don't exist")
    
    dao_Reactif.soft_delete_reactif(id_reactif=id_Reactif)

    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Reactif with id: {id_Reactif} successfully deleted")

