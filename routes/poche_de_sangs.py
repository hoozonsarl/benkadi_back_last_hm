from database.dao.dao_donneursUsers import DaoDonneurUsers
from database.dao.dao_logs import DaoLogs
from fastapi import APIRouter, status, HTTPException, Depends, Query
from models.fractions import Fraction
from schemas.logs import LogsCreate
from sqlalchemy.orm import Session
from auth.deps import get_current_user, get_db
from database.dao.dao_prelevements import DaoPrelevement
from models.users import User
from typing import List, Optional
from schemas.poches_de_sangs import PocheDeSangCreate, PocheDeSangUpdate, PocheDeSangResponseModel
from schemas.fractions import FractionCreate, FractionUpdate, FractionResponseModel
from database.dao.dao_poche_de_sangs import DaoPocheDeSang
from database.dao.dao_fractions import DaoFraction
from database.dao.dao_donneurs import DaoDonneur
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tasks import celery_app, scheduled_sms_task
from models.prelevements import Prelevement

PocheDeSangRouter = APIRouter()


@PocheDeSangRouter.get("", description="get all poche de sang")
def get_all_poche_de_sangs(estFractionne: bool = False, is_phenotype_done: Optional[bool] = False, estDetruire: bool = False, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PocheDeSangResponseModel]:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_all_poche_de_sangs(estFractionne=estFractionne, is_phenotype_done=is_phenotype_done, estDetruire=estDetruire)

    return poche_de_sang

@PocheDeSangRouter.get("/without_analyse_done", description="get all poche de sang without analyse done")
def get_all_poche_de_sangs_without_analyse_done(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PocheDeSangResponseModel]:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_all_poche_de_sangs_without_analyse_done()

    return poche_de_sang

@PocheDeSangRouter.get("/destroy", description="get all poche de sang destroy")
def get_all_poche_de_sangs_destroy(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PocheDeSangResponseModel]:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_all_poche_de_sangs_destroy()

    return poche_de_sang

@PocheDeSangRouter.get("/with_analyse_done", description="get all poche de sang with analyse done")
def get_all_poche_de_sangs_with_analyse_done(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PocheDeSangResponseModel]:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_all_poche_de_sangs_with_analyse_done()

    return poche_de_sang

@PocheDeSangRouter.get("/pagination")
def get_all_poche_de_sangs(estFractionne: bool = False, skip:int= 0, limit:int =100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PocheDeSangResponseModel]:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_poche_de_sangs_by_pagination(estFractionne=estFractionne, skip=skip, limit=limit)

    return poche_de_sang

