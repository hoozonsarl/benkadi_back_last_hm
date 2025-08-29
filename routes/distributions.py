from datetime import datetime
from database.dao.dao_logs import DaoLogs
from schemas.logs import LogsCreate
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from schemas.distributions import DistributionCreate, DistributionUpdate, DistributionResponseModel
from typing import List
from database.dao.dao_distributions import DaoDistribution
from database.dao.dao_fractions import DaoFraction
from database.dao.dao_bon_de_sangs import DaoBonDeSang
from auth.deps import get_db, get_current_user
from models.users import User
from database.dao.dao_receveurs import DaoReceveur

DistributionRouter = APIRouter()


@DistributionRouter.get("", description="get all distribution", response_model=List[DistributionResponseModel])
def get_all_distribution(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DistributionResponseModel]:

    dao_distribution = DaoDistribution(db=db)
    distributions = dao_distribution.get_all_distributions()
    return distributions

@DistributionRouter.post("", description="create a distribution", response_model=List[DistributionResponseModel])
def create_new_distribution(distribution_create: DistributionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[DistributionResponseModel]:

    dao_distribution = DaoDistribution(db=db)
    dao_bon_de_sang = DaoBonDeSang(db=db)
    dao_fraction = DaoFraction(db=db)
    dao_logs = DaoLogs(db=db)

    bon_de_sang_exist = dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=distribution_create.id_bon_de_sang)
    if not bon_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bon de sang with id: {distribution_create.id_bon_de_sang} don't exist in database")

    distributions = dao_distribution.create_distribution(distribution_create=distribution_create, id_user=user.id)
    dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
        action="creation de la distribution pour le bon de sang "+bon_de_sang_exist.nom+" "+bon_de_sang_exist.prenom,
        nom_utilisateur=user.nom+" "+user.prenom,
        date_action=datetime.now(),
        ressource="distribution",
        status="success",
        id_utilisateur=user.id
    ))
    results = []
    
    fractions = [dao_fraction.get_fraction_by_id(id_fraction=id_fraction) for id_fraction in distribution_create.id_fractions]

    for  fraction in fractions:
        if not fraction:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"One of this {distribution_create.id_fractions} fractions  don't exist in database")
    
    bon_de_sang_exist.estDistribue = True
    db.commit()
    db.refresh(bon_de_sang_exist)
    if distributions:
        
        result = dao_bon_de_sang.put_distribute(id_bon_de_sang=distribution_create.id_bon_de_sang) # mettre le bon de sang a estDistrubue

        # mettre estDistribue des fractions de poche de sang a True
        for id_fraction in distribution_create.id_fractions:
            results.append(dao_fraction.archive_fraction(id_fraction=id_fraction))
            
    return distributions

@DistributionRouter.put("/{id_distribution}", description="Update distribution", response_model=DistributionResponseModel)
def update_distribution(id_distribution: int, distribution_update: DistributionUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DistributionResponseModel:

    dao_distribution = DaoDistribution(db=db)

    distribution_exist = dao_distribution.get_distribution_by_id(id_distribution=id_distribution)

    if not distribution_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Distribution with id{id_distribution} don't exist in database")


    result = dao_distribution.update_distribution(id_distribution=id_distribution, update_distribution=update_distribution)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error dring the update Distribution")

    return dao_distribution.get_distribution_by_id(id_distribution=id_distribution)

@DistributionRouter.delete("/{id_distribution}", description=f"Delete de Distribution", status_code=status.HTTP_204_NO_CONTENT)
def delete_distribution(id_distribution: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_distribution = DaoDistribution(db=db)

    distribution_exist = dao_distribution.get_distribution_by_id(id_distribution=id_distribution)

    if not distribution_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Distribution with id: {id_distribution} you want to update don't exist")
    dao_distribution.delete_distribution(distribution=distribution_exist)
    dao_fraction = DaoFraction(db=db)
    result = dao_fraction.de_archive_fraction(id_fraction=distribution_exist.id_fraction)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during de dearchive fraction during the delete distribution")
    
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Distribution with id: {id_distribution} successfully deleted")
