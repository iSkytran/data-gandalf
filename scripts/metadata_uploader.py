import os, json
from db import init, get_all, create_datasets

import pandas as pd

from models import Dataset

# Initialize Database Connection
init()

# To take all values from folder, specify folder. Leave as empty string to specify individual files.
FILE_INPUT_PATH = "metadata/academics"
INPUT_FILES = []


if FILE_INPUT_PATH != "":
    INPUT_FILES = os.listdir(FILE_INPUT_PATH)

# Creates a model from a metadata dict
def create_model_from_dict(metadata:dict):
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
    # id: Optional[int] = Field(default=None, primary_key=True)
    # topic: str
    # title: str 
    # description: str
    # source: str
    # tags: List[str] = Field(sa_column=JSON)
    # licenses: List[str] = Field(sa_column=JSON)
    # col_names: List[str] = Field(sa_column=JSON)
    # row_count: int
    # col_count: int
    # percent_null: float 
    # usability: float
# Extract metadata and output
datasets_to_upload = []
problem_files = []

for filename in INPUT_FILES:

    try:
        # READ METADATA TO MODEL
        path = os.path.join(FILE_INPUT_PATH, filename)

        if path[len(path) - 5:] != '.json':
            continue
        
        file = open(path, 'r')

        dataset_dict = json.load(file)

        dataset = create_model_from_dict(dataset_dict)

        datasets_to_upload.append(dataset)


    except Exception as e:
        problem_files.append(filename)
        print(e)


with open("problem-files-upload.txt", "w+") as newfile:
    newfile.write(json.dumps(problem_files))
print("Found ", len(problem_files), " problem files. Look at problem-files-upload.txt for a list.")

    
# Upload datasets
create_datasets(datasets_to_upload)
