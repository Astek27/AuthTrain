import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "admin"


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=401, headers={'WWW-Authenticate': "Basic"})
    return credentials.username