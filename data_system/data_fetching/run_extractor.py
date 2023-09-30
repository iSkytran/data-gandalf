from csv_to_json_extractor import CSVToJsonExtractor


# Script Configuration
TOPICS = ["academics", "finance", "health", "housing", "sports"]
SOURCE = "kaggle"
FILE_INPUT_PATH = "datasets/" + TOPICS[0]
FILE_OUTPUT_PATH = "metadata/" + TOPICS[0]

extractor = CSVToJsonExtractor(file_input_path=FILE_INPUT_PATH, 
                               file_output_path=FILE_OUTPUT_PATH, 
                                topic=TOPICS[0], source=SOURCE)

extractor.extract_children()

for topic in TOPICS:
    if topic == TOPICS[0]:
        continue
    extractor.file_input_path = "datasets/" + topic
    extractor.file_output_path = "metadata/" + topic
    extractor.topic = topic
    extractor.extract_children()

