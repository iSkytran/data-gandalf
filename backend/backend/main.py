from fastapi import FastAPI

from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset

app = FastAPI()

@app.on_event("startup")
def startup() -> None:
    db.init()

@app.get("/health")
async def health() -> str:
    return "Service is up"

@app.get("/datasets", response_model=list[Dataset])
def allDatasets() -> str:
    datasets = db.get_all()
    return datasets



# @app.get("/dataset")
# def dataset() -> list[str]:
#     datasets = db.get_all()
#     return recommender.rank(datasets)
