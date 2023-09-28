import os
class MetadataExtractor:

    def __init__(self, file_input_path):
        self.file_input_path:str = file_input_path
        self.metadata:dict = None
        self.metadata_suffix = '_metadata.json'

    def extract_children(self, folder):
        # Get Path
        dataset_path:str = os.path.join(self.file_input_path, folder)

        # Extract Metadata
        self.metadata = self.extract_from_dataset(dataset_path)

        # Output Metadata to File
        self.output_data(str(self.metadata['title'] + self.metadata_suffix))

    def extract_from_dataset(self, dataset_folder) -> dict:
        pass
    
    def output_data(self, metadata):
        pass