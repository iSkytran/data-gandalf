# Where to save trained model
MODEL_PATH = "../backend/models/test.pkl"

# DB Configurations
DBNAME="training_database"
USER="postgres"
PASSWORD="default"
HOST="localhost"
PORT="5432"
TABLENAME="dataset"

# Text columns to be used as input into TF-IDF
COLS_TO_CLEAN = ["topic", "title", "description"]
# These default column names match the pg_dump.sql file
ID_COL ="id"
LICENSES_COL="licenses"
TAGS_COL="tags"
COLUMN_NAMES_COL="col_names"

# Tokenization method used by the TF-IDF Model
TOKENIZATION_METHOD="scibert"

# Weights of specific features on final recommendation scores
# To deactivate a feature, set feature weight to 1
LICENSES_WEIGHT=1.1
TAGS_WEIGHT=1.1
COLUMN_NAMES_WEIGHT=1.05
