# Backend for Data Gandalf

## Scripts Setup

In order to run the scripts, Python 3.11 will need to be installed. The following steps can then be run to get the backend running.

1. Create a virtual environment and activate it.

    ```bash
    python -m venv .venv
    . .venv/bin/activate

    WINDOWS:
    .venv\Scripts\activate
    ```

2. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```


## Data Upload Process

In order to upload data, some fields may to be manually input or edited. 
This process is done through editing JSON. 

Running ```data_fetching/run_extractor.py``` will convert each csv file in the datasets folder
to a JSON file under the metadata folder if a CSVToJsonExtractor subclass is used (default). 


Optionally, manually update the necessary fields in the JSON files (under ```metadata```) you want to upload.

Then, run ```data_uploading/run_uploader.py``` to upload the JSON representation of the data to the database if the JsonToDBUploader subclass is used (default). 

## Extractor/Uploader Implementation

Extractor objects should inherit from the MetadataExtractor class in ```data_fetching extractor_interface.py```. The current implementation (CSVToJsonExtractor) uses kaggle, so one apparent use case of this inheritance is supporting different methods of data fetching. Another is testing. 

 We can override the "extract_from_dataset" method to determine how to parse a dataset folder and use the "output_data" method to determine what output means in the given context. Then, update the run_extractor file with the new class and desired configuration (topic folder list, source definition) and run. The script will need to be minimally edited to provide the class with necessary fields. 

 Uploader objects should inhereit from the MetadataUplaoder class in ```data_uploading/uploader_interface.py```. The current implementation (JsonToDB)... (TODO)

 ## Steps for Running Engines
 ### Kaggle
 1. Go to https://www.kaggle.com/docs/api
 2. Register. 
 3. Run ```pip install kaggle``` in the virtual environment. 
 4. Follow steps in https://www.kaggle.com/docs/api?rvi=1 to get authentication token. 

 # Data Gandalf

Data Gandalf is a web application for finding related datasets. The setup instructions to get up and running can be found in the [frontend](./frontend/) and [backend](./backend) folders.

## DB Dump and Load Process

### Prerequisites:
* PostgreSQL and all related CLI are installed (pg_dump, psql) as well as PGAdmin.

### Dump process:
1. Run ```pg_dump -U <username> <database_to_dump> > <dump_filename>.sql```

### Load process:
1. Create an empty database with name <db_name>
2. Run ```psql -U <username> <db_name> < <dump_filename>.sql```
The database should now be populated with correct tables and records.

## Testing
Generate Coverage Report:
```coverage  run --source=data_fetching,data_uploading --omit=data_fetching/run_extractor.py,data_uploading/run_uploader.py -m pytest```

View Coverage Report:
```coverage```