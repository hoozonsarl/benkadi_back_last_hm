from datetime import datetime
from database.dao.dao_logs import DaoLogs
from fastapi import APIRouter, Depends, Body, status
from schemas.logs import LogsCreate
from schemas.users import UserCreate
from models.users import User
from sqlalchemy.orm import Session
from database.dao.dao_users import DaoUser
from database.dao.dao_groupe_utilisateur import DaoGroupeUtilisateur
from database.dao.dao_users import DaoUser
from sqlalchemy.orm import Session
from auth.deps import get_db
from schemas.users import UserCreate
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserResponseModel, Token
from typing import Union, List
from passlib.context import CryptContext
from auth.jwt_handler import sign_jwt
from auth.deps import get_db, get_current_user
from schemas.smss import SMSResponseModel
from database.dao.dao_smss import DaoSMS
from database.dao.dao_groupe_utilisateur import DaoGroupeUtilisateur

UserRouter = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@UserRouter.post("/login", )
def get_acces_token(db: Session = Depends(get_db), user_credentiel: OAuth2PasswordRequestForm = Depends())->dict:
    
    daoUser = DaoUser(db=db)
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    user_exist = daoUser.get_user_by_email(email=user_credentiel.username)
    if user_exist:
        try:
            print(user_exist.password, user_credentiel.password)
            password = hash_helper.verify(user_credentiel.password, user_exist.password)

        except Exception as e:
            print(e)
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        if password:

            permissions = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(user_exist.id_groupe_utilisateur).permissions

            return sign_jwt(email=user_credentiel.username, user= user_exist, permissions=permissions)
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email or password")
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Email or password")


@UserRouter.post("", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
def create_new_users(group_user_id:int, user_create: UserCreate, db: Session = Depends(get_db))-> UserResponseModel:

    daoUser = DaoUser(db=db)
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    dao_logs = DaoLogs(db=db)

    group_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=group_user_id)

    if not group_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Groupe User with id: {group_user_id} don't exit in database")

    user_exists = daoUser.get_user_by_email(email=user_create.email)
    print("USER : ", user_exists)
    if user_exists:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    
    user = daoUser.create_new_user(id_groupe_utilisateur=group_user_id, user=user_create)
    dao_logs.create_new_log(id_user=user.id, log=LogsCreate(
        action="creation d'un utilisateur",
        nom_utilisateur=user.nom+" "+user.prenom,
        date_action=datetime.now(),
        ressource="user",
        status="success",
        id_utilisateur=user.id
    ))
    return user




@UserRouter.get("/pagination", description="get all user by pagination", response_model=List[UserResponseModel])
def get_all_user_by_pagination(skip: int = 0, limit: int = 100,  db: Session = Depends(get_db), user: User = Depends(get_current_user))->List[UserResponseModel]:
    daoUser = DaoUser(db=db)
    users = daoUser.get_users_by_pagination(skip=skip, limit=limit)
    return users


@UserRouter.get("", description="get all user",)
def get_all_user(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[UserResponseModel]:
    dao_user = DaoUser(db=db)
    dao_groupe_utilisateur =  DaoGroupeUtilisateur(db=db)

    users = dao_user.get_users()
    
    return users

@UserRouter.delete("/{user_id}")
def delete_user(user_id: int, group_user_id:int,  db: Session = Depends(get_db), user = Depends(get_current_user)):
    daoUser = DaoUser(db=db)
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    group_user_exist = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=group_user_id)

    if not group_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group user don't exist in database")
    user_ = daoUser.get_user_by_id(user_id=user_id)
    print(f"user : {user_}")
    if not user_:
        raise HTTPException(authentifcqtionstatus_code=400, detail="User not found")
    
    daoUser.delete_user(user=user_)

    return HTTPException(status_code=status.HTTP_200_OK, detail=f"User with id {user_.id} successfully deleted")


@UserRouter.get("/{id_user}/SMSs", description="get all SMS send by user id", response_model=List[SMSResponseModel])
def get_all_SMS_send_by_user_id(id_user:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[SMSResponseModel]:

    daoUser = DaoUser(db=db)
    user_exist = daoUser.get_user_by_id(user_id=id_user)
    print(f"user : {user_exist}")
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with id: {id_user} not found in database")

    
    dao_sms = DaoSMS(db=db)

    SMSs = dao_sms.get_all_SMS_by_user_id(id_user=id_user)

    return SMSs