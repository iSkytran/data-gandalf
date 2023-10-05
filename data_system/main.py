from data_fetching import kaggle
from data_fetching.extractor_interface import MetadataExtractor
from data_uploading.uploader_interface import MetadataUploader

from data_fetching import kaggle_extractor

from data_uploading import json_to_db_uploader

# CONFIGURATION
SAVE_CSV = True
DATASET_FOLDER = "datasets"
METADATA_FOLDER = "metadata"
TOPICS = ['sports', 'academics', 'housing', 'health', 'finance']
SOURCE = "kaggle"


extractor = MetadataExtractor(DATASET_FOLDER)
uploader = MetadataUploader()

# Fetch Data
if SOURCE == "kaggle":
    # kaggle.fetch(TOPICS, DATASET_FOLDER)
    extractor = kaggle_extractor.KaggleExtractor(file_input_path=DATASET_FOLDER, file_output_path=METADATA_FOLDER, source="kaggle")

extractor.extract_topics(TOPICS)

# from csv_to_json_extractor import CSVToJsonExtractor


# # Script Configuration
# TOPICS = ["academics", "finance", "health", "housing", "sports"]
# SOURCE = "kaggle"
# FILE_INPUT_PATH = "datasets/" + TOPICS[0]
# FILE_OUTPUT_PATH = "metadata/" + TOPICS[0]

# extractor = CSVToJsonExtractor(file_input_path=FILE_INPUT_PATH, 
#                                file_output_path=FILE_OUTPUT_PATH, 
#                                 topic=TOPICS[0], source=SOURCE)

# extractor.extract()

# for topic in TOPICS:
#     if topic == TOPICS[0]:
#         continue
#     extractor.file_input_path = "datasets/" + topic
#     extractor.file_output_path = "metadata/" + topic
#     extractor.topic = topic
#     extractor.extract()
