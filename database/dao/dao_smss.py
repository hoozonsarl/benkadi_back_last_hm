from sqlalchemy.orm import Session
from models.smss import Sms
from schemas.smss import SMSCreate, SMSUpdate
from datetime import datetime

class DaoSMS():
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    
    def get_all_SMS(self,):
        SMSs = self.db.query(Sms).all()
        return SMSs
    
    def get_SMS_by_id(self, id_SMS:int):
        SMS = self.db.query(Sms).filter(Sms.id == id_SMS).first()
        return SMS

    def get_all_SMS_by_user_id(self, id_user:int):
        SMSs = self.db.query(Sms).filter(Sms.id_user == id_user).all()
        return SMSs
    
    def get_all_SMS_by_donneur_id(self, id_donneur:int):
        SMSs = self.db.query(Sms).filter(Sms.id_donneur == id_donneur).all()
        return SMSs

    def create_new_SMS(self, id_donneur:int, id_user:int, SMS_create: SMSCreate):
        SMS = Sms(contenue = SMS_create.contenue, id_donneur=id_donneur, id_user=id_user, updatedAt=datetime.now())
        self.db.add(SMS)
        self.db.commit()
        self.db.refresh(SMS)
        return SMS
    
    def update_SMS(self, id_SMS:int, SMS_update: SMSUpdate):
        result = False
        try:

            SMS_update_dict = SMS_update.model_dump()
            self.db.query(Sms).filter(Sms.id == id_SMS).update(SMS_update_dict)
            self.db.commit()
            result = True
        except Exception as e:
            print("Error during the update SMS", e)
        return result
    
    def delete_SMS(self, SMS: Sms):
        self.db.delete(SMS)
        self.db.commit()
    
