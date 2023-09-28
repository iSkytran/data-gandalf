# Backend for Data Gandalf

## Running Locally

In order to run the backend locally, Python 3.11 will need to be installed. The following steps can then be run to get the backend running.

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

3. Run the server.

    ```bash
    python -m uvicorn backend.main:app --host "0.0.0.0" --port 8080
    ```

## Running with Docker

In order to run the backend in a container, Docker needs to be installed and the image needs to be built.

```bash
docker build . -t backend
```

Once built, the container can be run in the background.

```bash
docker run -dit --name backend -p 8080:8080 backend
```

## Data Upload Process

In order to upload data, some fields need to be manually input. 
This process is done through editing JSON. 
Running ```metadata_extractor.py``` will convert each csv file in the datasets folder
 to a JSON file under the metadata folder. 
Then, manually update the necessary fields in the JSON files you want to upload.
Then, run ```metadata_uploader.py``` to upload the JSON representation of the data to the database. 