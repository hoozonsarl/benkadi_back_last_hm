from datetime import datetime
from database.dao.dao_logs import DaoLogs
from database.utils import generate_username
from fastapi import APIRouter, status, HTTPException, Depends
from auth.deps import get_current_user, get_db
from database.dao.dao_bon_de_sangs import DaoBonDeSang
from database.dao.dao_receveurs import DaoReceveur
from models.bon_de_sang import BonDeSang
from schemas.logs import LogsCreate
from schemas.receveurs import ReceveurUpdate
from sqlalchemy.orm import Session
from models.users import User
from schemas.bon_de_sang import BonDeSangCreate, BonDeSangUpdate, BonDeSangResponseModel
from typing import Optional, List


bonDeSangRouter = APIRouter()


@bonDeSangRouter.get("", description="get all bon de sangs", response_model=List[BonDeSangResponseModel])
def get_all_bon_de_sangs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_bon_de_sang = DaoBonDeSang(db=db)

    bon_de_sangs = dao_bon_de_sang.get_all_bon_de_sangs()

    return bon_de_sangs


@bonDeSangRouter.get("/list", description="get all bon de sangs", response_model=List[BonDeSangResponseModel])
def get_list_bon_de_sangs(estDistribue: Optional[bool] = None, estAnalyse: Optional[bool] = None, is_phenotype_done: Optional[bool] = None, is_test_compatibilite_done: Optional[bool] = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_bon_de_sang = DaoBonDeSang(db=db)

    bon_de_sangs = dao_bon_de_sang.get_list_bon_de_sangs(estDistribue=estDistribue, estAnalyse=estAnalyse, is_phenotype_done=is_phenotype_done, is_test_compatibilite_done=is_test_compatibilite_done)

    return bon_de_sangs


@bonDeSangRouter.post("")
def create_a_new_bon_sangs(bon_de_sang_create: BonDeSangCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_bon_de_sangs = DaoBonDeSang(db=db)
    dao_receveurs = DaoReceveur(db=db)
    dao_logs = DaoLogs(db=db)


    username = generate_username(bon_de_sang_create.nom, bon_de_sang_create.prenom)

    receveur_exist = dao_receveurs.get_receveur_by_userName_and_dateDeNaissance(userName=username, dateDeNaissance=bon_de_sang_create.dateDeNaissance)
    print("receveur_exist", receveur_exist)

    if receveur_exist:
        bon_de_sang = dao_bon_de_sangs.create_bon_de_sang(id_user=user.id, bon_de_sang_create=bon_de_sang_create, id_receveur=receveur_exist.id, userName=username)
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="creation du bon de sang pour le receveur "+receveur_exist.nom+" "+receveur_exist.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="bon de sang",
            status="success",
            id_utilisateur=user.id
        ))
    else:
        receveur = dao_receveurs.create_new_receveur(id_user=user.id, receveur=bon_de_sang_create)
        print("receveur", receveur)
        bon_de_sang = dao_bon_de_sangs.create_bon_de_sang(id_user=user.id, bon_de_sang_create=bon_de_sang_create, id_receveur=receveur.id, userName=username)
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="creation du bon de sang pour le receveur "+bon_de_sang_create.nom+" "+bon_de_sang_create.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="bon de sang",
            status="success",
            id_utilisateur=user.id
        ))
    return bon_de_sang  


# @bonDeSangRouter.put("/{id_bon_de_sang}", description="update bon de sang", response_model=BonDeSangResponseModel)
# def update_bon_de_sang(id_bon_de_sang: int, bon_de_sang_update: BonDeSangUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

#     dao_bon_de_sang = DaoBonDeSang(db=db)
#     dao_receveurs = DaoReceveur(db=db)

#     bon_de_sang_exist = dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=id_bon_de_sang)

#     if not bon_de_sang_exist:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bon de sang with id: {id_bon_de_sang} don't exist in database")

#     result = dao_bon_de_sang.update_bon_de_sang(id_bon_de_sang=id_bon_de_sang, bon_de_sang_update=bon_de_sang_update)
#     dao_receveurs.update_receveur(id_receveur=bon_de_sang_exist.id_receveur, receveur_update=bon_de_sang_update)

#     if not result:

#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during the update of Bon de sang")
    
#     return dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=id_bon_de_sang)



