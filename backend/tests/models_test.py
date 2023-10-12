from backend.models import Dataset

def test_create_dataset():
    dataset_data = {
        "id": 1,
        "topic": "Test Topic",
        "name": "Test Dataset",
        "description": "This is a test dataset.",
        "source": "Test Source",
        "tags": "tag1, tag2",
        "percent_null": 10,
        "column_count": 5,
    }
    
    dataset = Dataset(**dataset_data)

    assert dataset.id is not None
