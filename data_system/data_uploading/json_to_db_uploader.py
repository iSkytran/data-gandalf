import os, json
from data_uploading.uploader_interface import MetadataUploader
from database_connection.models import Dataset
from database_connection.db import create_datasets, init

class JsonToDbUploader(MetadataUploader):
    def __init__(self, file_input_path):
        self.file_input_path = file_input_path
        self.datasets_to_upload = []
        super().__init__()

    def prepare_upload_for_topic(self, topic):
        topic_path = os.path.join(self.file_input_path, topic)
        files_to_upload = os.listdir(topic_path)
        # Add datasets to list
        for filename in files_to_upload:
            try:
                # READ METADATA TO MODEL
                path:str = os.path.join(topic_path, filename)

                if path[len(path) - 5:] != '.json':
                    continue
                
                file = open(path, 'r')
                dataset_dict = json.load(file)
                dataset = self.create_model_from_dict(dataset_dict)

                self.datasets_to_upload.append(dataset)
            except Exception as e:
                self.problem_files.append(filename)
                print(e)
    # Processes files on input path and prepares for uploading.
    def prepare_upload(self, topics):
        for topic in topics:
            self.prepare_upload_for_topic(topic)
   
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
        dataset.url = metadata['url']
        dataset.tags = metadata['tags']
        dataset.title = metadata['title']
        dataset.topic = metadata['topic']
        dataset.source = metadata['source']
        dataset.col_names = metadata['col_names']
        dataset.usability = metadata['usability']
        dataset.entry_count = metadata['num_entries']
        dataset.null_count = metadata['null_count']
        dataset.licenses = []
        try:
            dataset.licenses = list(map(lambda x: x['name'], metadata['licenses']))
        except Exception as e:
            self.problem_files.append(dataset.topic + "(License issue)")

        return dataset

    def report_issues(self):
        # Report issues.
        with open("data_uploading/problem-files-upload.txt", "w+") as newfile:
            newfile.write(json.dumps(self.problem_files))
        print("Successfully uploaded", len(self.datasets_to_upload), "datasets.")

        print("Found ", len(self.problem_files), " problem files while uploading. Look at data_uploading/problem-files-upload.txt for a list.")
        return len(self.problem_files)