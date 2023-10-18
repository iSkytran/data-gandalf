from fastapi import FastAPI
from typing import Optional
from uuid import UUID

from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset, Rating

app = FastAPI()

@app.on_event("startup")
def startup() -> None:
    db.init()

@app.get("/health")
async def get_health() -> str:
    return "Service is up"

@app.get("/topics", response_model=list[str])
def get_topics() -> list[str]:
    return db.get_topics()

@app.get("/datasets", response_model=list[Dataset])
def get_datasets(topic: Optional[str] = None) -> list[Dataset]:
    if topic:
        datasets = db.get_by_topic(topic)
        return datasets
    else:
        datasets = db.get_all()
        return datasets
    
@app.get("/datasets/{uid}")
def get_dataset(uid: str):
    # TODO: get list of Dataset objects (get_dataset in db.py)
    return recommendation_model.rank(uid)

# TODO: POST ratings
@app.get("/ratings")
def get_ratings(user_session: UUID, source_dataset: int) -> list[Rating]:
    return db.get_ratings(user_session, source_dataset)

@app.post("/ratings")
def add_rating(rating: Rating) -> None:
    db.add_rating(rating)

@app.delete("/ratings/{uid}")
def delete_rating(uid: int) -> None:
    db.delete_rating(uid)

