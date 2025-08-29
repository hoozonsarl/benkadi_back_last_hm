from fastapi import APIRouter, status, HTTPException, Depends
from auth.deps import get_db, get_current_user
from database.dao.dao_dashboards import DaoDashboards
from sqlalchemy.orm import Session
from models.users import User



DashboardsRouter = APIRouter()


@DashboardsRouter.get('', description="get all dashboards")
def get_all_dashbord(db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_dashbords = DaoDashboards(db=db)

    return dao_dashbords.full_dashbord()
