from sqlalchemy.orm import Session
from models.groupe_utilisateur import GroupeUtisateurHasPermissions
from models.permissions import Permission
from models.groupe_utilisateur import GroupeUtilisateur
from schemas.groupe_utilisateur_has_permissions import GroupeUtisateurHasPermissionsCreate, GroupeUtisateurHasPermissionsupdate
from datetime import datetime

class DaoGroupeUtilisateurHas_permissions():
    db: Session


    def __init__(self, db: Session):
        self.db = db

    
    def get_all_groupe_utilisateur_has_permissions(self):
        groupe_utilisateur_has_permissions = self.db.query(GroupeUtisateurHasPermissions).all()
        return groupe_utilisateur_has_permissions

    def get_all_permissions_by_groupe_utilisateur(self, id_group_user):
        groupe_utilisateur_has_permisions_by_group_user = self.query(GroupeUtisateurHasPermissions).filter(GroupeUtisateurHasPermissions.group_utilisateur_id==id_group_user).all()
        return groupe_utilisateur_has_permisions_by_group_user
    
    def create_new_groupe_utilisateur_has_permissions(self, groupeUtilisateurCreate: GroupeUtisateurHasPermissionsCreate):
        
        groupe_user = self.db.query(GroupeUtilisateur).filter(GroupeUtilisateur.id==groupeUtilisateurCreate.idGroupeUtilisateur).first()
        permissions = [self.db.query(Permission).filter(Permission.id==i).first() for i in groupeUtilisateurCreate.idPermission]
        print(permissions)
        groupe_user.permissions = permissions
        self.db.commit()

        return True
    
    def delete_groupe_utilisateur_has_permisions(self, ):
        pass
    

