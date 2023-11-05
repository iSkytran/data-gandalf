from fastapi import FastAPI, Depends
from typing import Annotated, Any, Optional
from sqlmodel import Session, SQLModel, create_engine

from backend import config as cf
from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset, Rating

app = FastAPI()

# Database Setup
db_url = cf.DB_URL
engine = create_engine(db_url)
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/health")
async def get_health() -> str:
    return "Service is up"

@app.get("/topics", response_model=list[str])
def get_topics(session: Annotated[Session, Depends(get_session)]) -> list[str]:
    return db.get_topics(session)

@app.get("/datasets", response_model=list[Dataset])
def get_datasets(session: Annotated[Session, Depends(get_session)], topic: Optional[str] = None) -> list[Dataset]:
    if topic:
        datasets = db.get_by_topic(session, topic)
        return datasets
    else:
        datasets = db.get_all(session)
        return datasets
    
@app.get("/datasets/{uid}")
def get_dataset(session: Annotated[Session, Depends(get_session)], uid: str) -> tuple[list[Dataset], list[tuple[Any, list[Dataset]]]]:
    dataset = db.get_by_id(session, uid)
    return (dataset, recommendation_model.rank(session, uid))

@app.get("/ratings", response_model=list[Rating])
def get_ratings(session: Annotated[Session, Depends(get_session)], user_session: str, source_dataset: int) -> list[Rating]:
    return db.get_ratings(session, user_session, source_dataset)

@app.post("/ratings", response_model=Rating)
def post_rating(session: Annotated[Session, Depends(get_session)], rating: Rating) -> Rating:
    rating = Rating.from_orm(rating)
    if (rating.id == None):
        return db.add_rating(session, rating)
    else:
        return db.update_rating(session, rating)

@app.delete("/ratings/{uid}")
def delete_rating(session: Annotated[Session, Depends(get_session)], uid: int) -> None:
    db.delete_rating(session, uid)

