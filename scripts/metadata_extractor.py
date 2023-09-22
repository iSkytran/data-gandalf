import os, json
from db import init, get_all

import pandas as pd

# Get files or file path
FILE_INPUT_PATH = "datasets"
FILE_OUTPUT_PATH = "metadata"

if not os.path.exists(FILE_OUTPUT_PATH):
    os.makedirs(FILE_OUTPUT_PATH)

# Extract metadata dict from a dataframe
def get_metadata_from_df(df):
    metadata = {}
    
    # Compute Values
    percent_null = df.isnull().sum().sum() * 100 / len(df)
    metadata['percent_null'] = percent_null

    row_count = df.shape[0]
    metadata['row_count'] = row_count

    col_count = df.shape[1]
    metadata['col_count'] = col_count

    return metadata

def print_metadata_to_file(metadata, filename):
    full_path = os.path.join(FILE_OUTPUT_PATH, filename)
    print(full_path)

    meta_json = json.dumps(metadata)

    with open(full_path, "w+") as newfile:
        newfile.write(meta_json)
    

# Extract metadata and output
problem_files = []

for filename in os.listdir(FILE_INPUT_PATH):
    try:
        # EXTRACT METADATA
        file = os.path.join(FILE_INPUT_PATH, filename)

        if file[len(file) - 4:] != '.csv':
            continue

        df = pd.read_csv(file, encoding='unicode_escape')
        metadata = get_metadata_from_df(df)

        metadata['title'] = filename[:len(filename) - 4]

        # OUTPUT METADATA TO FILE
        print_metadata_to_file(metadata, str(metadata['title'] + '_metadata.json'))
    except Exception:
        problem_files.append(filename)

with open("problem-files.txt", "w+") as newfile:
    newfile.write(json.dumps(problem_files))
print("Found ", len(problem_files), " problem files. Look at problem-files.txt for a list.")

# init()

# get_all()