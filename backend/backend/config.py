import os

MODEL_PATH = "models/recommendations.pkl"
ENV_URL = os.getenv("DATABASE_ADDRESS", "localhost:5432")
DB_URL = f"postgresql://postgres:password@{ENV_URL}"
