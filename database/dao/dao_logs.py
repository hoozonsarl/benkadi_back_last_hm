from sqlalchemy.orm import Session
from schemas.logs import LogsCreate, LogsResponseModel, LogsUpdate
from models.logs import Logs
from datetime import datetime

class DaoLogs():

    db : Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_logs(self):
        logs = self.db.query(Logs).all()
        return logs
    
    #get all logs with pagination order by createdAt desc
    def get_logs_with_pagination(self, skip: int = 0, limit: int = 10):
        logs = self.db.query(Logs).order_by(Logs.createdAt.desc()).offset(skip).limit(limit).all()
        return logs
    
    def get_log_by_id(self, id: int):
        log = self.db.query(Logs).filter(Logs.id==id).first()
        return log
    
    def get_logs_by_created_at(self, created_at: datetime):
        logs = self.db.query(Logs).filter(Logs.created_at==created_at).all()
        return logs

    def update_log(self, id_log:int,  log_update: LogsUpdate ):
        result = False
        try:

            log_update_dict = log_update.model_dump()
            self.db.query(Logs).filter(Logs.id==id_log).update(log_update_dict)
            self.db.commit()
            result = True

        except Exception as e:
            print("Error durint update log ", e)
        return result

    def create_new_log(self, id_user:int, log: LogsCreate):
        log_db = Logs(action=log.action, 
                      nom_utilisateur=log.nom_utilisateur, 
                      date_action=log.date_action, 
                      ressource=log.ressource, 
                      status=log.status, 
                      id_utilisateur=id_user,
                      createdAt=datetime.now(),
                      updatedAt=datetime.now())
        self.db.add(log_db)
        self.db.commit()
        self.db.refresh(log_db)
        return log_db
    
    def create_new_log_whithout_commit(self, id_user:int, log: LogsCreate):
        log_db = Logs(action=log.action, 
                      nom_utilisateur=log.nom_utilisateur, 
                      date_action=log.date_action, 
                      ressource=log.ressource, 
                      status=log.status, 
                      id_utilisateur=id_user,
                      createdAt=datetime.now(),
                      updatedAt=datetime.now())
        self.db.add(log_db)
        #self.db.commit()
        self.db.refresh(log_db)
        return log_db


    def delete_log(self, log: Logs):
        self.db.delete(log)
        self.db.commit()