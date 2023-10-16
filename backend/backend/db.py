from sqlmodel import Session, SQLModel, create_engine, select
import os

from backend.models import Dataset

env_url = os.getenv("DATABASE_ADDRESS", "postgres:5432")
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
        datasets = list_conversion_helper(datasets)
        return datasets

def get_all(limit: int = 100) -> list[Dataset]:
    with Session(engine) as session:
        datasets = session.exec(select(Dataset).limit(limit)).all()
        datasets = list_conversion_helper(datasets)
        return datasets

def get_by_id(id: str) -> list[Dataset]:
    with Session(engine) as session:
        dataset = session.exec(select(Dataset).where(Dataset.id == id)).first()
        if dataset is None:
            #TODO: is this an error?
            pass
        return dataset

def list_conversion_helper(datasets: list[Dataset]) -> list[Dataset]:
    for dataset in datasets:
        tags_str = dataset.tags
        licenses_str = dataset.licenses
        col_names_str = dataset.col_names

        tags_str = tags_str.replace("\"", "")
        tags_str = tags_str.replace("{", "")
        tags_str = tags_str.replace("}", "")

        licenses_str = licenses_str.replace("\"", "")
        licenses_str = licenses_str.replace("{", "")
        licenses_str = licenses_str.replace("}", "")

        col_names_str = col_names_str.replace("\"", "")
        col_names_str = col_names_str.replace("{", "")
        col_names_str = col_names_str.replace("}", "")

        tags_list = tags_str.split(",")
        licenses_list = licenses_str.split(",")
        col_names_list = col_names_str.split(",")
        dataset.tags = tags_list
        dataset.licenses = licenses_list
        dataset.col_names = col_names_list
    return datasets