@PocheDeSangRouter.get("/{id_donneur}", description="get poche de sang of a donneur") 
def get_poche_de_sangs_of_a_donneur(id_donneur: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> PocheDeSangResponseModel:

    dao_poches_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang = dao_poches_de_sang.get_poche_of_a_donneur(id_donneur=id_donneur)

    return poche_de_sang

@PocheDeSangRouter.post("", description="Create a new blood bag", response_model=PocheDeSangResponseModel)
def create_new_poche_de_sang(
    poche_de_sang_create: PocheDeSangCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
) -> PocheDeSangResponseModel:
    # Initialize data access objects
    dao_poche_de_sang = DaoPocheDeSang(db=db)
    dao_donneur = DaoDonneur(db=db)
    dao_prelevement = DaoPrelevement(db=db)
    dao_donneurUsers = DaoDonneurUsers(db=db)
    dao_logs = DaoLogs(db=db)
    
    # Validate required records exist
    donneur = dao_donneur.get_donneur_by_id(donneur_id=poche_de_sang_create.id_donneur)
    if not donneur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor with ID {poche_de_sang_create.id_donneur} not found"
        )
    
    prelevement = dao_prelevement.get_prelevement_by_id(id_prelevement=poche_de_sang_create.id_prelevement)
    if not prelevement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection record with ID {poche_de_sang_create.id_prelevement} not found"
        )
    
    # Define donation interval constants
    MALE_DONATION_INTERVAL_MONTHS = 3
    FEMALE_DONATION_INTERVAL_MONTHS = 4
    
    # Calculate next donation date based on donor gender
    donation_interval = MALE_DONATION_INTERVAL_MONTHS if donneur.sexe == "HOMME" else FEMALE_DONATION_INTERVAL_MONTHS
    date_prochain_don = datetime.today() + relativedelta(months=donation_interval)
    interval_text = f"{donation_interval} mois"
    
    # Begin transaction
    try:
        # Step 1: Create new blood bag
        poche_de_sang = dao_poche_de_sang.create_new_poche_de_sang(
            id_user=user.id, 
            poche_de_sang_create=poche_de_sang_create
        )
        print("poche_de_sang", poche_de_sang)
        
        # Step 2: Update donor information
        donneur.dateDeProchainDon = date_prochain_don.date()
        donneur.last_don_date = datetime.today().date()
        donneur.is_don_done = True
        donneur.final_comment = "Le donneur a effectué un don de sang avec succès"
        donneur.groupeSanguin = poche_de_sang_create.groupeSanguin
            
        # Step 3: Update donor user record (if it exists)
        print("donneur.id_donneurUser", donneur.id_donneurUser)
        if donneur.id_donneurUser:
            print("donneur.id_donneurUser", donneur.id_donneurUser)
            try:
                # dao_donneurUsers.update_donneurUsers_is_don_done(
                #     id_donneurUsers=donneur.id_donneurUser, 
                #     groupeSanguin=poche_de_sang_create.groupeSanguin, 
                #     date_prochain_don=date_prochain_don
                # )
                donneurUser= dao_donneurUsers.get_donneurUsers_by_id(donneurUsers_id=donneur.id_donneurUser)
                if donneurUser:
                    donneurUser.groupeSanguin = poche_de_sang_create.groupeSanguin
                    donneurUser.is_don_done = True
                    donneurUser.last_don_date = datetime.today().date()
                    donneurUser.dateDeProchainDon = date_prochain_don.date()
                    # Handle the None case for donation count
                    if donneurUser.nombreDeDonsGenyco is None:
                        donneurUser.nombreDeDonsGenyco = 1
                    else:
                        donneurUser.nombreDeDonsGenyco += 1
        
                    donneurUser.final_comment = "Il a effectué un don de sang avec succès"
                    donneurUser.isDelayed = False
                    donneurUser.isDelayedDate = None
            except Exception as e:
                print(f"Warning: Failed to update donor user record: {str(e)}")
                # Continue processing - this isn't critical
        
        # Step 4: Update collection record's phenotype status
        print("poche_de_sang_create.id_prelevement", poche_de_sang_create.id_prelevement)
    
        try:
            #dao_prelevement.make_phenotype_done(id_prelevement=poche_de_sang_create.id_prelevement)
            prelevement = dao_prelevement.get_prelevement_by_id(id_prelevement=poche_de_sang_create.id_prelevement)
            if prelevement:
                prelevement.is_phenotype_done = True
            print("poche_de_sang_create.id_prelevement", poche_de_sang_create.id_prelevement)
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="groupage et phenotype du donneur "+donneur.nom+" "+donneur.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="groupage et phenotype",
            status="success",
            id_utilisateur=user.id
          ))
        except Exception as e:
            print(f"Warning: Failed to update phenotype status: {str(e)}")
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="tentative de groupage et phenotype du donneur "+donneur.nom+" "+donneur.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="groupage et phenotype",
                status="error",
                id_utilisateur=user.id
            ))
        
        # Step 5: Schedule reminder SMS
        message = (
            f"Nous vous remercions pour votre don de sang que vous avez fait il y a {interval_text}. "
            f"Vous êtes de nouveau éligible pour faire un don de sang. "
            f"Veuillez vous présenter à l'hôpital pour votre prochain don."
        )
        
        try:
            print("donneur.telephone", donneur.telephone)
            scheduled_sms_task.apply_async(
                args=(donneur.telephone, message), 
                eta=date_prochain_don
            )
        except Exception as sms_error:
            # Log SMS scheduling error but continue with the process
            print(f"Warning: Failed to schedule reminder SMS: {str(sms_error)}")
        
        # Commit all changes at once at the end
        db.commit()
        
        return poche_de_sang
    except Exception as e:
        # Rollback the transaction on error
        db.rollback()
        print(f"Error creating blood bag: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create blood bag: {str(e)}"
        )


@PocheDeSangRouter.put("/{id_poche_de_sang}", description="update poche de sang")
def update_poche_de_sang(id_poche_de_sang: int, poche_de_sang_update: PocheDeSangUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> PocheDeSangResponseModel:
    dao_poche_de_sang = DaoPocheDeSang(db=db)
    dao_logs = DaoLogs(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    result = dao_poche_de_sang.update_poche_de_sang(id_poche_de_sang=id_poche_de_sang, poche_de_sang_update=poche_de_sang_update)
    dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
        action="analyse de la poche de sang",
        nom_utilisateur=user.nom+" "+user.prenom,
        date_action=datetime.now(),
        ressource="poche de sang",
        status="success",
        id_utilisateur=user.id
    ))
    if not result:
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="tentative d'analyse de la poche de sang",
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="poche de sang",
            status="error",
            id_utilisateur=user.id
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during update Poche de sang")
    
    # dao_prelevement = DaoPrelevement(db=db)
    # dao_prelevement.make_analyse(id_prelevement=poche_de_sang_exist.id_prelevement)

  # Si estvalide est True dans le body, mettre à jour toutes les fractions liées
    if poche_de_sang_update.estvalide and poche_de_sang_update.estvalide == True:
        # Récupérer toutes les fractions liées à cette poche de sang
        fractions = db.query(Fraction).filter(Fraction.id_poche_de_sang == id_poche_de_sang).all()
        
        # Mettre à jour is_ok_to_use pour chaque fraction
        for fraction in fractions:
            fraction.is_ok_to_use = True
        
        # Sauvegarder les modifications dans la base de données
        db.commit()
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="validation de la poche de sang",
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="poche de sang",
            status="success",
            id_utilisateur=user.id
        ))
    # Si estDetruire est True dans le body, mettre à jour toutes les fractions liées
    if poche_de_sang_update.estDetruire and poche_de_sang_update.estDetruire == True:
        # Récupérer toutes les fractions liées à cette poche de sang
        fractions = db.query(Fraction).filter(Fraction.id_poche_de_sang == id_poche_de_sang).all()
        
        # Mettre à jour is_destroy pour chaque fraction
        for fraction in fractions:
            fraction.is_destroy = True
        
        # Sauvegarder les modifications dans la base de données
        db.commit()
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="destruction de la poche de sang",
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="poche de sang",
            status="success",
            id_utilisateur=user.id
        ))
    return dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)

