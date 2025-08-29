from datetime import datetime
from database.dao.dao_donneursUsers import DaoDonneurUsers
from database.utils import generate_username
from fastapi import APIRouter, HTTPException, status, Depends
from auth.deps import get_db, get_current_user
from schemas.donneurs import DonneurCreate, DonneurUpdate, DonneurResponseModel
from schemas.donneursUsers import DonneurUsersCreate, DonneurUsersResponseModel, DonneurUsersUpdate, DonneurUsersWithDonneurResponseModel, DonneurUsersWithoutDonneurResponseModel
from schemas.parametres import ParametreCreate, ParametreUpdate, ParametreResponseModel
from schemas.smss import SMSCreate, SMSUpdate, SMSResponseModel
from sqlalchemy.orm import Session
from database.dao.dao_donneurs import DaoDonneur
from database.dao.dao_parametres import DaoParametre
from models.users import User
from database.dao.dao_smss import DaoSMS
from typing import List, Optional
from tasks import sendSMStoDonneur

DonneurUsersRouter = APIRouter()




@DonneurUsersRouter.get("/all", description="get list donneurUsers all", response_model=List[DonneurUsersResponseModel])
def get_list_donneurUsers_all( db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurUsersResponseModel]:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneursUsers = dao_donneurUsers.get_all_donneursUsers()

    return donneursUsers


@DonneurUsersRouter.get("/storage", description="get list donneurUsers storage", response_model=List[DonneurUsersWithoutDonneurResponseModel])
def get_list_donneurUsers_storage( skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurUsersWithoutDonneurResponseModel]:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneursUsers = dao_donneurUsers.get_all_donneursUsers_storage(skip=skip, limit=limit)

    return donneursUsers


#get donneurUsers by userName
@DonneurUsersRouter.get("/by-userName/{userName}", description="get donneurUsers by userName", response_model=DonneurUsersResponseModel)
def get_donneurUsers_by_userName(userName: str, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DonneurUsersResponseModel:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneurUsers = dao_donneurUsers.get_donneurUsers_by_userName(userName=userName)

    return donneurUsers



#get donneurUsers by id
@DonneurUsersRouter.get("/by-id/{id_donneurUsers}", description="get donneurUsers by id", response_model=DonneurUsersWithDonneurResponseModel)
def get_donneurUsers_by_id(id_donneurUsers: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DonneurUsersWithDonneurResponseModel:

    print("id_donneurUsers", id_donneurUsers)

    dao_donneurUsers = DaoDonneurUsers(db=db)

    print("id_donneurUsers", id_donneurUsers)

    donneurUsers = dao_donneurUsers.get_donneurUsers_by_id(donneurUsers_id=id_donneurUsers)

    print("donneurUsers", donneurUsers)
    if not donneurUsers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DonneurUsers with id {id_donneurUsers} not found"
        )


    # donneurUsers_dict={
    #     "id": donneurUsers.id,
    #     "userName": donneurUsers.userName,
    #     "nom": donneurUsers.nom,
    #     "prenom": donneurUsers.prenom,
    #     "dateDeNaissance": donneurUsers.dateDeNaissance,
    #     "lieuDeNaissance": donneurUsers.lieuDeNaissance,
    #     "numeroCNI": donneurUsers.numeroCNI,
    #     "dateDelivranceIdCard": donneurUsers.dateDelivranceIdCard,
    #     "villeResidence": donneurUsers.villeResidence,
    #     "niveauEtude": donneurUsers.niveauEtude,
    #     "passport": donneurUsers.passport,
    #     "permisConduire": donneurUsers.permisConduire,
    #     "telephone": donneurUsers.telephone,
    #     "email": donneurUsers.email,
    #     "sexe": donneurUsers.sexe,
    #     "profession": donneurUsers.profession,
    #     "statusMatrimonial": donneurUsers.statusMatrimonial,
    #     "paysOrigine": donneurUsers.paysOrigine,
    #     "religion": donneurUsers.religion,
    #     "adresse": donneurUsers.adresse,
    #     "groupeSanguin": donneurUsers.groupeSanguin,
    #     "dateDeProchainDon": donneurUsers.dateDeProchainDon,
    #     "dateDernierDon": donneurUsers.dateDernierDon,
    #     "datePossibleDon": donneurUsers.datePossibleDon,
    #     "nombreDeDons": donneurUsers.nombreDeDons,
    #     "accidentDon": donneurUsers.accidentDon,
    #     "dejaTransfuse": donneurUsers.dejaTransfuse,
    #     "createdAt": donneurUsers.createdAt,
    #     "updatedAt": donneurUsers.updatedAt
    # }


    return donneurUsers

#get all donneursUsers by  userName and dateDeNaissance
@DonneurUsersRouter.get("/user/{userName}/{dateDeNaissance}", description="get all donneursUsers by  userName and dateDeNaissance", response_model=List[DonneurUsersResponseModel])
def get_all_donneursUsers_by_userName_and_dateDeNaissance(userName: str, dateDeNaissance: datetime, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurUsersResponseModel]:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneursUsers = dao_donneurUsers.get_all_donneursUsers_by_userName_and_dateDeNaissance(userName=userName, dateDeNaissance=dateDeNaissance)

    return donneursUsers


 #check user 
@DonneurUsersRouter.get("/check-user/{nom}/{prenom}/{dateDeNaissance}", description="check user", response_model= List[DonneurUsersResponseModel])
def check_user(nom: str, prenom: str, dateDeNaissance: datetime, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurUsersResponseModel]:

    userName = generate_username(nom, prenom)

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneurUsers = dao_donneurUsers.get_all_donneursUsers_by_userName_and_dateDeNaissance(userName=userName, dateDeNaissance=dateDeNaissance)

    print("donneurUsers", donneurUsers)

    return donneurUsers


#verify user
@DonneurUsersRouter.get("/verify-user/{id_donneurUsers}", description="verify user", response_model=DonneurUsersWithDonneurResponseModel)
def verify_user(id_donneurUsers: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DonneurUsersWithDonneurResponseModel:

    print("id_donneurUsers", id_donneurUsers)

    dao_donneurUsers = DaoDonneurUsers(db=db)


    print("id_donneurUsers", id_donneurUsers)

    donneurUsers = dao_donneurUsers.get_donneurUsers_by_id(donneurUsers_id=id_donneurUsers)


    print("donneurUsers", donneurUsers)

    if not donneurUsers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DonneurUsers don't exist in database")

    # Check if donneurUsers is delayed
    if donneurUsers and donneurUsers.isDelayed == True:
        if donneurUsers.isDelayedDate > datetime.now().date():
            print("donneurUsers.isDelayedDate", donneurUsers.isDelayedDate)
            print("datetime.now()", datetime.now().date())
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail="Vous ne pouvez pas faire un don avant la date de don qui est le " + str(donneurUsers.isDelayedDate))
           
    # Check if donneurUsers is not delayed
    if donneurUsers and donneurUsers.isDelayed == False:
        if donneurUsers.dateDeProchainDon > datetime.now().date():
            print("donneurUsers.dateDeProchainDon", donneurUsers.dateDeProchainDon)
            print("datetime.now()", datetime.now().date())
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail="Vous ne pouvez pas faire un don avant la date du prochain don qui est le " + str(donneurUsers.dateDeProchainDon))
        
    

    return donneurUsers



