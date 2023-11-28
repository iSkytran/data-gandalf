from __future__ import annotations
import pickle
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
from sqlmodel import Session
from typing import Any

from backend.models import Dataset
import backend.config as cf
import backend.db as db

class RecommendationModel:
    """A class representing/wrapping the recommendation model.
    
    Attributes:
        model (TfidfRecommender | dict): The actual recommendation model.
    """
    _instance = None
    
    def __new__(cls, model_dir: str) -> RecommendationModel:
        """Creates a singleton instance for the model.

        Parameters:
            model_dir (str): The location of the model to load in from. 

        Returns:
            RecommendationModel: The singleton instance object.
        """
        if cls._instance == None:
            cls._instance = super(RecommendationModel, cls).__new__(cls)
            cls._instance._load_model(model_dir)
        return cls._instance
    
    def _load_model(self, model_dir: str) -> None:
        """Load in the model from storage.
        Parameters:
            model_dir (str): The location of the model to load in from. 
        """
        with open(model_dir, 'rb') as file:
            self.model = pickle.load(file)
        # TODO: catch exceptions if model file doesn't exist

    def rank(self, session: Session, dataset_id: str) -> list[tuple[Any, list[Dataset]]]:
        """Create a ranked list of recommendations for a dataset.

        Parameters:
            session (Session): The database session. 
            dataset_id (str): The id of the dataset to get recommendations for.

        Returns:
            list[tuple[Any, list[Dataset]]]: The ranked list of recommendations.

        Raises:
            Exception: If the model is not supported.
        """
        # Check if model is an instance of TfidfRecommender
        if isinstance(self.model, TfidfRecommender):
            full_rec_list = self.model.recommendations
            dataset_recs = full_rec_list[dataset_id] # (score, UID)s
            datasets = [(score, db.get_by_id(session, id)) for score,id in dataset_recs] # (score, Datasets)s
            return datasets
        # Check if model is dictionary
        elif isinstance(self.model, dict):
            dataset_recs = self.model[int(dataset_id)]
            datasets = [(score, db.get_by_id(session, id)) for score,id in dataset_recs][:100]
            return datasets
        else:
            raise Exception("Unexpected model type")

# Creates the recommendation model.
recommendation_model = RecommendationModel(Path(cf.MODEL_PATH))
