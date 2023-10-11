import os, shutil, json
from data_fetching.kaggle_extractor import KaggleExtractor

TEST_DATA_PATH = os.path.join('tests', 'extractor_tests', 'test_datasets')
TEST_OUTPUT_PATH = os.path.join('tests', 'extractor_tests', 'test_metadata')

# Clear old test output
if os.path.exists(TEST_OUTPUT_PATH):
    shutil.rmtree(TEST_OUTPUT_PATH)

os.makedirs(TEST_OUTPUT_PATH)

extractor = KaggleExtractor(file_input_path=TEST_DATA_PATH, file_output_path=TEST_OUTPUT_PATH)

def test_extract_topics():
    # Extract metadata 
    topics = ["academics"]
    extractor.extract_topics(topics)

    # Load output
    grades_output_file = open(os.path.join(TEST_OUTPUT_PATH, 'academics', 'Grades_metadata.json'))
    grades_dict = json.load(grades_output_file)

    # Assert expectations
    assert grades_dict['col_count'] == 3
    assert grades_dict['col_names'] == ["ID", "Age", "Grade"]
    assert grades_dict['description'] == "A dataset about grades"
    assert len(grades_dict['licenses']) == 2
    assert grades_dict['licenses'][0]['name'] == "Test License 1"
    assert grades_dict['licenses'][1]['name'] == "Test License 2"
    assert grades_dict['null_count'] == 4
    assert grades_dict['num_entries'] == 27
    assert grades_dict['row_count'] == 9
    assert grades_dict['source'] == "kaggle"
    assert len(grades_dict['tags']) == 1
    assert grades_dict['tags'][0] == "academics"
    assert grades_dict['title'] == "Grades"
    assert grades_dict['topic'] == "academics"
    assert grades_dict['usability'] == 0.8235294117647058
