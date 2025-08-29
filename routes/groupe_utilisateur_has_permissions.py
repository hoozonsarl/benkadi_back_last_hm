from fastapi import APIRouter, Depends, Body, status, HTTPException
from database.dao.dao_groupe_utilisateur import DaoGroupeUtilisateur
from database.dao.dao_permissions import DaoPermissions
from database.dao.dao_groupe_utilisateur_has_permissions import DaoGroupeUtilisateurHas_permissions
from auth.deps import get_db, get_current_user
from sqlalchemy.orm import Session
from schemas.groupe_utilisateur_has_permissions import GroupeUtisateurHasPermissionsResponseModel, GroupeUtisateurHasPermissionsCreate, GroupeUtisateurHasPermissionsupdate
from typing import List
from models.users import User

GroupeUtisateurHasPermissionsRouter = APIRouter()


@GroupeUtisateurHasPermissionsRouter.get("")
def get_all_groupe_utilisateur_has_permisions(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[GroupeUtisateurHasPermissionsResponseModel]:

    dao_groupe_utilisateur_has_permisions =  DaoGroupeUtilisateurHas_permissions(db=db)

    groupe_utilisateur_has_permisions = dao_groupe_utilisateur_has_permisions.get_all_groupe_utilisateur_has_permissions()

    return groupe_utilisateur_has_permisions


@GroupeUtisateurHasPermissionsRouter.post("", description="Create a Groupe Utilisateur has permissions model", status_code=status.HTTP_201_CREATED)
def add_groupe_utilisateur_has_permisions(groupe_utilisateur_has_permisions_create: GroupeUtisateurHasPermissionsCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_groupe_utilisateur_has_permisions =  DaoGroupeUtilisateurHas_permissions(db=db)
    dao_permision = DaoPermissions(db=db)
    dao_groupe_utilisateur = DaoGroupeUtilisateur(db=db)
    print("IDs : ", groupe_utilisateur_has_permisions_create.idPermission)
    groupe_utilisateur = dao_groupe_utilisateur.get_groupe_utilisateur_by_id(group_utilisateur_id=groupe_utilisateur_has_permisions_create.idGroupeUtilisateur)

    if not groupe_utilisateur:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group User don't Exist")
    permisions = [dao_permision.get_permission_by_id(permission_id=i) for i in groupe_utilisateur_has_permisions_create.idPermission]
    if None in permisions :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission don't Exist")
    
    groupe_utilisateur_has_permission = dao_groupe_utilisateur_has_permisions.create_new_groupe_utilisateur_has_permissions(groupeUtilisateurCreate=groupe_utilisateur_has_permisions_create)
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Permissions successfully attribute to Group User") if groupe_utilisateur_has_permission else HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during attribute permission to group User")




