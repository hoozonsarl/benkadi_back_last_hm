from datetime import datetime
from database.dao.dao_donneursUsers import DaoDonneurUsers
from database.dao.dao_logs import DaoLogs
from database.dao.dao_prelevements import DaoPrelevement
from database.utils import generate_username
from fastapi import APIRouter, HTTPException, status, Depends
from auth.deps import get_db, get_current_user
from models.prelevements import VolumePrevele
from schemas.donneurs import DonneurCreate, DonneurUpdate, DonneurResponseModel
from schemas.donneursUsers import DonneurUsersUpdate
from schemas.logs import LogsCreate
from schemas.parametres import ParametreCreate, ParametreUpdate, ParametreResponseModel
from schemas.prelevements import PrelevementCreate
from schemas.smss import SMSCreate, SMSUpdate, SMSResponseModel
from sqlalchemy.orm import Session
from database.dao.dao_donneurs import DaoDonneur
from database.dao.dao_parametres import DaoParametre
from models.users import User
from database.dao.dao_smss import DaoSMS
from typing import List, Optional
from tasks import sendSMStoDonneur

DonneurRouter = APIRouter()



@DonneurRouter.get("", description="get list donneur", response_model=List[DonneurResponseModel])
def get_list_donneur(isValideMedecin: Optional[bool] = False, isValideAnalyseTDR: Optional[bool] = False, is_tdr_done: Optional[bool] = False, is_ok_prelevement: Optional[bool] = False, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_donneurs(isValideMedecin=isValideMedecin, isValideAnalyseTDR=isValideAnalyseTDR, is_tdr_done=is_tdr_done, is_ok_prelevement=is_ok_prelevement)

    return donneurs


@DonneurRouter.get("/tdr", description="get list donneur tdr", response_model=List[DonneurResponseModel])
def get_list_donneur_tdr( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_donneurs_by_is_tdr_done()

    return donneurs


@DonneurRouter.get("/all", description="get list donneur all", response_model=List[DonneurResponseModel])
def get_list_donneur_all( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_all_donneurs()

    return donneurs


@DonneurRouter.get("/temp", description="get list donneur temporaire", response_model=List[DonneurResponseModel])
def get_list_donneur_temp( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_temp_donneurs()

    return donneurs


@DonneurRouter.get("/ok", description="get list donneur ok prelevement", response_model=List[DonneurResponseModel])
def get_list_donneur_ok_prelevement( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_donneurs_by_is_ok_prelevement()

    return donneurs

@DonneurRouter.get("/rejected", description="get list donneur rejected", response_model=List[DonneurResponseModel])
def get_list_donneur_rejected( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs = dao_donneur.get_donneurs_by_is_rejected()

    return donneurs




@DonneurRouter.get("/pagination", description="get list donneur by pagination", response_model=List[DonneurResponseModel])
def get_list_donneur_by_pagination(isDonneur: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneurs_by_pagination = dao_donneur.get_donneurs_by_pagination(isDonneur=isDonneur, skip=skip, limit=limit)

    return donneurs_by_pagination



@DonneurRouter.post("", description="Create New Donneur", response_model=DonneurResponseModel)
def create_new_donneur(donneur_create: DonneurCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DonneurResponseModel:

    dao_donneur = DaoDonneur(db=db)
    dao_donneurUsers = DaoDonneurUsers(db=db)
    dao_logs = DaoLogs(db=db)

    userName = generate_username(donneur_create.nom, donneur_create.prenom)

    donneurUsers_exist = dao_donneurUsers.get_all_donneursUsers_by_userName_and_dateDeNaissance(userName=userName, dateDeNaissance=donneur_create.dateDeNaissance)
    print("donneurUsers_exist", donneurUsers_exist)

    if donneurUsers_exist:
        print("donneurUsers_exist", donneurUsers_exist)
        donneur = dao_donneur.create_new_donneur(id_user=user.id, donneur=donneur_create, id_donneurUser=donneurUsers_exist[0].id , userName=userName)
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="creation du donneur "+donneur.nom+" "+donneur.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="Donneur",
            status="success",
            id_utilisateur=user.id
        ))
    else:
        donneurUsers = dao_donneurUsers.create_new_donneurUsers(id_user=user.id, donneurUsers=donneur_create)
        print("donneurUsers", donneurUsers)
        donneur = dao_donneur.create_new_donneur(id_user=user.id, donneur=donneur_create, id_donneurUser=donneurUsers.id, userName=userName)
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="creation du donneur "+donneur.nom+" "+donneur.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="Donneur",
            status="success",
            id_utilisateur=user.id
        ))
    print("donneur", donneur)
    return donneur

# @DonneurRouter.put("/{id_donneur}", description="Update Donneur", response_model=DonneurResponseModel)
# def update_donneur(id_donneur: int, donneur_update: DonneurUpdate, db: Session = Depends(get_db), user: User =  Depends(get_current_user)):

#     dao_donneur = DaoDonneur(db=db)
#     dao_prelevement = DaoPrelevement(db=db)
#     donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur);

#     if  not donneur_exist:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Donneur don't exist in database")

#     result = dao_donneur.update_donneur(id_donneur=id_donneur, donneur_update=donneur_update)

#     if not result:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Donneur")
    
#     if donneur_update.is_ok_prelevement == True:
#         #create new prelevement
#         prelevement_create = PrelevementCreate(
#             id_donneur=id_donneur,
#             dateDePrelevement=datetime.now().date(),
#             heureDebut=datetime.now().time(),
#             heureFin=datetime.now().time(),
#             poidsDePoche=0,
#             volumePrevele=donneur_exist.parametres[0].quantite,
#             remarques="",
#             effetsIndesirables="",
#             id_parametre=donneur_exist.parametres[0].id
#         )
#         dao_prelevement.create_new_prelevement(id_user=user.id, prelevement=prelevement_create)


#     return dao_donneur.get_donneur_by_id(donneur_id=id_donneur)


@DonneurRouter.put("/{id_donneur}", description="Update Donneur", response_model=DonneurResponseModel)
def update_donneur(id_donneur: int, donneur_update: DonneurUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get necessary data access objects
    dao_donneur = DaoDonneur(db=db)
    dao_donneurUsers = DaoDonneurUsers(db=db)
    dao_prelevement = DaoPrelevement(db=db)
    dao_logs = DaoLogs(db=db)
    
    # First verify the donor exists
    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)
    print("donneur_exist", donneur_exist)
    if not donneur_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Donor with id: {id_donneur} doesn't exist in database"
        )
    
    # Use a regular transaction instead of nested
    try:
        # PART 1: Handle username changes if name/firstname is updated
        username_changed = False
        new_username = None
        
        if ((donneur_update.nom is not None and donneur_update.nom != donneur_exist.nom) or 
            (donneur_update.prenom is not None and donneur_update.prenom != donneur_exist.prenom)):
            
            # Get the new values (use existing if not being updated)
            new_nom = donneur_update.nom if donneur_update.nom is not None else donneur_exist.nom
            new_prenom = donneur_update.prenom if donneur_update.prenom is not None else donneur_exist.prenom
            
            # Generate new username
            new_username = generate_username(new_nom, new_prenom)
            
            # Only update if username actually changed
            if new_username != donneur_exist.userName:
                # Add username to donor update values
                donneur_update_dict = donneur_update.model_dump(exclude_unset=True)
                donneur_update_dict["userName"] = new_username
                donneur_update = DonneurUpdate(**donneur_update_dict)
                username_changed = True
        
        # PART 2: Update the donor record
        result = dao_donneur.update_donneur(id_donneur=id_donneur, donneur_update=donneur_update)
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="update du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="Donneur",
            status="success",
            id_utilisateur=user.id
        ))
        if not result:
            # Just need to raise an exception - the outer try/except will handle the rollback
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="tentative d'update du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="Donneur",
                status="error",
                id_utilisateur=user.id
            ))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Error updating donor record"
            )
        
        # PART 3: Prepare DonneurUsers update for synchronized fields
        if donneur_exist.id_donneurUser:
            # List of fields that should be synchronized between both models
            shared_fields = [
                'nom', 'prenom', 'dateDeNaissance', 'lieuDeNaissance', 'numeroCNI',
                'passport', 'carte_scolaire', 'carte_elec', 'carte_etudiant',
                'dateDelivranceIdCard', 'villeResidence', 'niveauEtude', 'permisConduire',
                'sexe', 'profession', 'statusMatrimonial', 'paysOrigine', 'religion',
                'adresse', 'telephone', 'email', 'groupeSanguin', 'dateDeProchainDon',
                'dateDernierDon', 'datePossibleDon', 'nombreDeDons', 'accidentDon',
                'dejaTransfuse', 'isDelayed', 'isDelayedDate', 'is_don_done',
                'last_don_date', 'final_comment'
            ]
            
            # Create dictionary with only fields that were updated in the request
            donneurUsers_update_dict = {}
            update_data = donneur_update.model_dump(exclude_unset=True, exclude_none=True)
            
            for field in shared_fields:
                if field in update_data:
                    donneurUsers_update_dict[field] = update_data[field]
            
            # Add username if it changed
            if username_changed:
                donneurUsers_update_dict['userName'] = new_username
            
            # Only update DonneurUsers if we have changes to make
            if donneurUsers_update_dict:
                donneurUsers_update = DonneurUsersUpdate(**donneurUsers_update_dict)
                
                update_result = dao_donneurUsers.update_donneurUsers(
                    id_donneurUsers=donneur_exist.id_donneurUser,
                    donneurUsers_update=donneurUsers_update
                )
                
                if not update_result:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="Error synchronizing changes with donor user record"
                    )
        
        # PART 4: Handle automatic prelevement creation if is_ok_prelevement is True
        if donneur_update.is_ok_prelevement == True:
            nbr_prelevements = dao_prelevement.count_prelevements_of_the_month()
            print("nbr_prelevements", nbr_prelevements)
            nbr_poches= nbr_prelevements + 1
            print("nbr_poches", nbr_poches)
            # Safety check for parameters
            if donneur_exist.parametres and len(donneur_exist.parametres) > 0:
                prelevement_create = PrelevementCreate(
                    id_donneur=id_donneur,
                    dateDePrelevement=datetime.now().date(),
                    heureDebut=datetime.now().time(),
                    heureFin=datetime.now().time(),
                    poidsDePoche=0,
                    volumePrevele=donneur_exist.parametres[0].quantite,
                    remarques="",
                    effetsIndesirables="",
                    id_parametre=donneur_exist.parametres[0].id
                )
                dao_prelevement.create_new_prelevement(id_user=user.id, prelevement=prelevement_create, nbr_poches=nbr_poches)
                # Explicitly flush the session to ensure the prelevement is in the database
                # but doesn't commit the transaction
                db.flush()
                dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                    action="validation du prelevement du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                    nom_utilisateur=user.nom+" "+user.prenom,
                    date_action=datetime.now(),
                    ressource="tdr",
                    status="success",
                    id_utilisateur=user.id
                ))
            else:
                print(f"Warning: Cannot create prelevement - no parameters found for donor {id_donneur}")
                dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                    action="tentative de validation du prelevement du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                    nom_utilisateur=user.nom+" "+user.prenom,
                    date_action=datetime.now(),
                    ressource="tdr",
                    status="error",
                    id_utilisateur=user.id
                ))
        
        if donneur_update.isDelayed == True:
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="renvoie du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="Donneur",
                status="success",
                id_utilisateur=user.id
            ))
        
        if donneur_update.isValideMedecin == True:
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="validation du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="Donneur",
                status="success",
                id_utilisateur=user.id
            ))
        
        # PART 5: Update DonneurUsers is_don_done to False if is_rejected is True
        if donneur_update.is_rejected == True:
            print("donneur_update.is_rejected", donneur_update.is_rejected)
            dao_donneurUsers.update_donneursUsers_is_not_don_done(id_donneurUsers=donneur_exist.id_donneurUser)
            dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
                action="rejet du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
                nom_utilisateur=user.nom+" "+user.prenom,
                date_action=datetime.now(),
                ressource="Donneur",
                status="success",
                id_utilisateur=user.id
            ))
        # Commit all changes at once at the end
        db.commit()
        
        # Return the updated donor record
        return dao_donneur.get_donneur_by_id(donneur_id=id_donneur)
    
    except Exception as e:
        # Rollback on any error
        db.rollback()
        print(f"Error during donor update: {str(e)}")
        # Créer le log d'erreur dans une nouvelle transaction
    try:
        dao_logs.create_new_log(
            action="tentative d'update du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="Donneur",
            status="error",
            id_utilisateur=user.id
        )
    except:
        pass  # Si le log échoue, on ne veut pas masquer l'erreur principale
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"An error occurred during the update process: {str(e)}"
    )
    



