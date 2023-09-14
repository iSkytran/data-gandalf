from sqlmodel import Session, SQLModel, create_engine, select

from backend.models import Dataset

db_url = "postgresql://postgres:default@database:5432"
engine = create_engine(db_url)

def init():
    SQLModel.metadata.create_all(engine)

def get_all(limit: int = 100) -> list[Dataset]:
    with Session(engine) as session:
        datasets = session.exec(select(Dataset).limit(limit)).all()
        return datasets
