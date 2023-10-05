from fastapi import FastAPI
from typing import Optional

from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset

app = FastAPI()

@app.on_event("startup")
def startup() -> None:
    db.init()

@app.get("/health")
async def health() -> str:
    return "Service is up"

@app.get("/topics", response_model=list[str])
def topics() -> list[str]:
    return db.get_topics()

@app.get("/datasets", response_model=list[Dataset])
def datasets(topic: Optional[str] = None) -> list[Dataset]:
    if topic:
        datasets = db.get_by_topic(topic)
        return datasets
    else:
        datasets = db.get_all()
        return datasets