@bonDeSangRouter.put("/{id_bon_de_sang}", description="update bon de sang", response_model=BonDeSangResponseModel)
def update_bon_de_sang(id_bon_de_sang: int, bon_de_sang_update: BonDeSangUpdate, 
                        db: Session = Depends(get_db), 
                        user: User = Depends(get_current_user)):
    
    # Create DAOs
    dao_bon_de_sang = DaoBonDeSang(db=db)
    dao_receveur = DaoReceveur(db=db)
    dao_logs = DaoLogs(db=db)
    
    # Get the existing blood donation form
    bon_de_sang_exist = dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=id_bon_de_sang)
    print("bon_de_sang_exist", bon_de_sang_exist)
    
    if not bon_de_sang_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Bon de sang with id: {id_bon_de_sang} doesn't exist in database"
        )
    
    # Get the associated recipient
    receveur = dao_receveur.get_receveur_by_id(reveveur_id=bon_de_sang_exist.id_receveur)
    print("receveur", receveur)
    
    if not receveur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Associated recipient with id: {bon_de_sang_exist.id_receveur} not found"
        )
    
    # Start a transaction
    try:
        # 1. Update the blood donation form
        result = dao_bon_de_sang.update_bon_de_sang(
            id_bon_de_sang=id_bon_de_sang, 
            bon_de_sang_update=bon_de_sang_update
        )
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="update du bon de sang pour le receveur "+receveur.nom+" "+receveur.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="bon de sang",
            status="success",
            id_utilisateur=user.id
        ))
        if bon_de_sang_update.is_phenotype_done:
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="phenotype et groupage du bon de sang pour le receveur "+receveur.nom+" "+receveur.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="bon de sang",
                status="success",
                id_utilisateur=user.id
            ))
        if bon_de_sang_update.is_test_compatibilite_done:
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="test de compatibilite du bon de sang pour le receveur "+receveur.nom+" "+receveur.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="bon de sang",
                status="success",
                id_utilisateur=user.id
            ))
        if not result:
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="tentative d'update du bon de sang pour le receveur "+receveur.nom+" "+receveur.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="bon de sang",
                status="error",
                id_utilisateur=user.id
            ))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Error during the update of Bon de sang"
            )
        
        # 2. Check if we need to update shared fields in the recipient record
        receveur_update_dict = {}
        shared_fields = [
            'nom', 'prenom', 'dateDeNaissance', 'telephone', 'email', 
            'sexe', 'groupe_sanguin', 'groupe_sanguin_receveur', 'phenotype', 
            'hospital', 'service'
        ]
        
        update_data = bon_de_sang_update.dict(exclude_unset=True, exclude_none=True)
        
        # Build recipient update dictionary with only the shared fields that were updated
        for field in shared_fields:
            if field in update_data:
                receveur_update_dict[field] = update_data[field]
        
        # 3. If name or first name changed, regenerate username
        username_changed = False
        if ('nom' in receveur_update_dict or 'prenom' in receveur_update_dict):
            # Get current values, use updated values where available
            new_nom = receveur_update_dict.get('nom', receveur.nom)
            new_prenom = receveur_update_dict.get('prenom', receveur.prenom)
            
            # Generate new username
            new_username = generate_username(new_nom, new_prenom)
            
            # Only update if it actually changed
            if new_username != receveur.userName:
                receveur_update_dict['userName'] = new_username
                username_changed = True
                
                # Also need to update the username in the bon_de_sang
                db.query(BonDeSang).filter(BonDeSang.id == id_bon_de_sang).update(
                    {'userName': new_username}
                )
        
        # 4. Update the recipient if we have changes
        if receveur_update_dict:
            # Convert to ReceveurUpdate model
            receveur_update = ReceveurUpdate(**receveur_update_dict)
            
            # Update the recipient
            update_result = dao_receveur.update_receveur(
                id_receveur=bon_de_sang_exist.id_receveur,
                receveur_update=receveur_update
            )
            
            if not update_result:
                # If recipient update fails, rollback and return error
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Error during synchronization of recipient data"
                )
        
        # Commit all changes
        db.commit()
        
        # Return updated blood donation form
        return dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=id_bon_de_sang)
    
    except Exception as e:
        # Rollback in case of any error
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="tentative d'update du bon de sang pour le receveur "+receveur.nom+" "+receveur.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="bon de sang",
            status="error",
            id_utilisateur=user.id
        ))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred during update: {str(e)}"
        )
    

@bonDeSangRouter.delete("/{id_bon_de_sang}")
def delete_bon_sang(id_bon_de_sang: int, db: Session =Depends(get_db), user: User = Depends(get_current_user)):

    dao_bon_de_sang = DaoBonDeSang(db=db)

    bon_de_sang_exist = dao_bon_de_sang.get_bon_de_sang_by_id(id_bon_de_sang=id_bon_de_sang)

    if not bon_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"bon de sang with id: {id_bon_de_sang}")
    
    dao_bon_de_sang.delete(bon_de_sang=bon_de_sang_exist)
    
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Donneur with id {id_bon_de_sang} successfully deleted")
