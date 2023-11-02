import os
class MetadataExtractor:

    def __init__(self, file_input_path):
        self.file_input_path:str = file_input_path
        self.metadata_suffix = '_metadata.json'
        self.datasets_processed = []
        self.problem_files = []

    # Extract all topics in given list. 
    def extract_topics(self, topics):
        for topic in topics:
            self.extract_topic(topic)

    # Extract All Children Datasets from a Parent Folder.
    def extract_topic(self, topic):
        topic_folder = os.path.join(self.file_input_path, topic)
        for dataset_folder in os.listdir(topic_folder):
            try:
                # Get Path
                dataset_path:str = os.path.join(topic_folder, dataset_folder)

                # Extract Metadata
                metadata = self.extract_from_dataset(dataset_path, topic)

                filename = str("".join(filter(lambda x: x.isalpha(), metadata['title'])) + self.metadata_suffix)
                
                self.output_data(metadata, target_folder=topic, filename=filename)
            except Exception as e:
                self.problem_files.append(str(dataset_folder + ": " + str(e)))
                print("Problem:", e)
    # Extract a single dataset.
    def extract_from_dataset(self, dataset_folder, topic) -> dict:
        pass
    
    # Output the data gained from extraction.
    def output_data(self, metadata, target_folder, filename):
        pass

    # Report any issues.
    def report_issues(self):
        pass
