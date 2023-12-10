import pytest
import pickle
import os
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

@pytest.fixture
def mock_ratings():
    return pd.DataFrame({
        'user_session': ['a','a','a','b','b'],
        'recommend': [True, True, True, False, True],
        'source_dataset': [1,2,3,1,2],
        'destination_dataset': [2,1,1,2,1],
        'id': [1,2,3,4,5]
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

# test that shared tags appropriately weigh the similarity scores
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

def assert_key_error(callable):
    try:
        callable()
        raise AssertionError("Expected KeyError but no exception was raised.")
    except KeyError:
        pass  # Expected exception
    except Exception as e:
        raise AssertionError("Unexpected exception: {}".format(e))

def test_realign_ratings(mock_ratings):
    ratings = script.realign_ratings(mock_ratings)
    assert(ratings.loc[(1,2)][0] == (1,1))
    assert_key_error(lambda: ratings.loc[(1,3)])
    assert(ratings.loc[(2,1)][0] == (2,0))
    assert_key_error(lambda: ratings.loc[(2,3)])
    assert(ratings.loc[(3,1)][0] == (1,0))
    assert(ratings.loc[(3,2)][0] == (0,0))

def test_finalized_model(mocker, mock_metadata, mock_ratings):
    model_path = 'test.pkl'
    mocker.patch('training.config.MODEL_PATH', model_path)
    mocker.patch('training.model_training.get_metadata_and_ratings_from_db', 
                 return_value=(mock_metadata,mock_ratings))

    # Create a new model and serialize it
    script.main()
    
    # Deserialize the model then delete it
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    os.remove(model_path)

    assert(len(model) == 3)
    assert(len(model[1]) == 2)
    assert(len(model[2]) == 2)
    assert(len(model[3]) == 2)