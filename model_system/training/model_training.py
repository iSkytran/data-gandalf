from pandas import DataFrame
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
import pickle
import psycopg2
from psycopg2 import Error
from tqdm import tqdm

import config as cf # configurations

# Main Script Code

# Connect to database with metadata
try:
    print("\nConnecting to database...")
    conn = psycopg2.connect(
        dbname=cf.DBNAME,
        user=cf.USER,
        password=cf.PASSWORD,
        host=cf.HOST,
        port=cf.PORT
    )

except Error as e:
    print("\tError connecting to database")
    print("\tpsycopg2 ERROR:", e)

# Get all rows from database metadata table
try:
    print(f"\nQuerying rows from '{cf.TABLENAME}' table in '{cf.DBNAME}' database...")
    # Get columns names
    cursor = conn.cursor()
    cursor.execute('SELECT * from dataset LIMIT 1')
    column_names = [desc[0] for desc in cursor.description]
    # Create pandas dataframe
    cursor.execute('SELECT * from dataset')
    metadata = DataFrame(cursor.fetchall(), columns=column_names)

except Error as e:
    print("\tError Querying database")
    print("\tpsycopg2 ERROR:", e)

finally:
    # close database connection
    cursor.close()
    conn.close()

# Instantiate the TF-IDF recommender
print("\nFitting TF-IDF Recommendation model...")
recommender = TfidfRecommender(id_col=cf.ID_COL, tokenization_method=cf.TOKENIZATION_METHOD)

# clean up the columns that will be combined for TF_IDF input
metadata[cf.COLS_TO_CLEAN] = metadata[cf.COLS_TO_CLEAN].applymap(lambda x: x.lower())
clean_col = 'cleaned_text'
df_clean = recommender.clean_dataframe(metadata, cf.COLS_TO_CLEAN, clean_col)

# Tokenize text with tokenization_method specified in class instantiation
tf, vectors_tokenized = recommender.tokenize_text(df_clean, text_col=clean_col)

# Fit the TF-IDF vectorizer
recommender.fit(tf, vectors_tokenized)

# Run a function to run the private function that generates full recommendation list
top_k_recommendations = recommender.recommend_top_k_items(df_clean, k=10)

# Get recommendations
full_rec_matrix = recommender.recommendations

# Tune the model
print("\nTuning the model...")

# extract strings from their formatting in the metadata table
def extract_strings(uid, col_name):
    strings = metadata.loc[uid][col_name]
    strings = strings.strip("{}").replace('"',"")
    return {string.lower() for string in strings.split(',')}

# for every recommendation...
metadata.set_index(cf.ID_COL, inplace=True) # to index directly into metadata rows
for (rec_from_uid, rec_list) in tqdm(full_rec_matrix.items()):
    for (original_score,rec_to_uid) in rec_list:
        
        # keep track of weight that will be applied to this recommendation
        weight = 1
        
        # Increase score if datasets have the same license
        if(metadata.loc[rec_from_uid][cf.LICENSES_COL] == metadata.loc[rec_to_uid][cf.LICENSES_COL]):
            weight *= cf.LICENSES_WEIGHT

        # Increase score by the number of shared tags
        from_tags = extract_strings(rec_from_uid, cf.TAGS_COL)
        to_tags = extract_strings(rec_to_uid, cf.TAGS_COL)
        num_shared_tags = len(from_tags & to_tags)
        weight *= cf.TAGS_WEIGHT ** num_shared_tags

        # Increase score by the number of column names
        from_cols = extract_strings(rec_from_uid, cf.COLUMN_NAMES_COL)
        to_cols = extract_strings(rec_to_uid, cf.COLUMN_NAMES_COL)
        num_shared_cols = len(from_cols & to_cols)
        weight *= cf.COLUMN_NAMES_WEIGHT ** num_shared_cols

        # Apply the weight to this recommendation
        if(weight != 1):
            index = next((i for i, rec in enumerate(rec_list) if rec[1] == rec_to_uid), None)
            weighted_recommendation = (original_score * weight, rec_to_uid)
            rec_list[index] = weighted_recommendation

    # Reorder the recommendations based on their new weighted scores
    rec_list.sort(key=lambda x: x[0], reverse=True)

# Dump the full into our model pickle file
model_path = Path(cf.MODEL_PATH) 
with open(model_path, 'wb') as file:
    pickle.dump(full_rec_matrix, file)