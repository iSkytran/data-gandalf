from pandas import DataFrame
from pathlib import Path
from recommenders.models.tfidf.tfidf_utils import TfidfRecommender
import pickle
import psycopg2

import training.config as cf # configurations

# Connect to database with metadata
conn = psycopg2.connect(
    dbname="training_database",
    user="postgres",
    password="default",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
cursor.execute('SELECT * from dataset')

# Create pandas data frame with metadata
metadata = DataFrame(cursor.fetchall(), columns=['UID', 'Topic', 'Title', 'Description', 'Source', 
                                                 'Tags', 'Licenses', 'Col_names', 'Row_count', 'Col_count', 
                                                 'Entry_count', 'Null_count', 'Usability'])

# why is each sports dataset duplicated three times???
metadata = metadata.drop_duplicates(subset="Title", keep="first").reset_index(drop=True) 

# Instantiate the TF-IDF recommender
recommender = TfidfRecommender(id_col='UID', tokenization_method='scibert')

# Assign columns to clean and combine
metadata = metadata.astype(str) # combined columns have to all be strings
metadata = metadata.applymap(lambda x: x.lower())

# For now, we will use all columns except the UID
cols_to_clean = metadata.columns.tolist()
cols_to_clean.remove("UID") 
clean_col = 'cleaned_text'
df_clean = recommender.clean_dataframe(metadata, cols_to_clean, clean_col)

# Tokenize text with tokenization_method specified in class instantiation
tf, vectors_tokenized = recommender.tokenize_text(df_clean, text_col=clean_col)

# Fit the TF-IDF vectorizer
recommender.fit(tf, vectors_tokenized)

# Run a function to run the private function that generates full recommendation list
top_k_recommendations = recommender.recommend_top_k_items(df_clean, k=10)

# Get recommendations
full_rec_list = recommender.recommendations

# Dump the model into our model pickle file
model_path = Path(cf.MODEL_PATH) 
with open(model_path, 'wb') as file:
    pickle.dump(full_rec_list, file)