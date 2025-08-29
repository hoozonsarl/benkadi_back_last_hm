from database.dao.dao_logs import DaoLogs
from fastapi import APIRouter, status, HTTPException, Depends
from auth.deps import get_current_user, get_db
from models.fractions import Fraction
from database.dao.dao_poche_de_sangs import DaoPocheDeSang
from database.dao.dao_fraction_types import DaoFractionType
from models.users import User
from sqlalchemy.orm import Session
from schemas.fractions import FractionCreate, FractionUpdate, FractionResponseModel
from typing import List
from database.dao.dao_fractions import DaoFraction



FractionRouter = APIRouter()



@FractionRouter.get("", description="get all fraction", response_model=List[FractionResponseModel])
def get_all_fraction(estDistribue: bool = False, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[FractionResponseModel]:
    
    dao_fraction = DaoFraction(db=db)

    fractions = dao_fraction.get_all_fractions(estDistribue=estDistribue)

    return fractions

@FractionRouter.get("/dashboard", description="dashboard statistique")
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_fraction = DaoFraction(db=db)

    dashborad = dao_fraction.etat_de_stock()

    return dashborad


@FractionRouter.get("/non_qualifier", description="dashboard statistique non qualifier")
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_fraction = DaoFraction(db=db)

    dashborad = dao_fraction.etat_de_stock_non_qualifier()

    return dashborad

@FractionRouter.get("/destroy", description="dashboard statistique destroy")
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_fraction = DaoFraction(db=db)

    dashborad = dao_fraction.etat_de_stock_destroy()

    return dashborad


@FractionRouter.get("/quarantaine", description="dashboard statistique quarantaine")
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_fraction = DaoFraction(db=db)

    dashborad = dao_fraction.etat_de_stock_quarantaine()

    return dashborad


@FractionRouter.post("", description="create a new fraction", response_model=FractionResponseModel)
def create_new_fraction(fraction: FractionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> FractionResponseModel:

    dao_fraction = DaoFraction(db=db)

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    dao_fraction_type = DaoFractionType(db=db)
    dao_logs = DaoLogs(db=db)

    poches_de_sang = dao_poches_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=fraction.id_poche_de_sang)

    if not poches_de_sang:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {fraction.id_poche_de_sang} don't exist in database")
    
    fraction_exist = dao_fraction_type.get_fraction_type_by_id(fraction_type_id=fraction.id_fraction_type)

    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction type with id: {fraction.id_fraction_type} don't exist in database")
    
    fraction_create = dao_fraction.create_new_fraction(id_poche_de_sang=fraction.id_poche_de_sang, fraction_create=fraction)
    poches_de_sang.estFractionne = True
    db.commit()
    db.refresh(poches_de_sang)

    return fraction_create


@FractionRouter.put("/{id_fraction}", description="Update fraction", response_model=FractionResponseModel)
def update_fraction(id_fraction:int,  fraction_update: FractionUpdate, db: Session = Depends(get_db), user: User = Depends(get_db))-> FractionResponseModel:

    dao_fraction = DaoFraction(db=db)

    fraction_exist =  dao_fraction.get_fraction_by_id(id_fraction=id_fraction)

    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"fraction with id {id_fraction} don't exist in database")

    result = dao_fraction.update_fraction(id_fraction=id_fraction, fraction_update=fraction_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during the update Fraction")
    
    return dao_fraction.get_fraction_by_id(id_fraction=id_fraction)


@FractionRouter.delete("{id_fraction}", description="delete fraction", status_code=status.HTTP_200_OK)
def delete_fraction(id_fraction: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_fraction = DaoFraction(db=db)

    fraction_exist = dao_fraction.get_fraction_by_id(id_fraction=id_fraction)

    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction with id: {id_fraction} don't exit in database")

    dao_fraction.delete_fraction(fraction=fraction_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Fraction with id: {id_fraction} successfully deleted")



