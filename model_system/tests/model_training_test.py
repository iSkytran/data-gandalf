import pytest
from pytest_mock import mocker
import training.model_training as script
from pathlib import Path
import pandas as pd
import copy

@pytest.fixture
def mock_metadata():
    return pd.DataFrame({
        'id': [1,2,3],
        'topic': ['sports','medical','sports'],
        'title': ['EPL Winners','MCAT Scores','Superbowl Winners'],
        'description': ['Winners of the EPL','Winners of the MCAT Exam','Winners of the annual NFL Superbowl'],
        'licenses': ['LicenseA', 'LicenseA', 'LicenseB'],
        'tags': [r'{A,B,C}',r'{C,D,"Test WhItESpAcE"}',r'{A,D,"Test Whitespace"}'],
        'col_names': [r'{1,2,3}',r'{4,"5 and 6"}',r'{1,2,3,4}']
    }).copy()

def test_get_metadata_from_db_error(mocker):
    mocker.patch('training.config.HOST', "BAD_HOST")
    assert(script.get_metadata_and_ratings_from_db() == (None,None))

def test_build_rec_matrix(mock_metadata):
    rec_matrix = script.build_rec_matrix(mock_metadata)
    assert(rec_matrix is not None)

# test that if all weights are one, similarity scores do not change
def test_tune_rec_matrix_no_weights(mock_metadata,mocker):
    rec_matrix = script.build_rec_matrix(mock_metadata)
    mocker.patch('training.config.LICENSES_WEIGHT', 1)
    mocker.patch('training.config.TAGS_WEIGHT', 1)
    mocker.patch('training.config.COLUMN_NAMES_WEIGHT', 1)

    tuned_rec_matrix = script.tune_rec_matrix(rec_matrix,mock_metadata,None)
    assert(tuned_rec_matrix == rec_matrix)

# # test that shared tags appropriately weigh the similarity scores
def test_tune_rec_matrix_tags(mock_metadata,mocker):
    weight = 2
    mocker.patch('training.config.LICENSES_WEIGHT', 1)
    mocker.patch('training.config.TAGS_WEIGHT', weight)
    mocker.patch('training.config.COLUMN_NAMES_WEIGHT', 1)

    rec_matrix = script.build_rec_matrix(mock_metadata)
    tuned_rec_matrix = script.tune_rec_matrix(copy.deepcopy(rec_matrix),mock_metadata,None)

    old_rec_from_1_to_3 = next((rec for rec in rec_matrix[1] if rec[1] == 3), None)[0]
    new_rec_from_1_to_3 = next((rec for rec in tuned_rec_matrix[1] if rec[1] == 3), None)[0]
    assert(new_rec_from_1_to_3 == weight * old_rec_from_1_to_3)

    old_rec_from_2_to_3 = next((rec for rec in rec_matrix[2] if rec[1] == 3), None)[0]
    new_rec_from_2_to_3 = next((rec for rec in tuned_rec_matrix[2] if rec[1] == 3), None)[0]
    assert(new_rec_from_2_to_3 == weight ** 2 * old_rec_from_2_to_3)

    old_rec_from_1_to_2 = next((rec for rec in rec_matrix[1] if rec[1] == 2), None)[0]
    new_rec_from_1_to_2 = next((rec for rec in tuned_rec_matrix[1] if rec[1] == 2), None)[0]
    assert(new_rec_from_1_to_2 == weight * old_rec_from_1_to_2)

# def test_tune_rec_matrix_main(mock_metadata,mocker):
#     mocker.patch('training.config.MODEL_PATH', "//////")
#     mocker.patch("training.model_training.get_metadata_from_db", return_value = mock_metadata)
#     mocker.patch('training.config.LICENSES_WEIGHT', 1)
#     mocker.patch('training.config.TAGS_WEIGHT', weight)
#     mocker.patch('training.config.COLUMN_NAMES_WEIGHT', 1)
#     assert(True)

def test_tune_rec_matrix_path_error(mocker):
    mocker.patch('training.config.MODEL_PATH', "//////")
    with pytest.raises(SystemExit) as excinfo:
        script.main()
    assert excinfo.value.code != 0

def test_rating_weight():
    # More ratings should have a stronger influence on weight
    assert(script.rating_weight(1,0) < script.rating_weight(2,0))
    assert(script.rating_weight(0,1) > script.rating_weight(0,2))
    assert(script.rating_weight(10,1) < script.rating_weight(100,10))
    assert(script.rating_weight(1,10) > script.rating_weight(10,100))
    assert(script.rating_weight(0,0) == 1)
    assert(script.rating_weight(50,50) == 1)

    print(f"\n(1,0) -> {script.rating_weight(1,0)}")
    print(f"\n(2,0) -> {script.rating_weight(2,0)}")
    print(f"\n(3,0) -> {script.rating_weight(3,0)}")
    print(f"\n(0,1) -> {script.rating_weight(0,1)}")
    print(f"\n(0,2) -> {script.rating_weight(0,2)}")
    print(f"\n(0,3) -> {script.rating_weight(0,3)}")
    print(f"\n(100,10) -> {script.rating_weight(100,10)}")
    print(f"\n(10,1) -> {script.rating_weight(10,1)}")
    print(f"\n(10,100) -> {script.rating_weight(10,100)}")
    print(f"\n(1,10) -> {script.rating_weight(1,10)}")