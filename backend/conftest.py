import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from backend.main import app, get_session
from backend.models import Dataset
from backend.recommender import RecommendationModel

@pytest.fixture
def recommendation_model() -> RecommendationModel:
    # Mocking the model path for testing
    TEST_MODEL_DIR = "test_model.pkl"
    return RecommendationModel(TEST_MODEL_DIR)

@pytest.fixture
def mock_db_session(mock_db_engine: Engine, init_mock_db: None) -> Generator[Session, None, None]:
    with Session(mock_db_engine) as session:
        yield session

@pytest.fixture
def mock_db_engine() -> Generator[Engine, None, None]:
    mock_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(mock_engine)
    yield mock_engine
    mock_engine.dispose()

@pytest.fixture
def init_mock_db(mock_db_engine: Engine) -> None:
    with Session(mock_db_engine) as session:
        datasets = [
            Dataset(topic="Topic1", title="Dataset1", description="Description", url="http://example.com", source="Source", tags="['example']", licenses="['MIT']", col_names="['example']", col_count=1, row_count=2, entry_count=2, null_count=0, usability=1.0),
            Dataset(topic="Topic2", title="Dataset2", description="Description", url="http://example.com", source="Source", tags="['example']", licenses="['MIT']", col_names="['example']", col_count=1, row_count=2, entry_count=2, null_count=0, usability=1.0),
            Dataset(topic="Topic1", title="Dataset3", description="Description", url="http://example.com", source="Source", tags="['example']", licenses="['MIT']", col_names="['example']", col_count=1, row_count=2, entry_count=2, null_count=0, usability=1.0),
            Dataset(topic="Topic2", title="Dataset4", description="Description", url="http://example.com", source="Source", tags="['example']", licenses="['MIT']", col_names="['example']", col_count=1, row_count=2, entry_count=2, null_count=0, usability=1.0),
        ]
        session.add_all(datasets)
        session.commit()

@pytest.fixture
def test_client(mock_db_session: Session) -> Generator[TestClient, None, None]:
    def mock_session():
        return mock_db_session
    app.dependency_overrides[get_session] = mock_session
    yield TestClient(app)
    app.dependency_overrides = {}

