import os, json

import pandas as pd

# Get files or file path
TOPIC = "academics"
SOURCE = "kaggle"
FILE_INPUT_PATH = "datasets/" + TOPIC
FILE_OUTPUT_PATH = "metadata/" + TOPIC

datasets_processed = []
problem_files = []

if not os.path.exists(FILE_OUTPUT_PATH):
    os.makedirs(FILE_OUTPUT_PATH)

# Extract metadata dict from a dataframe
def update_metadata_from_df(df: pd.DataFrame, metadata:dict) -> dict:
    # Compute Values
    null_count = int(df.isnull().sum().sum()) 
    metadata['null_count'] = null_count + metadata.get('null_count', 0)

    num_entries = df.size
    metadata['num_entries'] = num_entries + metadata.get('num_entries', 0)

    row_count = df.shape[0]
    metadata['row_count'] = row_count + metadata.get('row_count', 0)

    col_count = df.shape[1]
    metadata['col_count'] = col_count + metadata.get('col_count', 0)

    col_names = df.columns.tolist()
    if 'col_names' not in metadata:
        metadata['col_names'] = col_names

    for name in col_names:
        if not name in metadata['col_names']:
            metadata['col_names'].append(name)

    return metadata

# Extract metadata from a folder representing a dataset
def extract_metadata_from_folder(folder_path: str):
    global problem_files, datasets_processed
    metadata = {}
    for filename in os.listdir(folder_path):
        try:
            if filename[len(filename) - 4:] == '.csv':
                file = os.path.join(folder_path, filename)
                df = pd.read_csv(file, encoding='unicode_escape')
                metadata = update_metadata_from_df(df, metadata)
            elif filename[len(filename) - 5:] == '.json':
                file = open(os.path.join(folder_path, filename), 'r')
                given_metadata = json.load(file)
                metadata['source'] = SOURCE
                metadata['topic'] = TOPIC
                metadata['usability'] = given_metadata['usabilityRating']
                metadata['title'] = given_metadata['title']

                metadata['description'] = given_metadata['description']
                metadata['tags'] = given_metadata['keywords']
                metadata['licenses'] = given_metadata['licenses']
            else:
                continue
        except Exception as e:
            print(e)
            problem_files.append(filename)
    datasets_processed.append(metadata['title'])
    return metadata

# Print from metadata to JSON file
def print_metadata_to_file(metadata, filename):
    full_path = os.path.join(FILE_OUTPUT_PATH, filename)
    meta_json = json.dumps(metadata, indent=4, sort_keys=True)
    
    with open(full_path, "w+") as newfile:
        newfile.write(meta_json)


# Extract metadata from each csv file to JSON
# Iterate over dataset folders
for dataset_folder in os.listdir(FILE_INPUT_PATH):
    # Iterate over dataset
    dataset_path = os.path.join(FILE_INPUT_PATH, dataset_folder)
    metadata = extract_metadata_from_folder(dataset_path)
    print_metadata_to_file(metadata, str(metadata['title'] + '_metadata.json'))
 

with open("problem-files.txt", "w+") as newfile:
    newfile.write(json.dumps(problem_files))
print("Processed", len(datasets_processed), "datasets.")
print("Found", len(problem_files), "problem files. Look at problem-files.txt for a list.")
