import os
class MetadataExtractor:

    def __init__(self, file_input_path):
        self.file_input_path:str = file_input_path
        self.metadata_suffix = '_metadata.json'
        self.datasets_processed = []
        self.problem_files = []

    # Extract All Children Datasets from a Parent Folder.
    def extract_children(self):
        for dataset_folder in os.listdir(self.file_input_path):
            # Get Path
            dataset_path:str = os.path.join(self.file_input_path, dataset_folder)

            # Extract Metadata
            metadata = self.extract_from_dataset(dataset_path)

            # Output Metadata to File
            self.output_data(metadata, str(metadata['title'] + self.metadata_suffix))

    # Extract a single dataset.
    def extract_from_dataset(self, dataset_folder) -> dict:
        pass
    
    # Output the data gained from extraction.
    def output_data(self, metadata, target):
        pass

    # Report any issues.
    def report_issues(self):
        pass
