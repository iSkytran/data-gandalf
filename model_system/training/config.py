# Where to save trained model
MODEL_PATH = "../backend/models/new_recommendations.pkl"
# DB Configurations
DBNAME="training_database"
USER="postgres"
PASSWORD="default"
HOST="localhost"
PORT="5432"
TABLENAME="dataset"
# Weights of certain features on final recommendation scores
LICENSES_WEIGHT=1.1
TAGS_WEIGHT=1.1
COLUMN_NAMES_WEIGHT=1.05
