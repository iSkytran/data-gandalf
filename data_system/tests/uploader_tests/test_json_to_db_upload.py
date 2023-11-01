import os, shutil, json
from data_uploading import json_to_db_uploader
from database_connection import db

TEST_METADATA_PATH = os.path.join('tests', 'test_files', 'metadata')

uploader = json_to_db_uploader.JsonToDbUploader(file_input_path=TEST_METADATA_PATH)

datasets = []
def create_datasets_mock(data):
    global datasets
    for d in data:
        datasets.append(d)

def init_mock():
    return

json_to_db_uploader.create_datasets = create_datasets_mock
json_to_db_uploader.init = init_mock

def test_upload():
    global datasets
    uploader.prepare_upload(topics=["academics","energy","finance"])
    uploader.upload()
    issues = uploader.report_issues()
    assert issues == 0
    assert len(datasets) == 3
    assert datasets[0].title == "Grades"
    assert datasets[1].title == "energy"
    assert datasets[2].title == "Income"