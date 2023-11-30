import os, json
from data_uploading.uploader_interface import MetadataUploader
from database_connection.models import Dataset
from database_connection.db import create_datasets, init

class JsonToDbUploader(MetadataUploader):
    """
    Extends MetadataUploader, defining how to convert metadata from .JSON files to DB records.

    Attributes
    -----------------------------
    file_input_path : str
        The path that contains topic folders that contain metadata JSON files.
        e.g. {self.file_input_path}/{topic}/{dataset-title}.json

    datasets_to_upload : list[Dataset]
        The list of Dataset objects to upload to the system. Populated by calling prepare_upload_for_topic.
    
    
    Methods
    -----------
    prepare_upload_for_topic(topic: str)
        Uses {self.file_input_path} and {topic} to find topic folder, then adds all datasets in it 
        to {self.datasets_to_upload}. Converts datasets from JSON to Dataset objects by calling
        {self.create_model_from_dict()}. 

    prepare_upload(topics: list[str])
        Calls prepare_upload_for_topic on each topic in {topics}. 

    upload()
        Uploads the topics in {self.datasets_to_upload} to the database configured 
        in the database_connection module. 

    create_model_from_dict(metadata: dict) -> Dataset
        Converts a metadata dictionary to a Dataset object. 

    report_issues()
        Reports the number of problems found as well as the number of datasets successfully
        uploaded. 

    """

    def __init__(self, file_input_path):
        self.file_input_path = file_input_path
        self.datasets_to_upload = []
        super().__init__()

    def prepare_upload_for_topic(self, topic: str):
        """ 
        Uses {self.file_input_path} and {topic} to find topic folder, then adds all datasets in it 
        to {self.datasets_to_upload}. Converts datasets from JSON to Dataset objects by calling
        {self.create_model_from_dict()}. 
        
        Params
        ------------
        topic: str
            The name of the folder to prepare uploads for ({self.file_input_path}/{topic}). 
            Searches the folder and converts all JSON files to Dataset objects.         
        """
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

    def prepare_upload(self, topics):
        """Calls prepare_upload_for_topic on each topic in {topics}. """
        for topic in topics:
            self.prepare_upload_for_topic(topic)
   
    def upload(self):
        """        
        Uploads the topics in {self.datasets_to_upload} to the database configured 
        in the database_connection module. 
        """
        # Upload datasets.
        init()
        create_datasets(self.datasets_to_upload)
        
    def create_model_from_dict(self, metadata:dict):
        """
        Converts a metadata dictionary to a Dataset object.
        
        Params
        -----------
        metadata : dict
            The dictionary containing metadata. Usually read in directly from a json file
            with json.load(file). 
        """
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
        """
        Reports the number of problems found as well as the number of datasets successfully
        uploaded.

        Return
        ---------
        Returns the number of files with problems.      
        """
        
        with open("data_uploading/problem-files-upload.txt", "w+") as newfile:
            newfile.write(json.dumps(self.problem_files))
        print("Successfully uploaded", len(self.datasets_to_upload), "datasets.")

        print("Found ", len(self.problem_files), " problem files while uploading. Look at data_uploading/problem-files-upload.txt for a list.")
        return len(self.problem_files)