from sqlalchemy.orm import Session
from pydantic import EmailStr
from schemas.permissions import PermissionsCreate
from models.permissions import Permission
from datetime import datetime
from schemas.permissions import PermissionsUpdate




class DaoPermissions():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_permissions(self):
        permissions = self.db.query(Permission).all()
        return permissions


    def get_permission_by_id(self, permission_id: int):
        permission = self.db.query(Permission).filter(Permission.id==permission_id).first()
        return permission
    
    def get_permision_by_email(self, receveur_email: EmailStr):
        receveur = self.db.query(Permission).filter(Permission.email==receveur_email)
        return receveur

    def get_permision_by_telephone(self, receveur_telephone: EmailStr):
        receveur = self.db.query(Permission).filter(Permission.telephone==receveur_telephone)
        return receveur
    
    def create_new_permission(self, permissions: PermissionsCreate):
        permission_db = Permission(action= permissions.action, subject=permissions.subject, updatedAt=datetime.now())
        self.db.add(permission_db)
        self.db.commit()
        self.db.refresh(permission_db)
        return permission_db


    def get_permissions_by_pagination(self, skip: int = 0, limit: int = 100):
        return self.db.query(Permission).offset(skip).limit(limit).all()

    def update_permission(self, id_permission: int, permision_update: PermissionsUpdate):
        result = True
        try:
            permission_update_dict = permision_update.model_dump()
            print(permission_update_dict)
            self.db.query(Permission).filter(Permission.id==id_permission).update(permission_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update Permission", e)
            result = False
        return result
    
        return 111
    def delete_permision(self, permission: Permission):
        self.db.delete(permission)
        self.db.commit()



    