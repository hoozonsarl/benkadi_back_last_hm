from sqlalchemy.orm import Session
from models.users import User
from pydantic import EmailStr
from passlib.context import CryptContext
from schemas.users import UserCreate, UserUpdate
from models.users import User
from datetime import datetime



hash_helper = CryptContext(schemes=["bcrypt"])


class DaoUser():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_users(self):
        users = self.db.query(User).all()
        return users
    
    def get_users_by_pagination(self, skip:int, limit:int):
        users = self.db.query(User).skip(skip).limit(limit).all()
        return users


    def get_user_by_email(self, email: str):
        user = self.db.query(User).filter(User.email==email).first()
        return user

    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id==user_id).first()
        return user
    
    def get_user_by_groupe(self, id_group_user:int):
        users = self.db.query(User).filter_by(id_groupe_utilisateur=id_group_user).all()
        return users
    

    def create_new_user(self, id_groupe_utilisateur:int, user: UserCreate):
        user_db = User(email=user.email, password = hash_helper.encrypt(user.password), gender= user.gender, dateNaissance= user.dateNaissance, intituleDuPoste= user.intituleDuPoste, telephone = user.telephone, nom= user.nom, prenom=user.prenom, nationality = user.nationality, id_groupe_utilisateur = id_groupe_utilisateur, updatedAt=datetime.now())
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        return user_db

    def get_users_by_pagination(self, skip: int = 0, limit: int = 100):
        
        return self.db.query(User).offset(skip).limit(limit).all()


    def update_user(self, id_user: int, user_update: UserUpdate):
        result = True
        try:
            user_update_dict = user_update.model_dump()
            user_update_dict.update({"password": hash_helper.encrypt(user_update.password)})
            print(user_update_dict)
            self.db.query(User).filter(User.id==id_user).update(user_update_dict)
            self.db.commit()
        except Exception as e:
            print("error in update user", e)
            result = False
        return result
    def delete_user(self, user: User):

        self.db.delete(user)
        self.db.commit()



    