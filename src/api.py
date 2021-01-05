from os import name
from typing import List

from fastapi import Depends, FastAPI

from src import models, schemas
from src.db import Session, get_db

app = FastAPI()


@app.get("/hello")
def get_hello() -> str:
    return "hello"


@app.get("/user", response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> models.UserModel:
    return db.query(models.UserModel).offset(skip).limit(limit).all()


@app.post("/user", response_model=schemas.User)
def create_user(
    payload: schemas.UserCreate, db: Session = Depends(get_db)
) -> models.UserModel:
    obj = models.UserModel(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
