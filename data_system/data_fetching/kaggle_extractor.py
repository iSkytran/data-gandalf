import os, json

import pandas as pd
from data_fetching.extractor_interface import MetadataExtractor


class KaggleExtractor(MetadataExtractor):
    def __init__(self, file_input_path, file_output_path, source):
        self.file_output_path = file_output_path
        self.source = source

        super().__init__(file_input_path)

    def extract_topic(self, topic):
        return super().extract_topic(topic)

    # Extract a single dataset from a folder of CSVs and JSON.
    def extract_from_dataset(self, dataset_folder, topic) -> dict:
        metadata:dict = {}
        for filename in os.listdir(dataset_folder):
            try:
                # If CSV, run pandas analysis
                if filename[len(filename) - 4:] == '.csv':
                    file = os.path.join(dataset_folder, filename)
                    df = pd.read_csv(file, encoding='unicode_escape')
                    metadata = self.update_metadata_from_df(df, metadata)
                
                # If JSON, take relevant metadata
                elif filename[len(filename) - 5:] == '.json':
                    file = open(os.path.join(dataset_folder, filename), 'r')
                    given_metadata = json.load(file)
                    metadata['source'] = self.source
                    metadata['topic'] = topic
                    metadata['usability'] = given_metadata['usabilityRating']
                    metadata['title'] = given_metadata['title']
                    metadata['description'] = given_metadata['description']
                    metadata['tags'] = given_metadata['keywords']
                    metadata['licenses'] = given_metadata['licenses']
                # Otherwise, ignore
                else:
                    continue
            except Exception as e:
                print(e)
                self.problem_files.append(filename)
        self.datasets_processed.append(metadata['title'])
        return metadata
    
    # Output metadata to a target file.
    def output_data(self, metadata, target_folder, filename):
        
        full_folder_path:str = os.path.join(self.file_output_path, target_folder)

        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
        
        full_path = os.path.join(full_folder_path, filename)

        meta_json:json = json.dumps(metadata, indent=4, sort_keys=True)
        
        with open(full_path, "w+") as newfile:
            newfile.write(meta_json)

    # Updates metadata dict from a dataframe (one data file).
    def update_metadata_from_df(self, df: pd.DataFrame, metadata: dict) -> dict:
        # Compute Values
        null_count:int = int(df.isnull().sum().sum()) 
        metadata['null_count'] = null_count + metadata.get('null_count', 0)

        num_entries:int = df.size
        metadata['num_entries'] = num_entries + metadata.get('num_entries', 0)

        row_count:int = df.shape[0]
        metadata['row_count'] = row_count + metadata.get('row_count', 0)

        col_count:int = df.shape[1]
        metadata['col_count'] = col_count + metadata.get('col_count', 0)

        col_names:list[str] = df.columns.tolist()
        if 'col_names' not in metadata:
            metadata['col_names'] = col_names

        for name in col_names:
            if not name in metadata['col_names']:
                metadata['col_names'].append(name)

        return metadata

    # Reports any issues. 
    def report_issues(self):  
        # Report issues
        with open("problem-files.txt", "w+") as newfile:
            newfile.write(json.dumps(self.problem_files))
        print("Processed", len(self.datasets_processed), "datasets.")
        print("Found", len(self.problem_files), "problem files. Look at problem-files.txt for a list.")



