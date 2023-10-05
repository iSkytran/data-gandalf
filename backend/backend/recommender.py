import pickle
from pathlib import Path

from backend.models import Dataset

# TODO: add documentation
class RecomendationModel:
    _instance = None
    
    def __new__(cls, model_dir):
        if cls._instance == None:
            cls._instance = super(RecomendationModel, cls).__new__(cls)
            cls._instance._load_model(model_dir)
        return cls._instance
    
    def _load_model(self, model_dir):
        with open(model_dir, 'rb') as file:
            self.model = pickle.load(file)
        # TODO: catch exceptions if model file doesn't exist

    def rank(self, dataset_id: str) -> list[Dataset]:
        full_rec_list = self.model.recommendations
        dataset_recs = full_rec_list[dataset_id]
        return dataset_recs

recommendation_model = RecomendationModel(Path("models/model.pkl")) # TODO: make this path come frome config or env variable