from fastapi import FastAPI

from . import db
from . import models
from . import recommender

app = FastAPI()

@app.on_event("startup")
def startup() -> None:
    db.init()

@app.get("/health")
async def health() -> str:
    return "Service is up"

@app.get("/search", response_model=list[models.Dataset])
def search() -> str:
    return recommender.get_by_search()

@app.get("/dataset")
def dataset() -> str:
    return recommender.get_by_dataset()
