# Data Gandalf - Data Subsystem

## Data Workflow
1. Follow instructions in "Setup" section to prepare environment.
2. (Optional) Modify ```main.py``` file with configuration.
Configuration in file contains default values that can be overridden with command-line arguments:

* STAGES: Array containing combination of "FETCH", "EXTRACT", "UPLOAD", defaults to all three. 
* SAVE_CSV: True or False, default False. Whether csv files of downloaded data should be saved. 
* SAVE_METADATA: True or False, default False. Whether metadata files extracted should be saved. Set to True and modify STAGES if you want to manually examine JSON before uploading.
* TOPICS: Array containing list of topic strings. If "FETCH" is in STAGES, specifies which topics to query kaggle for. If "EXTRACT" is in STAGES, specifies which topics (folders in ```datasets/```) to extract metadata from. If "UPLOAD" is in stages, specifies which topics (folders in ```metadata/```) to upload.
* DATASETS_PER_TOPIC: Integer. If "FETCH" is in STAGES, specifies how many datasets to pull from kaggle from each topic.

The command line arguments below are grouped by their effect. If one of the options under a bullet point is included in the command, default settings above from the script file will be completely overridden by the values from the CLI. Any of these can be combined.

* STAGES: -f, -e, -u. If any of these are specified, only the listed stages will be run by the system. To run all stages with otherwise default settings, ```python main.py -f -e -u```
* SAVE_CSV: -c. If included, sets SAVE_CSV to True.
* SAVE_METADATA: -m. If included, sets SAVE_METADATA to True.
* TOPICS: -t {topic1} -t {topic2} --topic {topic3}. If included, overrides default topics. For example, ```python main.py -t sports --topic housing -t academics``` will set TOPICS=["sports", "housing", "academics"].
* DATASETS_PER_TOPIC: -n, --num_datasets. If included,overrides DATASETS_PER_TOPIC. For example, ```python main.py -n 3``` will pull 3 datasets from each default topic.

3. Run ```python main.py``` from ```data_system/```. 
* Data will be pulled from kaggle if "FETCH" is in stages. 
* Data will be analyzed and extracted to JSON if "EXTRACT" is in stages.
* Database will now populate if "UPLOAD" is in STAGES. 
4. (optional) To serialize existing database, view "DB Dump and Load Process" below.

## Setup
### Python 3.9/VENV
In order to run the scripts, Python 3.9 will need to be installed. The following steps can then be run to get the backend running.

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

 ### Kaggle CLI
 These steps are necessary when running the data_fetching component. 

 1. Go to https://www.kaggle.com/docs/api
 2. Register. 
 3. Run ```pip install kaggle``` in the virtual environment. 
 4. Follow steps in https://www.kaggle.com/docs/api?rvi=1 to get authentication token and store on local computer.


## Description/Design
The data subsystem is meant to pull existing datasets from public sources, structure the data, and  upload data to a configured database. 

The system is broadly split into three components:
1. Data Fetching 
2. Metadata Extraction 
3. Data Uploading 

all of which are used in sequence by the ```main.py``` script.

### 1. Data Fetching
The data fetching component (found in ```data_fetching``` folder) uses the kaggle command line interface to pull a configured number of public datasets with a given topic. Each dataset pulled is stored in its own folder in the ```datasets``` folder. Datasets typically contain ```.csv``` files as data and ```.json``` files containing metadata provided by kaggle. 

Files:
* ```data_fetching/kaggle.py```: Provides a "fetch" method to be used publicly by the main script as well as helper methods for itself. Calling fetch(topics, num_datasets, output_folder) will automatically fetch num_datasets datasets for each topic in the topics array and save each pulled dataset to the output_folder. The main script is configured with output_folder=```datasets```, so each dataset will be saved as a ```datasets/{topic}/{dataset_name}``` folder.


### 2. Metadata Extraction 
The metadata extraction component (found in ```data_fetching``` folder) uses Pandas data analysis to gain additional insights about the data pulled. It reads from the ```datasets``` folder (populated by the above component) and outputs to the ```metadata``` folder.

It combines metadata provided by kaggle (title, description, etc.) with this custom-generated metadata (row count, column names, etc.) and outputs a ```.json``` file for each dataset to the ```metadata/{topic}``` folder.

Files:
* ```data_fetching/extractor_interface.py```: Contains MetadataExtractor class. Provides extensible interface currently only implemented by KaggleExtractor in ```data_fetching/kaggle_extractor.py```. In essence, takes a file path containing datasets (pulled from data fetching component) as input and calls the extending class's ```extract_from_dataset``` and ```output_data``` methods to determine how to generate metadata and where to store the metadata. 
* ```data_fetching/kaggle_extractor.py```: Contains KaggleExtractor class that implements MetadataExtractor. Overrides ```extract_from_dataset``` to specify how to convert kaggle datasets into json. Overrides ```output_data``` to specify where and how to store the data (in this case, as JSON in the ```metadata``` folder). 


### 3. Data Uploading
The data uploading component (found in ```data_uploading``` folder) takes metadata generated by the Metadata Extraction component and uploads it to a database configured in ```database_connection/db.py```.
The component is mostly responsible for loading the ```.json``` files and converting them to objects of the Dataset class (```database_connection/models.py```) to work with the SQLModel ORM. However, it also does some small data transformation, like extracting licenses from a nested structure to a simple list. 

Files:
* ```data_uploading/uploader_interface.py```: Contains a MetadataUploader interface-like class for uploading data. Overriding classes must specify how to prepare uploading, how to upload, and how to report issues found uploading.
* ```data_uploading/json_to_db_uploader.py```: Contains a JsonToDbUploader class that extends MetadataUploader. Specifies how to read in metadata generated in Metadata Extraction and how to save it to the database. 



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
Tests exist for each component: kaggle, the extractor, and the uploader. 
### Kaggle Tests:
Kaggle tests don't interact with the Kaggle CLI but instead tests the helper methods used within ```data_fetching/kaggle.py``` to ensure they work. Tested methods:
* clean_dataset() - Ensure only ```.csv``` and ```.json``` files are retained after calling clean_dataset. 
* get_topic_urlList() - Ensure raw output of CLI (generated from sample) is processed correctly, ignoring first two elements and only reading one element (delimited by spaces) from each url.
* ensure_data_exists() - Ensure that this returns true when ```.csv``` files are present and false otherwise.
* process_dataset() - Ensure that datasets are not re-pulled. Ensure that new datasets being pulled result in success messages. Ensure that exceptions are being thrown when datasets are invalid and not when they are valid.

### Extractor Tests:
Extractor tests use fake data from the ```tests/test_files``` folder to test the behavior of the extractor. 
* extract_topics() - Tested on a variety of different file structures representing different pulled datasets. Ensure exceptions are thrown with broken data and data is extracted properly with valid data.

### Uploader Tests:
Uploader tests patch the actual uploading process (to the database), intercepting values to compare them against expected results.
* prepare_upload(), upload() - Tests conversion of ```.json``` to Dataset class objects, using the same fake data as extractor tests in ```tests/test_files```. 

### Running Tests
Run All Tests and Generate Coverage Report:
```coverage  run --source=data_fetching,data_uploading --omit=data_fetching/run_extractor.py,data_uploading/run_uploader.py -m pytest```

View Coverage Report:
```coverage report -m```