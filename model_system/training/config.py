from datetime import datetime

# Get time
current_datetime = datetime.now()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
hour = current_datetime.hour
minute = current_datetime.minute
second = current_datetime.second

# Where to save trained model
MODEL_PATH = f"../backend/models/{year}-{month:02d}-{day:02d}T{hour:02d}-{minute:02d}-{second:02d}_model.pkl"

# DB Configurations
DBNAME = "postgres"
USER = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
METADATA_TABLENAME = "dataset"
RATING_TABLENAME = "rating"

# Text columns to be used as input into TF-IDF
COLS_TO_CLEAN = ["topic", "title", "description"]
# These default column names match the pg_dump.sql file
ID_COL = "id"
LICENSES_COL = "licenses"
TAGS_COL = "tags"
COLUMN_NAMES_COL = "col_names"

# Tokenization method used by the TF-IDF Model
TOKENIZATION_METHOD = "scibert"

# Weights of specific features on final recommendation scores
# To deactivate a feature, set feature weight to 1
LICENSES_WEIGHT = 1.1
TAGS_WEIGHT = 1.1
COLUMN_NAMES_WEIGHT = 1.05
