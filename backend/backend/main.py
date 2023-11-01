from fastapi import FastAPI
from typing import Optional

from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset, Rating, RatingRead

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
def get_dataset(uid: str) -> list[Dataset]:
    dataset = db.get_by_id(uid)
    return [dataset, recommendation_model.rank(uid)]

@app.get("/ratings", response_model=list[RatingRead])
def get_ratings(user_session: str, source_dataset: int) -> list[RatingRead]:
    return db.get_ratings(user_session, source_dataset)

@app.post("/ratings", response_model=RatingRead)
def post_rating(rating: Rating) -> RatingRead:
    rating = Rating.from_orm(rating)
    if (rating.id == None):
        return db.add_rating(rating)
    else:
        return db.update_rating(rating)

@app.delete("/ratings/{uid}")
def delete_rating(uid: int) -> None:
    db.delete_rating(uid)

