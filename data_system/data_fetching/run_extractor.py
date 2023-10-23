from data_fetching.kaggle_extractor import KaggleExtractor


# Script Configuration
TOPICS = ["academics", "finance", "health", "housing", "sports"]
FILE_INPUT_PATH = "datasets/"
FILE_OUTPUT_PATH = "metadata/"

extractor = KaggleExtractor(file_input_path=FILE_INPUT_PATH, 
                               file_output_path=FILE_OUTPUT_PATH)

extractor.extract_topics(TOPICS)

