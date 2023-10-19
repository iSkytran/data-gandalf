import pickle
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender

from backend.models import Dataset
import backend.config as cf
import backend.db as db

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
        # Check if model is an instance of TfidfRecommender
        if isinstance(self.model, TfidfRecommender):
            full_rec_list = self.model.recommendations
            dataset_recs = full_rec_list[dataset_id] # (score, UID)s
            datasets = [(score, db.get_by_id(id)) for score,id in dataset_recs] # (score, Datasets)s
            return datasets
        # Check if model is dictionary
        elif isinstance(self.model, dict):
            print(self.model)
            dataset_recs = self.model[dataset_id]
            datasets = [(score, db.get_by_id(id)) for score,id in dataset_recs]
            return datasets
        else:
            raise Exception("Unexpected model type")

recommendation_model = RecommendationModel(Path(cf.MODEL_PATH))