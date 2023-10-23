import shutil, os

from data_fetching import kaggle
from data_fetching.extractor_interface import MetadataExtractor
from data_uploading.uploader_interface import MetadataUploader

from data_fetching.kaggle_extractor import KaggleExtractor

from data_uploading.json_to_db_uploader import JsonToDbUploader

# CONFIGURATION

# Whether to save downloaded CSV files from the datasets. 
SAVE_CSV = False
DATASET_FOLDER = "datasets"

# Whether to save the metadata JSON objects created. Should be true if you want the ability to edit.
SAVE_METADATA = False
METADATA_FOLDER = "metadata"

# The topics to query from. 
TOPICS = ['sports', 'education', 'housing', 'health', 'finance', 'energy', 'politics', 'agriculture', 'chemistry', 'entertainment']

# Source to query. 
SOURCE = "kaggle"

# Initialize default objects to be overridden. 
extractor = MetadataExtractor(DATASET_FOLDER)
uploader = MetadataUploader()

# Override extractor and uploader objects. 
if SOURCE == "kaggle":
    kaggle.fetch(TOPICS, DATASET_FOLDER)
    extractor = KaggleExtractor(file_input_path=DATASET_FOLDER, file_output_path=METADATA_FOLDER)
    uploader = JsonToDbUploader(file_input_path=METADATA_FOLDER)

# # Extract Topics. 
extractor.extract_topics(TOPICS)

print("SUCCESSFULLY EXTRACTED TOPICS.")

# Upload Topics. 
uploader.prepare_upload(topics=TOPICS)
uploader.upload()


print("SUCCESSFULLY UPLOADED METADATA.")

# Delete Unnecessary data. 
if not SAVE_CSV:
    for topic in TOPICS:
        shutil.rmtree(os.path.join(DATASET_FOLDER, topic))

if not SAVE_METADATA:
    for topic in TOPICS:
        shutil.rmtree(os.path.join(METADATA_FOLDER, topic))