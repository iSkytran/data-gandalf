import os, json
from uploader_interface import MetadataUploader
from database_connection.models import Dataset
from database_connection.db import create_datasets, init

class JsonToDbUploader(MetadataUploader):
    def __init__(self, file_input_path):
        self.file_input_path = file_input_path
        self.datasets_to_upload = []
        super().__init__()

    # Processes files on input path and prepares for uploading.
    def prepare_upload(self):
        files_to_upload = os.listdir(self.file_input_path)

        # Add datasets to list
        for filename in files_to_upload:
            try:
                # READ METADATA TO MODEL
                path:str = os.path.join(self.file_input_path, filename)

                if path[len(path) - 5:] != '.json':
                    continue
                
                file = open(path, 'r')
                dataset_dict = json.load(file)
                dataset = self.create_model_from_dict(dataset_dict)

                self.datasets_to_upload.append(dataset)
            except Exception as e:
                self.problem_files.append(filename)
                print(e)
   
    # Uploads datasets to the database.
    def upload(self):
        # Upload datasets.
        init()
        create_datasets(self.datasets_to_upload)
        
    # Creates a model from a metadata dict
    def create_model_from_dict(self, metadata:dict):
        dataset = Dataset()
        dataset.row_count = metadata['row_count']
        dataset.col_count = metadata['col_count']
        dataset.description = metadata['description']
        dataset.licenses = []
        dataset.tags = metadata['tags']
        dataset.title = metadata['title']
        dataset.topic = metadata['topic']
        dataset.source = metadata['source']
        dataset.col_names = metadata['col_names']
        dataset.usability = metadata['usability']
        dataset.entry_count = metadata['num_entries']
        dataset.null_count = metadata['null_count']
        return dataset

    def report_issues(self):
        # Report issues.
        with open("problem-files-upload.txt", "w+") as newfile:
            newfile.write(json.dumps(self.problem_files))
        print("Found ", len(self.problem_files), " problem files. Look at problem-files-upload.txt for a list.")
