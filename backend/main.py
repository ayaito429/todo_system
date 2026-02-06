from fastapi import FastAPI
from db.base import Base
from db.session import engine
from db import models 

app = FastAPI()


@app.get("/")
def health_check():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}