@PocheDeSangRouter.delete("/{id_poche_de_sang}")
def delete_poche_de_sang(id_poche_de_sang:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    dao_poche_de_sang = DaoPocheDeSang(db=db)
    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    dao_poche_de_sang.delete_poche_de_sang(poche_de_sang_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Poche de sang with id {id_poche_de_sang} successfully deleted")


@PocheDeSangRouter.get("/{id_poche_de_sang}/fractions", description="get all fractions by estArchive or estDistribue", response_model=List[FractionResponseModel])
def get_all_fractions(id_poche_de_sang:int, estArchive: bool = Query(default=False), estDistribue: bool = Query(default=False), db: Session = Depends(get_db,), user: User = Depends(get_current_user))-> List[FractionResponseModel]:

    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    dao_fraction = DaoFraction(db=db)

    fractions  = dao_fraction.get_all_fraction_distribue_archive(estArchive=estArchive,estDistribue=estDistribue)
    return fractions


@PocheDeSangRouter.post("/{id_poche_de_sang}/fractions")
def create_new_fraction(id_poche_de_sang: int, fraction_create: FractionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    dao_fraction = DaoFraction(db=db)
    fraction = dao_fraction.create_new_fraction(id_poche_de_sang=id_poche_de_sang, fraction_create=fraction_create)
    return fraction


@PocheDeSangRouter.put("/{id_poche_de_sang}/fractions/{id_fraction}", description="update fraction of poche de sang", response_model=FractionResponseModel)
def update_fraction(id_poche_de_sang: int, id_fraction:int , fraction_update: FractionUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> FractionResponseModel:

    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    
    dao_fraction = DaoFraction(db=db)
    fraction_exist = dao_fraction.get_fraction_by_id(id_fraction=id_fraction)

    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction with id: {id_fraction} don't exist in database")
    
    result  =  dao_fraction.update_fraction(id_fraction=id_fraction, fraction_update=fraction_update)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Fraction")
    return dao_fraction.get_fraction_by_id(id_fraction=id_fraction)


@PocheDeSangRouter.post("/{id_poche_de_sang}/fractions/{id_fraction}/archive", description="update fraction of poche de sang", response_model=FractionResponseModel)
def archive_fraction(id_poche_de_sang: int, id_fraction:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> FractionResponseModel:

    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    dao_fraction = DaoFraction(db=db)
    fraction_exist = dao_fraction.get_fraction_by_id(id_fraction=id_fraction)
    print(fraction_exist)
    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction with id: {id_fraction} don't exist in database")
    
    result  =  dao_fraction.archive_fraction(id_fraction=id_fraction)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Fraction")
    return dao_fraction.get_fraction_by_id(id_fraction=id_fraction)

@PocheDeSangRouter.delete("/{id_poche_de_sang}/fractions/{id_fraction}", description="delete fraction of poche de sang")
def delete_fraction(id_poche_de_sang:int, id_fraction: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    
    dao_fraction = DaoFraction(db=db)
    fraction_exist = dao_fraction.get_fraction_by_id(id_fraction=id_fraction)

    if not fraction_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Fraction with id: {id_fraction} don't exist in database")
    
    dao_fraction.delete_fraction(fraction_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Fraction with id {id_fraction} successfully delete")


@PocheDeSangRouter.get("/{id_poche_de_sang}/examens", description="get  all examen of poche de sang")
def get_all_examen_of_poche_de_sang(id_poche_de_sang:int , db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    dao_poche_de_sang = DaoPocheDeSang(db=db)

    poche_de_sang_exist = dao_poche_de_sang.get_poche_de_sang_by_id(id_poche_de_sang=id_poche_de_sang)
    
    if not poche_de_sang_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Poche de sang with id: {id_poche_de_sang} don't exist in database")
    
    return poche_de_sang_exist.examens