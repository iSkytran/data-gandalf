import subprocess
import os
from zipfile import ZipFile
import shutil

def fetch(topics, output_folder):
    # Fix initial working directory
    fixed_directory = os.getcwd()

    #Make a dataset folder to store everything in
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    os.chdir(output_folder)

    for topic in topics:
        #Get the string value of all the returned datasets when the list command is run with a max size of 1MB and a given topic search command
        datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --search \'{topic}\'').decode()

        #Make a subfolder for the topic
        if not os.path.exists(topic):
            os.makedirs(topic)
        os.chdir(topic)

        #Split the datasets into a list and remove the headers
        datasetList = datasets.split('\r\n')
        datasetList.pop(0)
        datasetList.pop(0)

        #Get a list of all the dataset URL suffixes
        urlList = []
        for d in datasetList:
            urlList.append(d.split(' ', 1)[0])

        #Download all of the dataset files and metadata into the topic folder
        for u in urlList[:10]:
            try:
                name = u[u.rindex('/'):]
                if not os.path.exists(os.getcwd() + name):
                    os.makedirs(os.getcwd() + name)
                os.chdir(os.getcwd() + name)
                subprocess.run(f'kaggle datasets download -d {u}')
                subprocess.run(f'kaggle datasets metadata {u}')
                os.chdir('..')
            except Exception as e:
                print("Unable to parse url:", u)
        os.chdir('..')

    #Unzip all of the dataset folder contents and remove the zip files
    for d in os.listdir(os.getcwd()):
        if os.path.isdir(d):
            os.chdir(d)
            for d in os.listdir(os.getcwd()):
                if os.path.isdir(d):
                    os.chdir(d)
                    for f in os.listdir(os.getcwd()):
                        if f.endswith('.zip') == True:
                            with ZipFile(f, 'r') as z:
                                z.extractall(os.getcwd())
                            os.remove(f)
                    for f in os.listdir(os.getcwd()):
                        if os.path.isfile(f) and f.endswith('.csv') == False and f.endswith('.json') == False:
                            os.remove(f)
                        if os.path.isdir(f):
                            shutil.rmtree(f)
                    os.chdir('..')
            os.chdir('..')
    
    # Reset working directory
    os.chdir(fixed_directory)