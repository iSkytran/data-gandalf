import subprocess
import os
from zipfile import ZipFile
import shutil

topic_url_list = {}

def clean_datasets(path):
    # Iterate over datasets
    for d in os.listdir(path):
        directory = os.path.join(path, d)
        if os.path.isdir(directory):
            remove_non_json_non_csv(directory)

            # Check if at least one csv file exists
            path_arr = path.split("/")
            topic = path_arr[len(path_arr) - 1]

def remove_non_json_non_csv(path):
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

# Datasets are output of kaggle datasets list cli call.
def get_topic_urlList(datasets, topic):
    global topic_url_list
    #Split the datasets into a list and remove the headers
    datasetList = datasets.split('\r\n')
    datasetList.pop(0)
    datasetList.pop(0)

    #Get a list of all the dataset URL suffixes
    urlList = []
    for d in datasetList:
        urlList.append(d.split(' ', 1)[0])

    topic_url_list[topic] = urlList
    return urlList

def pull_dataset(link):
    # NOTE: URL is kaggle.com/datasets/{link}
    try:
        name = link[link.rindex('/'):]
        if os.path.exists(os.getcwd() + name):
            raise Exception("Dataset already pulled.")
        os.makedirs(os.getcwd() + name)
        os.chdir(os.getcwd() + name)
        subprocess.run(f'kaggle datasets download -d {link}')
        subprocess.run(f'kaggle datasets metadata {link}')
        os.chdir('..')
        return True
    except Exception as e:
        print("Unable to parse url:", link)
        print(e)
        return False

def pull_topic(topic, num_datasets):

    #Get the string value of all the returned datasets when the list command is run with a max size of 1MB and a given topic search command
    datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --search \'{topic}\'').decode()

    #Make a subfolder for the topic
    if not os.path.exists(topic):
        os.makedirs(topic)
    os.chdir(topic)

    # Get list of all dataset URL suffixes.
    urlList = get_topic_urlList(datasets, topic)

    #Download all of the dataset files and metadata into the topic folder
    successful_pulls = 0
    idx = 0
    while idx < len(urlList) and successful_pulls < num_datasets:
        u = urlList[idx]
        if pull_dataset(u):
            successful_pulls += 1
                # If doesn't have CSV, delete it
        idx += 1
    os.chdir('..')

def fetch(topics, num_datasets, output_folder):
    # Fix initial working directory
    fixed_directory = os.getcwd()

    #Make a dataset folder to store everything in
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    os.chdir(output_folder)

    for topic in topics:
        pull_topic(topic, num_datasets)

    #Unzip all of the dataset folder contents and remove the zip files
    # for each topic folder
    for d in os.listdir(os.getcwd()):
        directory = os.path.join(os.getcwd(), d)
        if os.path.isdir(directory):
            # for each dataset
            clean_datasets(directory)
            
    
    # Reset working directory
    os.chdir(fixed_directory)