from sqlmodel import Session, select
from sqlalchemy import func
from backend.models import Dataset, Rating

def get_topics(session: Session) -> list[str]:
    """Retrieves a list of all the various topics in the database.

    Parameters:
        session (Session): The database session. 
    
    Returns:
        list[str]: A list of topic strings.
    """
    topics = session.exec(select(Dataset.topic).distinct()).all()
    return topics

def get_topic_count(session: Session, topic: str) -> int:
    """Retrieves a count of datasets associated with a topic.

    Parameters:
        session (Session): The database session. 
        topic (str): The topic to get a count of dataset for.
    
    Returns:
        int: The number of datasets for the topic.
    """
    count = session.exec(select([func.count(Dataset.id)]).where(Dataset.topic == topic)).one()
    return count

def get_by_topic(session: Session, topic: str, offset: int, limit: int = 100) -> list[Dataset]:
    """Retrieves datasets by topic.

    Parameters:
        session (Session): The database session. 
        topic (str): A topic to filter down by.
        offset (int): A number representing how many items off from
            the beginning to return.
        limit (int): A number representing how many items to return. Defaults
            to 100.

    Returns:
        list[Dataset]: A list of dataset objects.
    """
    datasets = session.exec(select(Dataset).where(Dataset.topic == topic).limit(limit).offset(offset)).all()
    datasets = list_conversion_helper(datasets)
    return datasets

def get_all_count(session: Session) -> int:
    """Retrieves a count of all the datasets in the system.

    Parameters:
        session (Session): The database session. 
    
    Returns:
        int: The number of datasets.
    """
    count = session.exec(select([func.count(Dataset.id)])).one()
    return count

def get_all(session: Session, offset: int, limit: int = 100) -> list[Dataset]:
    """Retrieves all the datasets in the system.

    Parameters:
        session (Session): The database session. 
        offset (int): A number representing how many items off from
            the beginning to return.
        limit (int): A number representing how many items to return. Defaults
            to 100.

    Returns:
        list[Dataset]: A list of dataset objects.
    """
    datasets = session.exec(select(Dataset).limit(limit).offset(offset)).all()
    datasets = list_conversion_helper(datasets)
    return datasets

def get_by_id(session: Session, id: str) -> list[Dataset]:
    """Retrieves a dataset by its id.

    Parameters:
        session (Session): The database session. 
            the beginning to return.
        id (str): The dataset id to retrieve.

    Returns:
        list[Dataset]: A list containing the dataset requested.
    """
    dataset = session.exec(select(Dataset).where(Dataset.id == id)).first()
    if dataset is not None:
        dataset = list_conversion_helper([dataset])
        return dataset
    else:
        return []

def add_rating(session: Session, rating: Rating) -> Rating:
    """Adds a rating for a dataset.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        rating (Rating): The rating to add.

    Returns:
        Rating: The added rating.
    """
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating

def update_rating(session: Session, rating: Rating) -> Rating:
    """Updates a rating for a dataset.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        rating (Rating): The rating to update.

    Returns:
        Rating: The updated rating.
    """
    updated = session.exec(select(Rating).where(Rating.id == rating.id)).one()
    updated.recommend = rating.recommend
    session.add(updated)
    session.commit()
    session.refresh(updated)
    return updated

def delete_rating(session: Session, id: int) -> None:
    """Removes a rating.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        id (int): The rating id of the rating to be removed.
    """
    rating = session.exec(select(Rating).where(Rating.id == id))
    session.delete(rating.one())
    session.commit()

def get_ratings(session: Session, user_session: str, source_dataset: int) -> list[Rating]:
    """Retrieves the user ratings for a dataset.
    
    Parameters:
        session (Session): A FastAPI dependency with the database session. 
        user_session (str): A unique string representing a session for a user.
        source_dataset (int): The unique identifier for the dataset which
            the ratings are being retrieved for.

    Returns:
        list[Rating]: A list of rating objects with the specified source dataset.
    """
    ratings = session.exec(select(Rating).where(Rating.user_session == user_session).where(Rating.source_dataset == source_dataset)).all()
    return ratings

def list_conversion_helper(datasets: list[Dataset]) -> list[Dataset]:
    """Helper function to convert the JSON fields to proper form.
    
    Parameters:
        dataset (list[Dataset]): The input list of datasets to format.

    Returns:
        list[Dataset]: The formatted list of dataset.
    """
    for dataset in datasets:
        tags_str = dataset.tags
        licenses_str = dataset.licenses
        col_names_str = dataset.col_names

        if tags_str is not None:
            tags_str = tags_str.replace("\"", "")
            tags_str = tags_str.replace("{", "")
            tags_str = tags_str.replace("}", "")
            dataset.tags = tags_str 

        if licenses_str is not None:
            licenses_str = licenses_str.replace("\"", "")
            licenses_str = licenses_str.replace("{", "")
            licenses_str = licenses_str.replace("}", "")
            dataset.licenses = licenses_str

        if col_names_str is not None:
            col_names_str = col_names_str.replace("\"", "")
            col_names_str = col_names_str.replace("{", "")
            col_names_str = col_names_str.replace("}", "")
            dataset.col_names = col_names_str
    return datasets
