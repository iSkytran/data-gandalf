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
        print(datasets[0])
        return datasets
    
@app.get("/dataset/{uid}")
def dataset(uid: str):
    # TODO: get list of Dataset objects (get_dataset in db.py)
    return recommendation_model.rank(uid)

# TODO: POST ratings
