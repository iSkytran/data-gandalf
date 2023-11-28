import pickle
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
from sqlmodel import Session
from typing import Any
import math

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

    def transform_score(self, score:float) -> float:
        adjusted_score = 0
        if score <= .05:
            adjusted_score = 1655 * score
        else:
            initial = 5.5 * math.log(score - .01) + 66
            adjusted_score = 100 - (1/3) * (100- initial)
        return adjusted_score

    def rank(self, session: Session, dataset_id: str) -> list[tuple[Any, list[Dataset]]]:
        # Check if model is an instance of TfidfRecommender
        if isinstance(self.model, TfidfRecommender):
            full_rec_list = self.model.recommendations
            dataset_recs = full_rec_list[dataset_id] # (score, UID)s
            datasets = []
            for score, id in dataset_recs:
                adjusted_score = self.transform_score(score)
                datasets.append(adjusted_score, db.get_by_id(session, id))
            return datasets
        # Check if model is dictionary
        elif isinstance(self.model, dict):
            dataset_recs = self.model[int(dataset_id)]
            datasets = []
            for score, id in dataset_recs[:100]:
                adjusted_score = self.transform_score(score)
                datasets.append((adjusted_score, db.get_by_id(session, id)))
            return datasets
        else:
            raise Exception("Unexpected model type")

recommendation_model = RecommendationModel(Path(cf.MODEL_PATH))

