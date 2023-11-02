from pandas import DataFrame
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
import pickle
import psycopg2
from psycopg2 import Error

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
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from {cf.TABLENAME}")

except Error as e:
    print("\tError Querying database")
    print("\tpsycopg2 ERROR:", e)
    cursor.close()
    conn.close()

# Create pandas dataframe with metadata
metadata = DataFrame(cursor.fetchall(), columns=['UID', 'Topic', 'Title', 'Description', 'Source', 
                                                 'Tags', 'Licenses', 'Col_names', 'Row_count', 'Col_count', 
                                                 'Entry_count', 'Null_count', 'Usability'])

# close database connection
conn.close()
cursor.close()

# drop duplicate rows
metadata = metadata.drop_duplicates(subset="Title", keep="first").reset_index(drop=True) 

# Instantiate the TF-IDF recommender
print("\nFitting TF-IDF Recommendation model...")
recommender = TfidfRecommender(id_col='UID', tokenization_method='scibert')

# clean up the columns that will be combined for TF_IDF input
cols_to_clean = ["Topic", "Title", "Description"]
metadata[cols_to_clean] = metadata[cols_to_clean].applymap(lambda x: x.lower())
clean_col = 'cleaned_text'
df_clean = recommender.clean_dataframe(metadata, cols_to_clean, clean_col)

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
metadata.set_index('UID', inplace=True) # to index directly into metadata rows
for (rec_from_uid, rec_list) in full_rec_matrix.items():
    for (original_score,rec_to_uid) in rec_list:
        
        # keep track of weight that will be applied to this recommendation
        weight = 1
        
        # Increase score if datasets have the same license
        if(metadata.loc[rec_from_uid]['Licenses'] == metadata.loc[rec_to_uid]['Licenses']):
            weight *= cf.LICENSES_WEIGHT

        # Increase score by the number of shared tags
        from_tags = extract_strings(rec_from_uid, "Tags")
        to_tags = extract_strings(rec_to_uid, "Tags")
        num_shared_tags = len(from_tags & to_tags)
        weight *= cf.TAGS_WEIGHT ** num_shared_tags

        # Increase score by the number of column names
        from_cols = extract_strings(rec_from_uid, "Col_names")
        to_cols = extract_strings(rec_to_uid, "Col_names")
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