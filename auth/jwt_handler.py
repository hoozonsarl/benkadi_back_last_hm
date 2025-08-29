import time
from typing import Dict
from jwt import encode, decode
from models.users import User
from config.config import Settings
from fastapi.encoders import jsonable_encoder
from models.users import User
from models.permissions import Permission
from typing import Any

def token_response(token: str, user: User, permissions: Permission):
    return {"access_token": token, "token_type": "Bearer", "user": jsonable_encoder(user), "permissions": jsonable_encoder(permissions)}


secret_key = Settings().secret_key


def sign_jwt(email: str, user: User, permissions: Permission) -> Dict[str, Any]:
    # Set the expiry time.
    payload = {"email": email, "expires": time.time() + 86400}
    return token_response(encode(payload, secret_key, algorithm="HS256"), user=user, permissions=permissions)


def decode_jwt(token: str) -> dict:
    decoded_token = decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}