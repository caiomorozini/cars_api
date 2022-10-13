import urllib3, requests, certifi
from fastapi import FastAPI
from app.db.database import database
from app.api.routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, render_template
from fastapi.middleware.wsgi import WSGIMiddleware
from app.api.routes import api
from app.db.database import SQLALCHEMY_DATABASE_URL
import requests


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app = FastAPI(title='Carford Car Shop API')

# Configurando aplicação FASTAPI
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(api_router)

flask_app = Flask(__name__)

flask_app.register_blueprint(
    api.blueprint
)

app.mount("/flask", WSGIMiddleware(flask_app))
