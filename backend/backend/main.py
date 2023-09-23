from fastapi import FastAPI

from backend import db
from backend import recommender
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
def allDatasets() -> list[Dataset]:
    datasets = db.get_all()
    return recommender.rank(datasets)

# @app.get("/dataset")
# def dataset() -> list[str]:
#     datasets = db.get_all()
#     return recommender.rank(datasets)
