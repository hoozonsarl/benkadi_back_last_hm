from sqlalchemy.orm import Session
from schemas.groupe_utilisateurs import GroupeUtilisateurCreate, GroupeUtilisateurUpdate
from models.groupe_utilisateur import GroupeUtilisateur
from datetime import datetime






class DaoGroupeUtilisateur():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_groupes_utilisateurs(self):
        groupe_utilisateurs = self.db.query(GroupeUtilisateur).all()
        return groupe_utilisateurs
    
    def get_groupe_utilisateur_by_name(self, nom: str):
        groupe_utlisateur = self.db.query(GroupeUtilisateur).filter(GroupeUtilisateur.nom==nom).first()
        return groupe_utlisateur


    def get_groupe_utilisateur_by_id(self, group_utilisateur_id: int):
        groupe_utilisateur = self.db.query(GroupeUtilisateur).filter(GroupeUtilisateur.id==group_utilisateur_id).first()
        return groupe_utilisateur

    def update_group_user(self, id_group_user:int, group_user_update: GroupeUtilisateurUpdate ):
        result = False
        try:

            group_user_update_dict = group_user_update.model_dump()
            self.db.query(GroupeUtilisateur).filter(GroupeUtilisateur.id==id_group_user).update(group_user_update_dict)
            self.db.commit()
            result = True

        except Exception as e:
            print("Error durint update group user ", e)
        return result

    def create_new_groupe_utilisateur(self, groupe_utilisateur: GroupeUtilisateurCreate):
        groupe_utilisateur_db = GroupeUtilisateur(nom=groupe_utilisateur.nom, updatedAt=datetime.utcnow())
        self.db.add(groupe_utilisateur_db)
        self.db.commit()
        self.db.refresh(groupe_utilisateur_db)
        return groupe_utilisateur_db

    def get_groupe_utilisateurs_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(GroupeUtilisateur).offset(skip).limit(limit).all()


    def delete_groupe_utilisateur(self, groupe_utilisateur: GroupeUtilisateur):
        self.db.delete(groupe_utilisateur)
        self.db.commit()



    