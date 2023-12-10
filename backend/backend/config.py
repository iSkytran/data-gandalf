import os

# Path to the current recommendation model.
MODEL_PATH = "models/new_recommendations.pkl"
# The address to the PostgreSQL database. Can be overwritten using env variables.
ENV_URL = os.getenv("DATABASE_ADDRESS", "localhost:5432")

# The database connection string using ENV_URL.
DB_URL = f"postgresql://postgres:password@{ENV_URL}"
