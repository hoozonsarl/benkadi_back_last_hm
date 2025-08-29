from routes.donneursUsers import DonneurUsersRouter
from routes.logs import LogsRouter
from routes.params_receveurs import ParamsReceveurRouter
from routes.reactifs import ReactifRouter
from routes.users import  UserRouter
from routes.permissions import PermissionRouter
from routes.receveurs import ReceveurRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.groupe_utilisateurs import GroupeUtilisateurRouter
from routes.groupe_utilisateur_has_permissions import GroupeUtisateurHasPermissionsRouter
from routes.donneurs import DonneurRouter
from routes.prelevements import PrevelementRouter
from routes.hospitals import HospitalRouter
from routes.fraction_types import FractionTypeRouter
from routes.fraction import FractionRouter
from routes.poche_de_sangs import PocheDeSangRouter
from routes.distributions import DistributionRouter
from routes.bon_de_sangs import bonDeSangRouter
from routes.dashbords import DashboardsRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI(description="Benkend For Benkadi Blood Application", contact={"email": "samanidarix@gmail.com", "tel": "691439424"},title="API BENKADI BLOOD")




origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Benkadi Blood API."}


app.include_router(UserRouter, tags=["USERS"], prefix="/users")
app.include_router(GroupeUtilisateurRouter, tags=["GROUPEUTILISATEUR"], prefix="/groupe-utilisateurs")
app.include_router(PermissionRouter, tags=["PERMISIONS"], prefix="/permissions")
app.include_router(GroupeUtisateurHasPermissionsRouter, tags=["GroupeUtilisateurHasPermisions"], prefix="/groupe-utilisateur-has-permisions"),
app.include_router(DonneurRouter, tags=["DONNEURS"], prefix="/donneurs")
app.include_router(PrevelementRouter, tags=["PRELEVEMENTS"], prefix="/prelevements")
app.include_router(ReactifRouter, tags=["REACTIFS"], prefix="/reactifs")
app.include_router(DonneurUsersRouter, tags=["DONNEURSUSERS"], prefix="/donneursUsers")
app.include_router(ParamsReceveurRouter, tags=["PARAMSRECEVEURS"], prefix="/params-receveurs")

app.include_router(PocheDeSangRouter, tags=["POCHESDESANGS"], prefix="/poche-de-sangs")

app.include_router(DistributionRouter, tags=["DISTRIBUTIONS"], prefix="/distributions")

app.include_router(DashboardsRouter, tags=["DASHBORDS"], prefix="/dashboards")
app.include_router(LogsRouter, tags=["LOGS"], prefix="/logs")

app.include_router(ReceveurRouter, tags=["RECEVEURS"], prefix="/receveurs")
app.include_router(bonDeSangRouter, tags=["BonDeSangs"], prefix="/bonDeSangs")
app.include_router(FractionTypeRouter, tags=["FractionType"], prefix="/fraction-types")
app.include_router(FractionRouter, tags=["FRACTIONS"], prefix="/fractions")
app.include_router(HospitalRouter, tags=["HOSPITALS"], prefix="/hospitals")
