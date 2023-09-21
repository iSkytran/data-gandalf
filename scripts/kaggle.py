import subprocess
import os
from zipfile import ZipFile
import shutil

# Data Topics: Sports, Academics, Real Estate, Health, Finance
topics = ['sports', 'academics', 'housing', 'health', 'finance']

for x in range(5):
    #Get the string value of all the returned datasets when the list command is run with a max size of 1MB
    datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --search \'{topics[x]}\'').decode()

    #Split the datasets into a list and remove the headers
    datasetList = datasets.split('\r\n')
    datasetList.pop(0)
    datasetList.pop(0)

    #Get a list of all the dataset URL suffixes
    urlList = []
    for d in datasetList:
        urlList.append(d.split(' ', 1)[0])

    #Download all of the dataset files into the dataset folder
    os.chdir('datasets')
    for u in urlList[:10]:
        subprocess.run(f'kaggle datasets download -d {u}')
    os.chdir('..')

os.chdir('datasets')
#Unzip all of the dataset folder contents and remove the zip files
for f in os.listdir(os.getcwd()):
    with ZipFile(f, 'r') as z:
        z.extractall(os.getcwd())
    os.remove(f)

for f in os.listdir(os.getcwd()):
    if os.path.isfile(f) and f.endswith('.csv') == False:
        os.remove(f)
    if os.path.isdir(f):
        shutil.rmtree(f)