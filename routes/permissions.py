from fastapi import APIRouter, Depends, Body, status
from schemas.users import UserCreate
from models.users import User
from sqlalchemy.orm import Session
from database.dao.dao_users import DaoUser
from database.dao.dao_groupe_utilisateur import DaoGroupeUtilisateur
from sqlalchemy.orm import Session
from auth.deps import get_db
from schemas.users import UserCreate
from fastapi.exceptions import HTTPException
from typing import List
from schemas.permissions import PermissionsCreate, PermissionsUpdate, PermissionResponseModel
from database.dao.dao_permissions import DaoPermissions
from auth.deps import get_db, get_current_user

PermissionRouter = APIRouter()




@PermissionRouter.get("", description="get all permisions")
def get_all_permissions(db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PermissionResponseModel]:
    
    dao_permision = DaoPermissions(db=db)

    permissions = dao_permision.get_permissions()

    return permissions

@PermissionRouter.get("/pagination", description="get all permisions by pagination")
def get_all_permissions_by_pagination(skip: int=0, limit: int=100, db: Session = Depends(get_db), user: User = Depends(get_current_user))-> List[PermissionResponseModel]:
    
    dao_permision = DaoPermissions(db=db)

    permissions = dao_permision.get_permissions_by_pagination(skip=skip, limit=limit)

    return permissions



@PermissionRouter.post("", response_description="Permission successfully created", status_code=status.HTTP_201_CREATED)
def create_new_permission(permission_create: PermissionsCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    dao_permission = DaoPermissions(db=db)
    
    permission_create  = dao_permission.create_new_permission(permissions=permission_create);

    return permission_create





@PermissionRouter.put("/{id_permission}", response_model=PermissionResponseModel, description="update permision")
def update_permision(id_permission: int, permision_update: PermissionsUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_permision = DaoPermissions(db=db)

    permission_exist = dao_permision.get_permission_by_id(permission_id=id_permission)

    if not permission_exist:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permision you want to update don't exist")

    result = dao_permision.update_permission(id_permission=permission_exist.id, permision_update=permision_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error during the update Permission")

    return dao_permision.get_permission_by_id(permission_id=id_permission)
    

@PermissionRouter.delete("/{id_permission}", status_code=status.HTTP_204_NO_CONTENT, description="delete permision")
def delete_permission(id_permission:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
     
    dao_permission = DaoPermissions(db=db)
    

    permission = dao_permission.get_permission_by_id(permission_id=id_permission)


    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not  found")
    
    dao_permission.delete_permision(permission=permission)

    return HTTPException(status_code=status.HTTP_200_OK, detail=f"permision with id {permission.id} successfully deleted")


        
        
    

