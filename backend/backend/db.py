from sqlmodel import Session, SQLModel, create_engine, select
import os

from backend.models import Dataset

env_url = os.getenv("DATABASE_ADDRESS", "database:5432")
db_url = f"postgresql://postgres:default@{env_url}"
engine = create_engine(db_url)

def set_engine(new_engine):
    """Replace engine for testing"""
    global engine
    engine = new_engine

def init():
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

