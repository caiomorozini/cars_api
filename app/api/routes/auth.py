from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.db.database import users, database
from app.resources import utils, oauth2
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)
from starlette.status import HTTP_201_CREATED
from app.schemas import auth
from app.resources.utils import hash


router = APIRouter()

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):

    user = await database.fetch_one(
        users.select().where(users.c.email == user_credentials.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciais inválidas")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciais inválidas")

    # Create access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create",
        status_code=201,
        response_model=auth.ResponseNewUser
        )
async def create_user(user: auth.NewUser):
    # hash the password - user.password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = users.insert().values(**user.dict())
    id = await database.execute(new_user)
    return {**user.dict(), 'id': id}
