from sqlmodel import Session, select
from sqlalchemy import func
from backend.models import Dataset, Rating

def get_topics(session: Session) -> list[str]:
    topics = session.exec(select(Dataset.topic).distinct()).all()
    return topics

def get_topic_count(session: Session, topic: str) -> int:
    count = session.exec(select([func.count(Dataset.id)]).where(Dataset.topic == topic)).one()
    return count

def get_by_topic(session: Session, topic: str, offset: int, limit: int = 100) -> list[Dataset]:
    datasets = session.exec(select(Dataset).where(Dataset.topic == topic).limit(limit).offset(offset)).all()
    datasets = list_conversion_helper(datasets)
    return datasets

def get_all_count(session: Session) -> int:
    count = session.exec(select([func.count(Dataset.id)])).one()
    return count

def get_all(session: Session, offset: int, limit: int = 100) -> list[Dataset]:
    datasets = session.exec(select(Dataset).limit(limit).offset(offset)).all()
    datasets = list_conversion_helper(datasets)
    return datasets

def get_by_id(session: Session, id: str) -> list[Dataset]:
    dataset = session.exec(select(Dataset).where(Dataset.id == id)).first()
    if dataset is not None:
        dataset = list_conversion_helper([dataset])
        return dataset
    else:
        return []

def add_rating(session: Session, rating: Rating) -> Rating:
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating

def update_rating(session: Session, rating: Rating) -> Rating:
    updated = session.exec(select(Rating).where(Rating.id == rating.id)).one()
    updated.recommend = rating.recommend
    session.add(updated)
    session.commit()
    session.refresh(updated)
    return updated

def delete_rating(session: Session, id: int) -> None:
    rating = session.exec(select(Rating).where(Rating.id == id))
    session.delete(rating.one())
    session.commit()

def get_ratings(session: Session, user_session: str, source_dataset: int) -> list[Rating]:
    ratings = session.exec(select(Rating).where(Rating.user_session == user_session).where(Rating.source_dataset == source_dataset)).all()
    return ratings

def list_conversion_helper(datasets: list[Dataset]) -> list[Dataset]:
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
