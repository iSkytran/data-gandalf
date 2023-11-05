import subprocess
import json
import os
from zipfile import ZipFile
import shutil

fixed_directory = ""
pulled_links = set()

# Unzip ZIP files, then remove Non-JSON and Non-CSV files.
def clean_dataset(path):
    # for each file
    for f in os.listdir(path):
        file = os.path.join(path, f)
        if file.endswith('.zip') == True:
            with ZipFile(file, 'r') as z:
                z.extractall(path)
            os.remove(file)
        if os.path.isfile(file) and file.endswith('.csv') == False and file.endswith('.json') == False:
            os.remove(file)
        if os.path.isdir(file):
            shutil.rmtree(file)

# Ensure at least one CSV file exists in the directory.
def ensure_data_exists(folder_path):
    # Ensure Data is non-empty
    csv = False
    for f in os.listdir(folder_path):
        file = os.path.join(folder_path, f)
        if file.endswith('.csv'):
            csv = True
    return csv
    
# Given a string represnting datasets (pulled from kaggle), get a topic URL list.
def get_topic_urlList(datasets, topic):
    #Split the datasets into a list and remove the headers
    datasetList = datasets.split('\r\n')
    datasetList.pop(0)
    datasetList.pop(0)

    #Get a list of all the dataset URL suffixes
    urlList = []
    for d in datasetList:
        urlList.append(d.split(' ', 1)[0])

    return urlList

# Pulls a dataset from kaggle with a given link.
def pull_dataset(link):
    subprocess.run(f'kaggle datasets download -d {link}')
    subprocess.run(f'kaggle datasets metadata {link}')

# Pull a dataset with a given link from kaggle, then validates it.
def process_dataset(link, topic):
    global fixed_directory
    path = os.path.join(fixed_directory, "datasets", topic)
    os.chdir(path)

    # NOTE: URL is kaggle.com/datasets/{link}
    try:
        # Pull Dataset
        name = link[link.rindex('/') + 1:]
        folder = os.path.join(os.getcwd(), name)
        if os.path.exists(folder) or link in pulled_links:
            raise Exception("Dataset already pulled.")
        pulled_links.add(link)
        os.makedirs(folder)
        os.chdir(folder)

        # Add link to metadata
        pull_dataset(link)
        metadata = dict()
        with open('dataset-metadata.json', 'r') as file:
            metadata = json.load(file)
            metadata['url'] = "kaggle.com/datasets/" + link
        
        with open('dataset-metadata.json', 'w') as file:
            file.write(json.dumps(metadata))

        os.chdir(path)

        # Clean Dataset Folder
        clean_dataset(folder)  

        data_exists = ensure_data_exists(folder)
        if not data_exists:
            shutil.rmtree(folder)
            raise Exception("No CSV files detected in", folder)

        return True
    except Exception as e:
        print("Unable to parse url:", link)
        print(e)
        return False

def pull_topic(topic, num_datasets):
    # Pessimistically, assume only 15/20 datasets pulled are usable
    pessimistic_pages = round((num_datasets + 14) / 15)


    path = os.path.join("datasets", topic)
    if not os.path.exists(path):
        os.makedirs(path)

    successful_pulls = 0
    try:
        for page in range(1, pessimistic_pages + 1):
            #Get the string value of all the returned datasets when the list command is run with a max size of 1MB and a given topic search command
            datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --page {page} --search \'{topic}\'').decode()

            # Get list of all dataset URL suffixes.
            urlList = get_topic_urlList(datasets, topic)

            #Download all of the dataset files and metadata into the topic folder
            idx = 0

            while idx < len(urlList) and successful_pulls < num_datasets:
                u = urlList[idx]
                if process_dataset(u, topic):
                    successful_pulls += 1
                idx += 1
    except Exception as e:
        print(e)

def fetch(topics, num_datasets, output_folder):
    global fixed_directory
    # Fix initial working directory
    fixed_directory = os.getcwd()

    #Make a dataset folder to store everything in
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for topic in topics:
        pull_topic(topic, num_datasets)
        os.chdir(fixed_directory)

    os.chdir(fixed_directory)
