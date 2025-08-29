from fastapi import APIRouter, Depends, status, HTTPException
from auth.deps import get_current_user, get_db
from sqlalchemy.orm import Session
from models.users import User
from schemas.fraction_types import FractionTypeResponseModel, FractionTypeCreate, FractionTypeUpdate 
from typing import List
from database.dao.dao_fraction_types import DaoFractionType

FractionTypeRouter = APIRouter()



@FractionTypeRouter.get("", description="get all fraction type", response_model=List[FractionTypeResponseModel])
def get_all_fraction_type(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[FractionTypeResponseModel]:

    dao_fraction_type = DaoFractionType(db=db)

    fraction_types = dao_fraction_type.get_fraction_types()
    
    return fraction_types

@FractionTypeRouter.post("", description="create a new Fraction Type", response_model=FractionTypeResponseModel, status_code=status.HTTP_201_CREATED)
def create_new_fraction_type(fraction_type_create: FractionTypeCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> FractionTypeResponseModel:
    
    dao_fraction_type = DaoFractionType(db=db)
    fraction_type_exist = dao_fraction_type.get_fraction_type_by_name(nom=fraction_type_create.nom)

    if fraction_type_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction Type with name: {fraction_type_create.nom} exist in database")

    fraction_type = dao_fraction_type.create_new_fraction_type(fraction_type=fraction_type_create)

    return fraction_type

@FractionTypeRouter.put("/{id_fraction_type}", description="Update Fraction Type", response_model=FractionTypeResponseModel)
def update_fraction_type(id_fraction_type:int, fraction_type_update: FractionTypeUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> FractionTypeResponseModel:

    dao_fraction_type = DaoFractionType(db=db)
    fraction_type_exist = dao_fraction_type.get_fraction_type_by_id(fraction_type_id=id_fraction_type)

    if not fraction_type_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"FractionType with id: {id_fraction_type} don't exist in database")

    result = dao_fraction_type.update_fraction_type(id_fraction_type=id_fraction_type,fraction_type_update=fraction_type_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Fraction Type")
    
    return dao_fraction_type.get_fraction_type_by_id(fraction_type_id=id_fraction_type)

@FractionTypeRouter.delete("/{id_fraction_type}", description="delete Farction Type", status_code=status.HTTP_200_OK)
def delete_fraction_type(id_fraction_type:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    dao_fraction_type = DaoFractionType(db=db)

    fraction_type_exist = dao_fraction_type.get_fraction_type_by_id(fraction_type_id=id_fraction_type)

    if not fraction_type_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fraction Type with id: {id_fraction_type} dont' exist in database")
    
    dao_fraction_type.delete_fraction_type(fraction_type=fraction_type_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Fraction Type with id: {id_fraction_type} successfully deleted")