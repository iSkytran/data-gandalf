from sqlmodel import Session, SQLModel, create_engine, select
from typing import List

from database_connection.models import Dataset


db_url = "postgresql://postgres:password@localhost:5432"
engine = create_engine(db_url, echo=True)

def init():
    SQLModel.metadata.create_all(engine)

def create_dataset(dataset: Dataset):
    with Session(engine) as session:
        session.add(dataset)
        session.commit()

def create_datasets(datasets:List[Dataset]):
    with Session(engine) as session:
        for dataset in datasets:
            session.add(dataset)
        session.commit()

def get_all(limit: int = 100) -> list[Dataset]:
    with Session(engine) as session:
        datasets = session.exec(select(Dataset).limit(limit)).all()
        return datasets
