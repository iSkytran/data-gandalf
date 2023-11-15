import os

MODEL_PATH = "models/2023-11-14T12-30-11_model.pkl"
ENV_URL = os.getenv("DATABASE_ADDRESS", "localhost:5432")
DB_URL = f"postgresql://postgres:password@{ENV_URL}"

