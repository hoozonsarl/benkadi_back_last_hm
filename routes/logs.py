from datetime import datetime
from fastapi import status, APIRouter, HTTPException, Depends
from auth.deps import get_current_user, get_db
from sqlalchemy.orm import Session
from models.users import User
from database.dao.dao_logs import DaoLogs
from schemas.logs import LogsCreate, LogsResponseModel, LogsUpdate
from typing import List

LogsRouter = APIRouter()


@LogsRouter.get("", description="get all Logs", response_model=List[LogsResponseModel])
def get_all_logs(db: Session = Depends(get_db), user: User = Depends(get_current_user))->List[LogsResponseModel]:
    
    dao_logs = DaoLogs(db=db)

    logs = dao_logs.get_logs()

    return logs

@LogsRouter.get("/pagination", description="get all Logs with pagination", response_model=List[LogsResponseModel])
def get_all_logs_with_pagination(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: User = Depends(get_current_user))->List[LogsResponseModel]:

    dao_logs = DaoLogs(db=db)

    logs = dao_logs.get_logs_with_pagination(skip=skip, limit=limit)
    return logs 

@LogsRouter.get("/{id_log}", description="get Log by id", response_model=LogsResponseModel)
def get_log_by_id(id_log:int, db: Session = Depends(get_db), user: User = Depends(get_current_user))->LogsResponseModel:

    dao_logs = DaoLogs(db=db)

    log = dao_logs.get_log_by_id(id=id_log) 

    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Log with id: {id_log} don't exist in database")

    return log


#get logs by created_at
@LogsRouter.get("/created_at/{created_at}", description="get Logs by created_at", response_model=List[LogsResponseModel])
def get_logs_by_created_at(created_at:datetime, db: Session = Depends(get_db), user: User = Depends(get_current_user))->List[LogsResponseModel]:

    dao_logs = DaoLogs(db=db)

    logs = dao_logs.get_logs_by_created_at(created_at=created_at)

    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Logs with created_at: {created_at} don't exist in database")

    return logs

@LogsRouter.post("", status_code=status.HTTP_201_CREATED, description="Create a new Log")
def create_new_logs(log_create: LogsCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_logs = DaoLogs(db=db)
    log_exist = dao_logs.get_log_by_id(id=log_create.id)

    if log_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Log with id: {log_create.id} exist in database")
    
    log = dao_logs.create_new_log(id_user=user.id, log=log_create)

    return log

@LogsRouter.put("/{id_log}", description="update Log", response_model=LogsResponseModel)
def update_log(id_log:int, log_update: LogsUpdate,db: Session = Depends(get_db), user: User = Depends(get_current_user))-> LogsResponseModel:
    
    dao_logs = DaoLogs(db=db)   
    log_exist = dao_logs.get_log_by_id(id=id_log)

    if not log_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Log with id: {id_log} don't exist in database")
    
    result = dao_logs.update_log(id_log=id_log, log_update=log_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during update log")
    return dao_logs.get_log_by_id(id=id_log)

@LogsRouter.delete("/{id_log}", description="Delete Log", status_code=status.HTTP_200_OK)
def delete_log(id_log:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_logs = DaoLogs(db=db)

    log_exist = dao_logs.get_log_by_id(id=id_log)

    if not log_exist:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Log with id: {id_log} don't exist in database")

    dao_logs.delete_log(log_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Log with id {id_log} successfully deleted")