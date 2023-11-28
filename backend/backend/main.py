from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Response
from typing import Annotated, Any, Optional
from sqlmodel import Session, SQLModel, create_engine
from psycopg2.extensions import register_adapter, AsIs
import numpy as np

from backend import config as cf
from backend import db
from backend.recommender import recommendation_model
from backend.models import Dataset, Rating

# Global variable for the database engine.
db_engine = None

# Database Setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the database connection and tables on startup.
    
    Parameters:
        app (FastAPI): Required for a lifespan function.
    """
    global db_engine
    db_url = cf.DB_URL
    db_engine = create_engine(db_url)
    SQLModel.metadata.create_all(db_engine)
    register_adapter(np.int64, AsIs)
    yield

app = FastAPI(lifespan=lifespan)

def get_session():
    """A function to generate a database session to interact with the database.
    Needed for dependency injection and overrides during testing. 

    Yields:
        Session: A database session.
    """
    with Session(db_engine) as session:
        yield session

@app.get("/health")
async def get_health() -> str:
    """Simple endpoint to check if the backend is running.
    
    Returns:
        str: A string stating that the service is running.
    """
    return "Service is up"

@app.get("/topics", response_model=list[str])
def get_topics(session: Annotated[Session, Depends(get_session)]) -> list[str]:
    """GET endpoint that gets a list of all the various topics in the database.

    Parameters:
        session (Session): A FastAPI dependency with the database session. 
    
    Returns:
        list[str]: A list of topic strings.
    """
    return db.get_topics(session)

@app.get("/datasets", response_model=list[Dataset])
def get_datasets(session: Annotated[Session, Depends(get_session)], response: Response, topic: Optional[str] = None, offset: Optional[int] = 0) -> list[Dataset]:
    """GET endpoint to get all the datasets or datasets by topic.
    This is paginated such that the X-Offset-Count header field allows for
    accessing the next set of datasets.

    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        response (Response): The object representing the response.
        topic (str, Optional): A topic to filter down by. Defaults to None.
        offset (int, Optional): A number representing how many items off from
            the beginning to return. Defaults to 0.

    Returns:
        list[Dataset]: A list of dataset objects.
    """
    response.headers["X-Offset-Count"] = str(offset)
    if topic and topic != "":
        datasets = db.get_by_topic(session, topic, offset)
        response.headers["X-Total-Count"] = str(db.get_topic_count(session, topic))
        return datasets
    else:
        datasets = db.get_all(session, offset)
        response.headers["X-Total-Count"] = str(db.get_all_count(session))
        return datasets
    
@app.get("/datasets/{uid}")
def get_dataset(session: Annotated[Session, Depends(get_session)], uid: str) -> tuple[list[Dataset], list[tuple[Any, list[Dataset]]]]:
    """GET endpoint to get a specified dataset and its relevant metadata, as
    well as a ranked list of recommended datasets similar to the dataset
    identified by uid.

    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        uid (int): An integer value of the id of the dataset to get.

    Returns:
        tuple[list[Dataset], list[tuple[Any, list[Dataset]]]]: The chosen dataset
            and a sorted list of recommendations.
    """
    dataset = db.get_by_id(session, uid)
    return (dataset, recommendation_model.rank(session, uid))

@app.get("/ratings", response_model=list[Rating])
def get_ratings(session: Annotated[Session, Depends(get_session)], user_session: str, source_dataset: int) -> list[Rating]:
    """GET endpoint to get the user ratings for a dataset.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        user_session (str): A unique string representing a session for a user.
        source_dataset (int): The unique identifier for the dataset which
            the ratings are being retrieved for.

    Returns:
        list[Rating]: A list of rating objects with the specified source dataset.
    """
    return db.get_ratings(session, user_session, source_dataset)

@app.post("/ratings", response_model=Rating)
def post_rating(session: Annotated[Session, Depends(get_session)], rating: Rating) -> Rating:
    """POST endpoint to add or update a rating for a dataset.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        rating (Rating): The rating to add or be updated.

    Returns:
        Rating: The added/updated rating.
    """
    rating = Rating.from_orm(rating)
    if (rating.id == None):
        return db.add_rating(session, rating)
    else:
        return db.update_rating(session, rating)

@app.delete("/ratings/{uid}")
def delete_rating(session: Annotated[Session, Depends(get_session)], uid: int) -> None:
    """DELETE endpoint to remove a rating.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        uid (int): The rating id of the rating to be removed.
    """
    db.delete_rating(session, uid)
