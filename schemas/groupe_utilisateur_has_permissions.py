from pydantic import BaseModel
from typing import List


class GroupeUtisateurHasPermissionsCreate(BaseModel):
    idGroupeUtilisateur: int
    idPermission: List[int]

class GroupeUtisateurHasPermissionsupdate(GroupeUtisateurHasPermissionsCreate):
    pass

class GroupeUtisateurHasPermissionsResponseModel(BaseModel):
    group_utilisateur_id: int
    permission_id: int