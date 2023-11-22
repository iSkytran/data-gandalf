from pandas import DataFrame, MultiIndex
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
import pickle
import psycopg2
from psycopg2 import Error
from tqdm import tqdm
import math

from . import config as cf

def get_metadata_and_ratings_from_db():
    metadata = None
    ratings = None
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

        print(f"\nQuerying rows from '{cf.METADATA_TABLENAME}' table in '{cf.DBNAME}' database...")
        # Get columns names
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from {cf.METADATA_TABLENAME} LIMIT 1')
        column_names = [desc[0] for desc in cursor.description]

        # Create pandas dataframe for metadata
        cursor.execute(f'SELECT * from {cf.METADATA_TABLENAME}')
        metadata = DataFrame(cursor.fetchall(), columns=column_names)

        print(f"\nQuerying rows from '{cf.RATING_TABLENAME}' table in '{cf.DBNAME}' database...")
        try:
            # Get columns names
            cursor.execute(f'SELECT * from {cf.RATING_TABLENAME} LIMIT 1')
            column_names = [desc[0] for desc in cursor.description]

            # Create pandas dataframe for ratings
            cursor.execute(f'SELECT * from {cf.RATING_TABLENAME}')
            ratings = DataFrame(cursor.fetchall(), columns=column_names)
        except Exception as e:
            print("\tNo ratings found in database. Ignoring ratings.")

    except Exception as e:
        print("\tDatabase error")
        print("\tpsycopg2 ERROR:", e)

    finally:
        # close database connection
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        return metadata, ratings
    
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

# return a weight for n positive ratings and m negative ratings
def rating_weight(n, m):
    # Range of values the weights can take, centered at 1
    # i.e. a range of 1 -> [0.5,1.5]; 0.5 -> [0.75,1.25]
    WEIGHT_RANGE = 1

    # The greater this threshold, the more ratings required to change the weight
    CONFIDENCE_THRESHOLD = 7 

    # return a neutral weight for equal ratings
    if(n == m):
        return 1

    # Calculate the ratio of the difference of ratings over all ratings
    ratio = (n - m) / (n + m)

    # Calculate confidence factor, placing more confidence around 1
    # confidence_factor = 1 - math.exp(-(n + m) / CONFIDENCE_THRESHOLD)
    confidence_factor = (1 - math.exp(-(n + m) / CONFIDENCE_THRESHOLD))

    return 1 + (WEIGHT_RANGE / 2) * ratio * confidence_factor


def tune_rec_matrix(rec_matrix,metadata,ratings):
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

            # Weight score based on user ratings
            try:
                rating = ratings.loc[(rec_from_uid,rec_to_uid)]
                up_ratings = rating[0][0]
                down_ratings = rating[0][1]
                weight *= rating_weight(up_ratings, down_ratings)
            except:
                pass # ignore recs that don't have a rating

            # Apply the weight to this recommendation
            if(weight != 1):
                index = next((i for i, rec in enumerate(rec_list) if rec[1] == rec_to_uid), None)
                weighted_recommendation = (original_score * weight, rec_to_uid)
                rec_list[index] = weighted_recommendation

        # Reorder the recommendations based on their new weighted scores
        rec_list.sort(key=lambda x: x[0], reverse=True)

    return rec_matrix

# Realigns the ratings to be a 2D matrix
def realign_ratings(ratings):
    # Calculate positive and negative ratings
    positive_ratings = ratings[ratings['recommend'] == True].groupby(['source_dataset', 'destination_dataset']).size().unstack(fill_value=0)
    negative_ratings = ratings[ratings['recommend'] == False].groupby(['source_dataset', 'destination_dataset']).size().unstack(fill_value=0)
    # Align the indices and columns to ensure both DataFrames have the same shape
    positive_ratings, negative_ratings = positive_ratings.align(negative_ratings, fill_value=0)
    # combine into a 2d matrix of source,destination with (positive,negative) ratings values
    return DataFrame({
        'ratings': list(zip(positive_ratings.to_numpy().flatten(), negative_ratings.to_numpy().flatten()))
    }, index=MultiIndex.from_product([positive_ratings.index, positive_ratings.columns], names=['source', 'destination']))


def main():
    # Open path before training as to not waste time training if we can't
    model_path = Path(cf.MODEL_PATH)
    try:
        open(model_path, 'wb')
    except Exception as e:
        print("\nFailed to write to given model path: ", e)
        exit(1)

    # Get metadata and ratings from database
    metadata, ratings = get_metadata_and_ratings_from_db()
    if metadata is None:
        print("\nFailed to retrieve metadata from database")
        exit(1)
    if ratings is None:
        print("\nFailed to retrieve ratings from database")
    else:
        ratings = realign_ratings(ratings)
    
    # Fit the TF-IDF model and then tune it
    recommendation_matrix = build_rec_matrix(metadata)
    recommendation_matrix = tune_rec_matrix(recommendation_matrix,metadata,ratings)

    # Dump the full into our model pickle file
    with open(model_path, 'wb') as file:
        pickle.dump(recommendation_matrix, file)  

    print("\nSuccesfully trained, serialized, and saved model")

if __name__ == '__main__':
    main()