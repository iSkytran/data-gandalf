# import subprocess
import os
from zipfile import ZipFile
import shutil
from data_fetching import kaggle

TEST_DATA_PATH = os.path.join('tests', 'test_files', 'datasets')
TEST_OUTPUT_PATH = os.path.join('tests', 'test_files', 'metadata')

# Clear old test output
if os.path.exists(TEST_OUTPUT_PATH):
    shutil.rmtree(TEST_OUTPUT_PATH)

os.makedirs(TEST_OUTPUT_PATH)

# Test clean dataset functionality. Deletes all non-csv and non-json files and folders.
def test_clean_dataset():
    # Make some non-csv files and folders, call clean dataset, ensure it's deleted.
    test_dataset_path = os.path.join(TEST_DATA_PATH, 'academics', 'grades1')

    txt_path = os.path.join(test_dataset_path, 'test.txt')
    with open(txt_path, "w+") as newfile:
        newfile.write("TEST FILE")

    folder_path = os.path.join(test_dataset_path, 'nested', 'nested2')
    os.makedirs(folder_path)

    files_in_folder = os.listdir(test_dataset_path)
    assert len(files_in_folder) == 4
    assert files_in_folder == ["dataset-metadata.json", "nested", "sample_grades.csv", "test.txt"]

    kaggle.clean_dataset(test_dataset_path)

    files_in_folder = os.listdir(test_dataset_path)

    assert len(files_in_folder) == 2
    assert files_in_folder == ["dataset-metadata.json", "sample_grades.csv"]

# Test getting topic URL list given raw kaggle output.
def test_get_topic_url_list():
    datasets = """title\r\ndescription\r\nurl_parsed this should not be parsed\r\nowi2.()* this should not be parsed"""

    url_list = kaggle.get_topic_urlList(datasets, "topic")
    assert len(url_list) == 2
    assert url_list == ["url_parsed", "owi2.()*"]

def test_ensure_data_exists():
    test_dataset_path = os.path.join(TEST_DATA_PATH, 'academics', 'grades1')
    assert kaggle.ensure_data_exists(test_dataset_path) == True
    assert kaggle.ensure_data_exists(TEST_DATA_PATH) == False

def test_process_dataset():
    fixed_directory = os.getcwd()

    # Deletes folder if created in past run.
    test_dataset_path = os.path.join(TEST_DATA_PATH, 'academics', 'grades_process_dataset')
    if os.path.exists(test_dataset_path):
        shutil.rmtree(test_dataset_path)

    # Simulates pulling a dataset, by creating a folder with a csv and json.
    def pull_dataset_holder(link):
        print(os.getcwd())
        with open('test.csv', "w+") as newfile:
            newfile.write("TEST FILE")
        with open('test.json', "w+") as newfile:
            newfile.write("TEST FILE")

    kaggle.pull_dataset = pull_dataset_holder
    kaggle.fixed_directory = os.path.join(os.getcwd(), "tests", "test_files")

    # Test pulling dataset that already exists.
    success = kaggle.process_dataset("/grades1", "academics")
    assert success == False

    os.chdir(fixed_directory)

    # Test pulling new dataset. 
    success = kaggle.process_dataset("/grades_process_dataset", "academics")
    assert success == True
  
    os.chdir(fixed_directory)

# # Pulls a dataset from kaggle with a given link.
# def pull_dataset(link):
#     subprocess.run(f'kaggle datasets download -d {link}')
#     subprocess.run(f'kaggle datasets metadata {link}')

# # Pull a dataset with a given link from kaggle, then validates it.
# def process_dataset(link, topic):
#     global fixed_directory
#     path = os.path.join(fixed_directory, "datasets", topic)
#     os.chdir(path)

#     # NOTE: URL is kaggle.com/datasets/{link}
#     try:
#         # Pull Dataset
#         name = link[link.rindex('/') + 1:]
#         folder = os.path.join(os.getcwd(), name)
#         if os.path.exists(folder):
#             raise Exception("Dataset already pulled.")
#         os.makedirs(folder)
#         os.chdir(folder)

#         pull_dataset(link)
  
#         os.chdir(path)

#         # Clean Dataset Folder
#         clean_dataset(folder)  

#         data_exists = ensure_data_exists(folder)
#         if not data_exists:
#             shutil.rmtree(folder)
#             raise Exception("No CSV files detected in", folder)

#         return True
#     except Exception as e:
#         print("Unable to parse url:", link)
#         print(e)
#         return False

# def pull_topic(topic, num_datasets):

#     #Get the string value of all the returned datasets when the list command is run with a max size of 1MB and a given topic search command
#     datasets = subprocess.check_output(f'kaggle datasets list --max-size 1000000 --file-type csv --search \'{topic}\'').decode()


#     path = os.path.join("datasets", topic)
#     if not os.path.exists(path):
#         os.makedirs(path)

#     # Get list of all dataset URL suffixes.
#     urlList = get_topic_urlList(datasets, topic)

#     #Download all of the dataset files and metadata into the topic folder
#     successful_pulls = 0
#     idx = 0
#     while idx < len(urlList) and successful_pulls < num_datasets:
#         u = urlList[idx]
#         if pull_dataset(u, topic):
#             successful_pulls += 1
#                 # If doesn't have CSV, delete it
#         idx += 1

# def fetch(topics, num_datasets, output_folder):
#     global fixed_directory
#     # Fix initial working directory
#     fixed_directory = os.getcwd()

#     #Make a dataset folder to store everything in
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for topic in topics:
#         pull_topic(topic, num_datasets)
#         os.chdir(fixed_directory)
        
#     os.chdir(fixed_directory)
