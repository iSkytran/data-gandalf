import os, json

import pandas as pd

# Get files or file path
FILE_INPUT_PATH = "datasets"
FILE_OUTPUT_PATH = "metadata"

if not os.path.exists(FILE_OUTPUT_PATH):
    os.makedirs(FILE_OUTPUT_PATH)

# Extract metadata dict from a dataframe
def extract_metadata(df: pd.DataFrame) -> dict:
    metadata = {}
    
    # Compute Values
    percent_null = df.isnull().sum().sum() * 100 / len(df)
    metadata['percent_null'] = percent_null

    row_count = df.shape[0]
    metadata['row_count'] = row_count

    col_count = df.shape[1]
    metadata['col_count'] = col_count

    metadata['topic'] = ''
    metadata['description'] = ''
    metadata['tags'] = []
    metadata['licenses'] = []

    return metadata

    # id: Optional[int] = Field(default=None, primary_key=True)
    # topic: str
    # title: str 
    # description: str
    # tags: List[str] = Field(sa_column=JSON)
    # licenses: List[str] = Field(sa_column=JSON)
    # percent_null: float 
    # row_count: int
    # col_count: int

# Print from metadata to JSON file
def print_metadata_to_file(metadata, filename):
    full_path = os.path.join(FILE_OUTPUT_PATH, filename)
    print("Processing", full_path)

    meta_json = json.dumps(metadata, indent=4, sort_keys=True)

    with open(full_path, "w+") as newfile:
        newfile.write(meta_json)

# Extract metadata and output
problem_files = []

# Extract metadat from each csv file to JSON
for filename in os.listdir(FILE_INPUT_PATH):
    try:
        # EXTRACT METADATA TO DICTIONARY
        file = os.path.join(FILE_INPUT_PATH, filename)

        if file[len(file) - 4:] != '.csv':
            continue

        # Check if metadata has already been generated
        if os.path.exists(os.path.join(FILE_OUTPUT_PATH, str(filename[:len(filename) - 4] + '_metadata.json'))):
            continue

        df = pd.read_csv(file, encoding='unicode_escape')
        metadata = extract_metadata(df)

        metadata['title'] = filename[:len(filename) - 4]

        # OUTPUT DICTIONARY TO FILE
        print_metadata_to_file(metadata, str(metadata['title'] + '_metadata.json'))

    except Exception:
        print("E")
        problem_files.append(filename)

with open("problem-files.txt", "w+") as newfile:
    newfile.write(json.dumps(problem_files))
print("Found ", len(problem_files), " problem files. Look at problem-files.txt for a list.")
