import pytest
from backend.recommender import RecommendationModel

# Mocking the model path for testing
TEST_MODEL_DIR = "test_model.pkl"

@pytest.fixture
def recommendation_model():
    return RecommendationModel(TEST_MODEL_DIR)

def test_singleton_behavior(recommendation_model):
    # Ensure that instances are the same
    another_model = RecommendationModel(TEST_MODEL_DIR)
    assert recommendation_model is another_model

def test_ranking(recommendation_model):
    # TODO: how to not hard code this every retrain if want to compare ranking results
    assert recommendation_model.rank("245") is not None