@DonneurUsersRouter.get("/pagination", description="get list donneurUsers by pagination", response_model=List[DonneurUsersResponseModel])
def get_list_donneurUsers_by_pagination(isDonneurUsers: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurUsersResponseModel]:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneursUsers_by_pagination = dao_donneurUsers.get_donneursUsers_by_pagination(skip=skip, limit=limit)

    return donneursUsers_by_pagination



@DonneurUsersRouter.post("", description="Create New DonneurUsers", response_model=DonneurUsersResponseModel)
def create_new_donneurUsers(donneur_create: DonneurUsersCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> DonneurUsersResponseModel:

    dao_donneurUsers = DaoDonneurUsers(db=db)

    userName = generate_username(donneur_create.nom, donneur_create.prenom)
    # donneur_exist = dao_donneur.get_donneur_by_numero_cni(numeroCNI=donneur_create.numeroCNI)
    donneurUsers_exist = dao_donneurUsers.get_donneurUsers_by_userName(userName=userName)

    if donneurUsers_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DonneurUsers already exist in database")
    
    donneurUsers = dao_donneurUsers.create_new_donneurUsers(id_user=user.id, donneurUsers=donneur_create)

    return donneurUsers

@DonneurUsersRouter.put("/{id_donneurUsers}", description="Update DonneurUsers", response_model=DonneurUsersResponseModel)
def update_donneur(id_donneurUsers: int, donneur_update: DonneurUsersUpdate, db: Session = Depends(get_db), user: User =  Depends(get_current_user)):

    dao_donneurUsers = DaoDonneurUsers(db=db)
    donneur_exist = dao_donneurUsers.get_donneurUsers_by_id(donneur_id=id_donneurUsers);

    if  not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DonneurUsers don't exist in database")

    result = dao_donneurUsers.update_donneurUsers(id_donneurUsers=id_donneurUsers   , donneurUsers_update=donneur_update)

    if not result:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Donneur")
    
    return dao_donneurUsers.get_donneurUsers_by_id(donneur_id=id_donneurUsers)


@DonneurUsersRouter.delete("/{id_donneurUsers}", description="delete donneurUsers")
def delete_donneurUsers(id_donneurUsers:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_donneurUsers = DaoDonneurUsers(db=db)

    donneur_exist = dao_donneurUsers.get_donneurUsers_by_id(donneur_id=id_donneurUsers)

    if not donneur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"DonneurUsers with id: {id_donneurUsers} don't exist in database")

    dao_donneurUsers.delete_donneurUsers(donneurUsers=donneur_exist)

    return HTTPException(status_code=status.HTTP_200_OK, detail=f"DonneurUsers with id {id_donneurUsers} successfully deleted")



# @DonneurUsersRouter.get("/{id_donneurUsers}/donneurs", description="Get all donneurs by donneurUsers id ", response_model=List[DonneurResponseModel])
# def get_DonneurUsers_donneurs(id_donneurUsers: int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[DonneurResponseModel]:

#     dao_donneurUsers = DaoDonneurUsers(db=db)
#     dao_donneur = DaoDonneur(db=db)

#     donneurUsers = dao_donneurUsers.get_donneurUsers_by_id(donneurUsers_id=id_donneurUsers)

#     if not donneurUsers:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"DonneurUsers with id: {id_donneurUsers} don't exist in database")

#     donneurs = dao_donneur.get_donneur_by_donneurUsers_id(id_donneurUsers=id_donneurUsers)

#     return dao_donneurUsers.get_donneur_by_donneurUsers_id(id_donneurUsers=id_donneurUsers)

