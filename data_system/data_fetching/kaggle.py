import subprocess
import os
from zipfile import ZipFile
import shutil

fixed_directory = ""

def clean_dataset(path):
    # for each file
    for f in os.listdir(path):
        file = os.path.join(path, f)
        print("FILE:", file)
        if file.endswith('.zip') == True:
            with ZipFile(file, 'r') as z:
                z.extractall(path)
            os.remove(file)
        if os.path.isfile(file) and file.endswith('.csv') == False and file.endswith('.json') == False:
            os.remove(file)
        if os.path.isdir(file):
            shutil.rmtree(file)


# Datasets are output of kaggle datasets list cli call.
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

def pull_dataset(link, topic):
    global fixed_directory
    path = os.path.join(fixed_directory, "datasets", topic)
    os.chdir(path)

    # NOTE: URL is kaggle.com/datasets/{link}
    try:
        # Pull Dataset
        name = link[link.rindex('/') + 1:]
        folder = os.path.join(os.getcwd(), name)
        if os.path.exists(folder):
            raise Exception("Dataset already pulled.")
        os.makedirs(folder)
        os.chdir(folder)
        subprocess.run(f'kaggle datasets download -d {link}')
        subprocess.run(f'kaggle datasets metadata {link}')
        os.chdir(path)

        # Clean Dataset Folder
        clean_dataset(folder)  

        # Ensure Data is non-empty
        csv = False
        for f in os.listdir(folder):
            file = os.path.join(folder, f)
            if file.endswith('.csv'):
                csv = True
        if not csv:
            shutil.rmtree(folder)
            raise Exception("No CSV files detected in", folder)
        
        return True
    except Exception as e:
        print("Unable to parse url:", link)
        print(e)
        return False

def pull_topic(topic, num_datasets):

    #Get the string value of all the returned datasets when the list command is run with a max size of 1MB and a given topic search command
    datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --search \'{topic}\'').decode()


    path = os.path.join("datasets", topic)
    if not os.path.exists(path):
        os.makedirs(path)

    # Get list of all dataset URL suffixes.
    urlList = get_topic_urlList(datasets, topic)

    #Download all of the dataset files and metadata into the topic folder
    successful_pulls = 0
    idx = 0
    while idx < len(urlList) and successful_pulls < num_datasets:
        u = urlList[idx]
        if pull_dataset(u, topic):
            successful_pulls += 1
                # If doesn't have CSV, delete it
        idx += 1

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
