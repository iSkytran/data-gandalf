# Backend for Data Gandalf

## Running Locally

In order to run the backend locally, Python 3.9 will need to be installed. The following steps can then be run to get the backend running.

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
