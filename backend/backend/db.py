from sqlmodel import Session, SQLModel, create_engine, select

from backend.models import Dataset

db_url = "postgresql://postgres:default@database:5432"
engine = create_engine(db_url)

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

