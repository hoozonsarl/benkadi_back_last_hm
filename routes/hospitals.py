from fastapi import status, APIRouter, HTTPException, Depends
from auth.deps import get_current_user, get_db
from sqlalchemy.orm import Session
from models.users import User
from database.dao.dao_hospitals import DaoHospital
from schemas.hostipals import HospitalCreate, HospitalResponseModel, HospitalUpdate
from typing import List

HospitalRouter = APIRouter()


@HospitalRouter.get("", description="get all Hospitals", response_model=List[HospitalResponseModel])
def get_all_hospital(db: Session = Depends(get_db), user: User = Depends(get_current_user))->List[HospitalResponseModel]:
    
    dao_hospital = DaoHospital(db=db)

    hospitals = dao_hospital.get_hospitals()

    return hospitals

@HospitalRouter.post("", status_code=status.HTTP_201_CREATED, description="Create a new Hospital")
def create_new_hospitals(hospital_create: HospitalCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_hospital = DaoHospital(db=db)
    hospital_exist = dao_hospital.get_hospital_by_name(nom=hospital_create.nom)

    if hospital_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with name: {hospital_create.nom} exist in database")
    
    hosiptal = dao_hospital.create_new_hospital(id_user=user.id, hospital=hospital_create)

    return hosiptal

@HospitalRouter.put("/{id_hospital}", description="update Hospital", response_model=HospitalResponseModel)
def update_hosipal(id_hospital:int, hospital_update: HospitalUpdate,db: Session = Depends(get_db), user: User = Depends(get_current_user))-> HospitalResponseModel:
    
    dao_hospital = DaoHospital(db=db)
    hospital_exist = dao_hospital.get_hospital_by_id(hospital_id=id_hospital)

    if not hospital_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with id: {id_hospital} don't exist in database")
    
    result = dao_hospital.update_hospital(id_hospital=id_hospital, hospital_update=hospital_update)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error during update hospital")
    return dao_hospital.get_hospital_by_id(hospital_id=id_hospital)

@HospitalRouter.delete("/{id_hospital}", description="Delete Hospital", status_code=status.HTTP_200_OK)
def delete_hospital(id_hospital:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    dao_hospital = DaoHospital(db=db)

    hospital_exist = dao_hospital.get_hospital_by_id(hospital_id=id_hospital)

    if not hospital_exist:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Hospital with id: {id_hospital} don't exist in database")

    dao_hospital.delete_hospital(hospital_exist)
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Hospital with id {id_hospital} successfully deleted")