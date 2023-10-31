from sqlmodel import Session, SQLModel, create_engine, select
from backend.models import Dataset, Rating, RatingRead
import os

env_url = os.getenv("DATABASE_ADDRESS", "database:5432")
db_url = f"postgresql://postgres:default@{env_url}"
engine = create_engine(db_url)

def set_engine(new_engine) -> None:
    """Replace engine for testing"""
    global engine
    engine = new_engine

def init() -> None:
    SQLModel.metadata.create_all(engine)

def get_topics() -> list[str]:
    with Session(engine) as session:
        topics = session.exec(select(Dataset.topic).distinct()).all()
        return topics

def get_by_topic(topic: str, limit: int = 100) -> list[Dataset]:
    with Session(engine) as session:
        datasets = session.exec(select(Dataset).where(Dataset.topic == topic).limit(limit)).all()
        return datasets

def get_all(limit: int = 100) -> list[Dataset]:
    with Session(engine) as session:
        datasets = session.exec(select(Dataset).limit(limit)).all()
        return datasets

def get_by_id(id: str) -> list[Dataset]:
    with Session(engine) as session:
        dataset = session.exec(select(Dataset).where(Dataset.id == id)).first()
        if dataset is None:
            #TODO: is this an error?
            pass
        return dataset

def add_rating(rating: Rating) -> RatingRead:
    with Session(engine) as session:
        session.add(rating)
        session.commit()
        session.refresh(rating)
        return rating

def update_rating(rating: Rating) -> RatingRead:
    with Session(engine) as session:
        updated = session.exec(select(Rating).where(Rating.id == rating.id)).one()
        updated.recommend = rating.recommend
        session.add(updated)
        session.commit()
        session.refresh(updated)
        return updated

def delete_rating(id: int) -> None:
    with Session(engine) as session:
        rating = session.exec(select(Rating).where(Rating.id == id))
        session.delete(rating.one())
        session.commit()

def get_ratings(user_session: str, source_dataset: int) -> list[RatingRead]:
    with Session(engine) as session:
        ratings = session.exec(select(Rating).where(Rating.user_session == user_session).where(Rating.source_dataset == source_dataset)).all()
        return ratings

