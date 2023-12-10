# import subprocess
import os, json
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
    fixed_directory = os.getcwd()

    # Make some non-csv files and folders, call clean dataset, ensure it's deleted.
    test_dataset_path = os.path.join(TEST_DATA_PATH, 'academics', 'grades1')

    txt_path = os.path.join(test_dataset_path, 'test.txt')
    with open(txt_path, "w+") as newfile:
        newfile.write("TEST FILE")

    folder_path = os.path.join(test_dataset_path, 'nested', 'nested2')
    os.makedirs(folder_path)

    files_in_folder = os.listdir(test_dataset_path)
    assert len(files_in_folder) == 4
    assert sorted(files_in_folder) == sorted(["dataset-metadata.json", "nested", "sample_grades.csv", "test.txt"])

    kaggle.clean_dataset(test_dataset_path)

    files_in_folder = os.listdir(test_dataset_path)

    assert len(files_in_folder) == 2
    assert sorted(files_in_folder) == sorted(["dataset-metadata.json", "sample_grades.csv"])

    os.chdir(fixed_directory)

# Test getting topic URL list given raw kaggle output.
def test_get_topic_url_list():
    fixed_directory = os.getcwd()

    datasets = """title\r\ndescription\r\nurl_parsed this should not be parsed\r\nowi2.()* this should not be parsed"""

    url_list = kaggle.get_topic_urlList(datasets)
    assert len(url_list) == 2
    assert sorted(url_list) == sorted(["url_parsed", "owi2.()*"])

    os.chdir(fixed_directory)

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
        with open('test.csv', "w+") as newfile:
            newfile.write("TEST FILE")
        with open('dataset-metadata.json', "w+") as newfile:
            metadata = dict()
            metadata['title'] = "TEST_TITLE"
            newfile.write(json.dumps(metadata))

    kaggle.pull_dataset = pull_dataset_holder
    kaggle.fixed_directory = os.path.join(os.getcwd(), "tests", "test_files")

    # Test pulling dataset that already exists.
    success = kaggle.process_dataset("/grades1", "academics")
    assert success == False

    # Test pulling new dataset. 
    success = kaggle.process_dataset("/grades_process_dataset", "academics")
    assert success == True

    # Delete Dataset created.
    created_dataset_path = os.path.join(TEST_DATA_PATH, 'academics', 'grades_process_dataset')
    if os.path.exists(created_dataset_path):
        shutil.rmtree(created_dataset_path)
  
    os.chdir(fixed_directory)