@DonneurRouter.delete("/{id_donneur}", description="delete donneur")
def delete_donneur(id_donneur:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_donneur = DaoDonneur(db=db)
    dao_logs = DaoLogs(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_donneur.delete_donneur(donneur=donneur_exist)
    dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
        action="suppression du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
        nom_utilisateur=user.nom+" "+user.prenom,
        date_action=datetime.now(),
        ressource="Donneur",
        status="success",
        id_utilisateur=user.id
    ))
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Donneur with id {id_donneur} successfully deleted")


@DonneurRouter.get("/{id_donneur}/parametres", description="Get all paramtres by donneur id ", response_model=List[ParametreResponseModel])
def get_parametres_donneur(id_donneur: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[ParametreResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_parametre = DaoParametre(db=db)

    return dao_parametre.get_parametre_by_donneur_id(id_donneur=id_donneur)


@DonneurRouter.post("/{id_donneur}/parametres", description="Create a new paramteres for donneur id",response_model=ParametreResponseModel)
def get_parametres_donneur(id_donneur: int, parametre_create: ParametreCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_parametre = DaoParametre(db=db)

    parametre = dao_parametre.create_new_parametre(id_donneur=id_donneur, parametre=parametre_create)

    return parametre

@DonneurRouter.put("/{id_donneur}/parametres/{id_parametre}", description="update parametre donneur", response_model=ParametreResponseModel)
def update_parametre_donneur(id_donneur: int, id_parametre: int, parametre_update: ParametreUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> ParametreResponseModel:
    dao_donneur = DaoDonneur(db=db)
    dao_logs = DaoLogs(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_parametre = DaoParametre(db=db)

    parametre_exist = dao_parametre.get_parametre_by_id(parametre_id=id_parametre)

    if not parametre_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Parameter with id: {id_parametre} don't exist in database")

    result =  dao_parametre.update_parametre(id_parametre=id_parametre, parametre_update=parametre_update)
    #si examen_tdr est different de null ou different de vide 
    if parametre_update.examen_tdr != None and parametre_update.examen_tdr != "":
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="ajout d'un examen tdr pour le donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="Tdr",
            status="success",
            id_utilisateur=user.id
        ))
    

    if not result:
        dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
            action="tentative d'update du parametre du donneur "+donneur_exist.nom+" "+donneur_exist.prenom,
            nom_utilisateur=user.nom+" "+user.prenom,
            date_action=datetime.now(),
            ressource="tdr",
            status="error",
            id_utilisateur=user.id
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update parametre donneur")
    

    return dao_parametre.get_parametre_by_id(parametre_id=id_parametre)
    

@DonneurRouter.get("/{id_donneur}/parametres/{id_parametre}", description="get parametre id by donneur id", response_model=ParametreResponseModel)
def get_parametres_donneur(id_donneur: int, id_parametre: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))->ParametreResponseModel:

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_parametre = DaoParametre(db=db)

    parametre_exist = dao_parametre.get_parametre_by_id(parametre_id=id_parametre)

    if not parametre_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Parametre with id: {id_parametre} don't exist in database" )
    

    return dao_parametre.get_parametre_by_id(parametre_id=id_parametre)


@DonneurRouter.get("/{id_donneur}/SMSs", description="get all sms by donneur by id ", response_model=List[SMSResponseModel])
def get_all_sms_by_donneur_id(id_donneur, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[SMSResponseModel]:

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")

    dao_sms = DaoSMS(db=db)
    SMSs = dao_sms.get_all_SMS_by_donneur_id(id_donneur=id_donneur)

    return SMSs

@DonneurRouter.post("/{id_donneur}/SMSs", description="send SMS by to donneur id", response_model=SMSResponseModel)
def send_SMS_to_donneur_id(id_donneur:int, SMS_create: SMSCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")
    
    dao_sms = DaoSMS(db=db)
    response = sendSMStoDonneur(donneur_exist.telephone, message=SMS_create.contenue)

    if response["responsecode"] == 1:
        sms = dao_sms.create_new_SMS(id_user=user.id, id_donneur=id_donneur, SMS_create=SMS_create)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=response["Errordescription"])

    return sms

@DonneurRouter.put("/{id_donneur}/SMSs/{id_sms}", description="update sms send to donneur", response_model=SMSResponseModel)
def update_SMS_send_to_Donneur(id_donneur:int, id_sms:int, SMS_update: SMSUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user))->SMSResponseModel:

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")
    
    dao_sms = DaoSMS(db=db)

    sms_exist = dao_sms.get_SMS_by_id(id_SMS=id_sms)

    if not sms_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SMS with id: {id_sms} don't exist in database")

    result  = dao_sms.update_SMS(id_SMS=id_sms, SMS_update=SMS_update)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during update SMS with id: {id_sms}")

    return dao_sms.get_SMS_by_id(id_SMS=id_sms)

@DonneurRouter.delete("/{id_donneur}/SMSs/{id_sms}", description="delete SMS", response_model=SMSResponseModel)
def delete_SMS_Donneur(id_donneur:int, id_sms:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> SMSResponseModel:

    dao_donneur = DaoDonneur(db=db)

    donneur_exist = dao_donneur.get_donneur_by_id(donneur_id=id_donneur)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Donneur with id: {id_donneur} don't exist in database")
    
    dao_sms = DaoSMS(db=db)

    sms_exist = dao_sms.get_SMS_by_id(id_SMS=id_sms)

    if not sms_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SMS with id: {id_sms} don't exist in database")  

    dao_sms.delete_SMS(SMS=sms_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"SMS with id: {id_sms} successfully deleted")