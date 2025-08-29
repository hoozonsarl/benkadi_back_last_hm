from fastapi import APIRouter, Depends, Body, status
from schemas.users import UserCreate, UserUpdate
from models.users import User
from sqlalchemy.orm import Session
from database.dao.dao_users import DaoUser
from database.dao.dao_groupe_utilisateur import DaoGroupeUtilisateur
from sqlalchemy.orm import Session
from auth.deps import get_db
from schemas.users import UserCreate
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserResponseModel, Token
from typing import Union, List
from schemas.users import UserResponseModel
from schemas.permissions import PermissionResponseModel
from schemas.groupe_utilisateurs import GroupeUtilisateurCreate, GroupeUtilisateurResponseModel, GroupeUtilisateurUpdate
from auth.deps import get_db, get_current_user

GroupeUtilisateurRouter = APIRouter()



@GroupeUtilisateurRouter.post("", response_description="User successfully created a group user.", status_code=status.HTTP_201_CREATED)
def create_new_groupe_utilisateur(groupe_utilisateur_create: GroupeUtilisateurCreate, db: Session = Depends(get_db)):
    
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    groupe_utilisateur_exists = dao_groupe_utilisateur.get_groupe_utilisateur_by_name(nom=groupe_utilisateur_create.nom)

    if groupe_utilisateur_exists:
        raise HTTPException(detail = "Groupe Utilisateur already exist", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    groupe_utilisateur_create = dao_groupe_utilisateur.create_new_groupe_utilisateur(groupe_utilisateur=groupe_utilisateur_create)

    return groupe_utilisateur_create


@GroupeUtilisateurRouter.get("", description="get all group User", response_model=List[GroupeUtilisateurResponseModel])
def get_all_create_groupe_user(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[GroupeUtilisateurResponseModel]:
    
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    # get all group user

    groupe_utilisateurs = dao_groupe_utilisateur.get_groupes_utilisateurs()

    return groupe_utilisateurs


@GroupeUtilisateurRouter.get("/{id_group_user}", description="get groupe user information", response_model= GroupeUtilisateurResponseModel)
def get_groupe_utilisateur_by_id(id_group_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    groupe_utilisateur = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)

    if not groupe_utilisateur:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Groupe utilisateur with id: {id_group_user} don't exist")
    
    return groupe_utilisateur

@GroupeUtilisateurRouter.get("/{id_group_user}/permisions", description="Permisions by Groupe User", response_model=List[PermissionResponseModel])
def get_all_permision_by_group_user(id_group_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[PermissionResponseModel]:

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    group_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)
    
    if not group_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group User don't exist")
    return group_user_exist.permissions


@GroupeUtilisateurRouter.put("/{id_group_user}", description="update groupe utilisateur", response_model=GroupeUtilisateurResponseModel)
def update_group_user(id_group_user: int, group_user_update: GroupeUtilisateurUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db))-> GroupeUtilisateurResponseModel:

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    groupe_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)
    if not groupe_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Group User with id :{ id_group_user} don't exist")
    
    # if id_group_user!=user.id_groupe_utilisateur:
    #     raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="you cannot modify this user group")
    
    result = dao_groupe_utilisateur.update_group_user(id_group_user=id_group_user, group_user_update=group_user_update)

    if not  result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Groupe Utilisateur")
    
    return dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)


@GroupeUtilisateurRouter.delete("/{id_group_user}", description="delete Groupe Utilisateur")
def delete_receveur(id_group_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    groupe_utisateur_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)

    if not groupe_utisateur_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Groupe Utilisateur with id: {id_group_user} don't exist in database")

    dao_groupe_utilisateur.delete_groupe_utilisateur(groupe_utilisateur=groupe_utisateur_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Groupe utilisateur with id {groupe_utisateur_exist} successfully deleted")

@GroupeUtilisateurRouter.post("/{id_group_user}/users", response_model=UserResponseModel)
def create_new_users(id_group_user: int, user_create: UserCreate, db= Depends(get_db)):

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    groupe_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(id_group_user)

    if not groupe_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group user not exist")
    
    if groupe_user_exist.id != id_group_user:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Please Provider a correct groupe User")
    
    dao_user = DaoUser(db=db)


    user_exist = dao_user.get_user_by_email(email=user_create.email)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    
    user = dao_user.create_new_user(id_groupe_utilisateur=id_group_user, user=user_create)

    return user

@GroupeUtilisateurRouter.get("/{id_group_user}/users", response_model=List[UserResponseModel])
def get_all_user_by_groupe_user(id_group_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[UserResponseModel]:

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    groupe_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(id_group_user)

    if not groupe_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group user not exist")
    
    if groupe_user_exist.id != id_group_user:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Please Provider a correct groupe User")
    dao_user = DaoUser(db=db)
    users = dao_user.get_user_by_groupe(id_group_user=groupe_user_exist.id)
    return users


@GroupeUtilisateurRouter.get("/{id_group_user}/users/{id_user}", response_model=UserResponseModel)
def get_all_users_by_groupe_user(id_group_user:int, id_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> UserResponseModel:

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    groupe_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(id_group_user)

    if not groupe_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group user not exist")
    
    if groupe_user_exist.id != id_group_user:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, details="Please Provider a correct groupe User")
    
    dao_user = DaoUser(db=db)
    user_exist = dao_user.get_user_by_id(user_id=id_user)
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with {id_user} don't exist in database")
    
    return user_exist

@GroupeUtilisateurRouter.put("/{id_group_user}/users/{id_user}", response_model=UserResponseModel, description="update user")
def update_user_to_groupe_user_user_id(id_group_user: int, id_user: int , user_update: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)

    group_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=id_group_user)

    if not group_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Groupe User don't exist in Database")
    dao_user = DaoUser(db=db)
    
    user_exist = dao_user.get_user_by_id(user_id=id_user)

    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User don't exist in database")
    
    result =  dao_user.update_user(id_user=user_exist.id, user_update=user_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Error during the update User")

    return dao_user.get_user_by_id(user_id=user_exist.id)




        
        
    

