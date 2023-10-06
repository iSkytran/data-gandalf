import pytest
from sqlmodel import create_engine, Session, SQLModel

from backend.models import Dataset
import backend.db as db

@pytest.fixture(scope="module")
def mock_db():
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine) # is this needed?
    yield engine # provide for testing
    engine.dispose() # tear down

@pytest.fixture
def sample_data(mock_db):
    with Session(mock_db) as session:
        datasets = [
            Dataset(topic="Topic1", name="Dataset1", description="Description", source="Source"),
            Dataset(topic="Topic2", name="Dataset2", description="Description", source="Source"),
            Dataset(topic="Topic1", name="Dataset3", description="Description", source="Source"),
            Dataset(topic="Topic2", name="Dataset4", description="Description", source="Source")
        ]
        session.add_all(datasets)
        session.commit()

@pytest.mark.usefixtures("sample_data")
def test_get_topics(mock_db):
    db.set_engine(mock_db)
    topics = db.get_topics()
    assert sorted(topics) == sorted(["Topic1", "Topic2"])

# TODO: why do the datasets double and triple in the next two tests??

@pytest.mark.usefixtures("sample_data")
def test_get_by_topic(mock_db):
    db.set_engine(mock_db)
    topic1_datasets = db.get_by_topic("Topic1")
    topic1_names = [d.name for d in topic1_datasets]
    topic2_datasets = db.get_by_topic("Topic2")
    topic2_names = [d.name for d in topic2_datasets]
    assert sorted(topic1_names) == sorted(["Dataset1","Dataset3"])
    assert sorted(topic2_names) == sorted(["Dataset2","Dataset4"])

@pytest.mark.usefixtures("sample_data")
def test_get_all(mock_db):
    db.set_engine(mock_db)
    datasets = db.get_all()
    names = [d.name for d in datasets]
    assert sorted(names) == sorted(["Dataset1","Dataset2","Dataset3","Dataset4"])
