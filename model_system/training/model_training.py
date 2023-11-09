from pandas import DataFrame
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
import pickle
import psycopg2
from psycopg2 import Error
from tqdm import tqdm
import os

from . import config as cf

def get_metadata_from_db():
    metadata = None
    conn = None
    cursor = None
    try:
        print("\nConnecting to database...")
        conn = psycopg2.connect(
            dbname=cf.DBNAME,
            user=cf.USER,
            password=cf.PASSWORD,
            host=cf.HOST,
            port=cf.PORT
        )

        print(f"\nQuerying rows from '{cf.TABLENAME}' table in '{cf.DBNAME}' database...")
        # Get columns names
        cursor = conn.cursor()
        cursor.execute('SELECT * from dataset LIMIT 1')
        column_names = [desc[0] for desc in cursor.description]

        # Create pandas dataframe
        cursor.execute('SELECT * from dataset')
        metadata = DataFrame(cursor.fetchall(), columns=column_names)

    except Exception as e:
        print("\tDatabase error")
        print("\tpsycopg2 ERROR:", e)

    finally:
        # close database connection
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        return metadata
    
def build_rec_matrix(metadata):
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
    recommender.recommend_top_k_items(df_clean, k=2)

    # Get recommendations
    return recommender.recommendations

def tune_rec_matrix(rec_matrix,metadata):
    # Tune the model
    print("\nTuning the model...")

    # extract strings from their formatting in the metadata table
    def extract_strings(uid, col_name):
        strings = metadata.loc[uid][col_name]
        strings = strings.strip("{}").replace('"',"")
        return {string.lower() for string in strings.split(',')}

    # for every recommendation...
    metadata.set_index(cf.ID_COL, inplace=True) # to index directly into metadata rows
    for (rec_from_uid, rec_list) in tqdm(rec_matrix.items()):
        for (original_score,rec_to_uid) in rec_list:
            
            # keep track of weight that will be applied to this recommendation
            weight = 1
            
            # Increase score if datasets have the same license
            if(cf.LICENSES_WEIGHT != 1):
                if(metadata.loc[rec_from_uid][cf.LICENSES_COL] == metadata.loc[rec_to_uid][cf.LICENSES_COL]):
                    weight *= cf.LICENSES_WEIGHT

            # Increase score by the number of shared tags
            if(cf.TAGS_WEIGHT != 1):
                from_tags = extract_strings(rec_from_uid, cf.TAGS_COL)
                to_tags = extract_strings(rec_to_uid, cf.TAGS_COL)
                num_shared_tags = len(from_tags & to_tags)
                weight *= cf.TAGS_WEIGHT ** num_shared_tags

            # Increase score by the number of column names
            if(cf.COLUMN_NAMES_WEIGHT != 1):
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

    return rec_matrix

def main():
    # Open path before training as to not waste time training if we can't
    model_path = Path(cf.MODEL_PATH)
    try:
        open(model_path, 'wb')
    except Exception as e:
        print("\nFailed to write to given model path: ", e)
        exit(1)

    # Get metadata from database
    metadata = get_metadata_from_db()
    if metadata is None:
        print("\nFailed to retrieve metadata from database")
        exit(1)
    
    # Fit the TF-IDF model and then tune it
    recommendation_matrix = build_rec_matrix(metadata)
    recommendation_matrix = tune_rec_matrix(recommendation_matrix,metadata)

    # Dump the full into our model pickle file
    with open(model_path, 'wb') as file:
        pickle.dump(recommendation_matrix, file)  

    print("\nSuccesfully trained, serialized, and saved model")

if __name__ == '__main__':
    main()