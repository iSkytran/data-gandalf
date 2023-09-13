from sqlmodel import SQLModel, create_engine

db_url = "postgresql://postgres:default@localhost:5432"
connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)

def init():
    SQLModel.metadata.create_all(engine)
