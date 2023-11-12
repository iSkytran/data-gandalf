import os, shutil, json
from data_fetching.kaggle_extractor import KaggleExtractor

TEST_DATA_PATH = os.path.join('tests', 'test_files', 'datasets')
TEST_OUTPUT_PATH = os.path.join('tests', 'test_files', 'metadata')

# Clear old test output
if os.path.exists(TEST_OUTPUT_PATH):
    shutil.rmtree(TEST_OUTPUT_PATH)

os.makedirs(TEST_OUTPUT_PATH)

extractor = KaggleExtractor(file_input_path=TEST_DATA_PATH, file_output_path=TEST_OUTPUT_PATH)

# Academics has no invalid files but has some null values.
def test_extract_academics():

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

# Finance has no null values or problematic files.
def test_extract_finance():

    # Extract metadata 
    topics = ["finance"]
    extractor.extract_topics(topics)

    # Load output
    income_output_file = open(os.path.join(TEST_OUTPUT_PATH, 'finance', 'income_metadata.json'))
    income_dict = json.load(income_output_file)

    # Assert expectations
    assert income_dict['col_count'] == 3
    assert income_dict['col_names'] == ["ID", "Age", "Income"]
    assert income_dict['description'] == "A dataset about income"
    assert len(income_dict['licenses']) == 2
    assert income_dict['licenses'][0]['name'] == "Test License 3"
    assert income_dict['licenses'][1]['name'] == "Test License 4"
    assert income_dict['null_count'] == 0
    assert income_dict['num_entries'] == 27
    assert income_dict['row_count'] == 9
    assert income_dict['source'] == "kaggle"
    assert len(income_dict['tags']) == 2
    assert income_dict['tags'][0] == "finance"
    assert income_dict['tags'][1] == "income"
    assert income_dict['title'] == "income"
    assert income_dict['topic'] == "finance"
    assert income_dict['usability'] == 0.298462346364

# Energy has an invalid CSV file and a broken JSON file, as well as valid files of each. 
def test_extract_energy():
    
    # Extract metadata 
    topics = ["energy"]
    extractor.extract_topics(topics)

    # Load output
    energy_output_file = open(os.path.join(TEST_OUTPUT_PATH, 'energy', 'energy_metadata.json'))
    energy_dict = json.load(energy_output_file)

    # Assert expectations
    assert energy_dict['col_count'] == 2
    assert energy_dict['col_names'] == ["installation", "watts"]
    assert energy_dict['description'] == "A dataset about energy"
    assert len(energy_dict['licenses']) == 2
    assert energy_dict['licenses'][0]['name'] == "Test License 5"
    assert energy_dict['licenses'][1]['name'] == "Test License 6"
    assert energy_dict['null_count'] == 0
    assert energy_dict['num_entries'] == 4
    assert energy_dict['row_count'] == 2
    assert energy_dict['source'] == "kaggle"
    assert len(energy_dict['tags']) == 0
    assert energy_dict['title'] == "energy"
    assert energy_dict['topic'] == "energy"
    assert energy_dict['usability'] == 0.45


# Energy has a broken JSON file (no title) and no csv files.
def test_extract_healthcare():
    
    # Extract metadata 
    topics = ["healthcare"]

    try:
        extractor.extract_topics(topics)
        assert False
    except Exception as e:
        assert True