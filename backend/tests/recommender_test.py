from sqlmodel import Session
from backend.recommender import RecommendationModel

def test_singleton_behavior(recommendation_model: RecommendationModel):
    # Ensure that instances are the same
    TEST_MODEL_DIR = "test_model.pkl"
    another_model = RecommendationModel(TEST_MODEL_DIR)
    assert recommendation_model is another_model

def test_ranking(mock_db_session: Session, recommendation_model: RecommendationModel):
    # TODO: how to not hard code this every retrain if want to compare ranking results
    assert recommendation_model.rank(mock_db_session, "1837") is not None

