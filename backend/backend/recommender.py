import pickle
from pathlib import Path
from backend.models import Dataset
import db

# TODO: add documentation
class RecommendationModel:
    _instance = None
    
    def __new__(cls, model_dir):
        if cls._instance == None:
            cls._instance = super(RecommendationModel, cls).__new__(cls)
            cls._instance._load_model(model_dir)
        return cls._instance
    
    def _load_model(self, model_dir):
        with open(model_dir, 'rb') as file:
            self.model = pickle.load(file)
        # TODO: catch exceptions if model file doesn't exist

    def rank(self, dataset_id: str) -> list[Dataset]:
        full_rec_list = self.model.recommendations
        dataset_recs = full_rec_list[dataset_id]
        # dataset_recs is (score, UID)s, here is list of (Datasets, score)s if needed for frontend:
        datasets = [(score, db.get_by_id(id)) for score,id in dataset_recs]
        # return dataset_recs # or datasets
        return datasets

recommendation_model = RecommendationModel(Path("../models/model.pkl"))
# TODO: make this path come frome config or env variable
# TODO: does path only work with Docker?