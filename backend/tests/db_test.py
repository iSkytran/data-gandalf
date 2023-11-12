from sqlmodel import Session
import backend.db as db

def test_get_topics(mock_db_session: Session):
    topics = db.get_topics(mock_db_session)
    assert sorted(topics) == sorted(["Topic1", "Topic2"])

def test_get_by_topic(mock_db_session: Session):
    topic1_datasets = db.get_by_topic(mock_db_session, "Topic1", offset=0)
    topic1_names = [d.title for d in topic1_datasets]
    topic2_datasets = db.get_by_topic(mock_db_session, "Topic2", offset=0)
    topic2_names = [d.title for d in topic2_datasets]
    assert sorted(topic1_names) == sorted(["Dataset1","Dataset3"])
    assert sorted(topic2_names) == sorted(["Dataset2","Dataset4"])

def test_get_all(mock_db_session: Session):
    datasets = db.get_all(mock_db_session, offset=0)
    names = [d.title for d in datasets]
    assert sorted(names) == sorted(["Dataset1","Dataset2","Dataset3","Dataset4"])

