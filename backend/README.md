# Backend for Data Gandalf

## Running Locally - Linux

In order to run the backend locally, [Python 3.9](https://www.python.org/) will need to be installed. The following steps can then be run to get the backend running.

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

3. Ensure a [PostgreSQL](https://www.postgresql.org/) database is installed and running.

4. Set the location of the PostgreSQL database. This can be done using environment variables. By default this is set to `database:5432` to support Docker Compose. In order to connect to a local database, the value should be `localhost:5432`.

    ```bash
    export DATABASE_ADDRESS="address:port of the database"
    ```

5. Run the server.

    ```bash
    python -m uvicorn backend.main:app --host "0.0.0.0" --port 8080
    ```

## Running with Docker

A PostgreSQL database needs to be running before the backend can be run. This can be done through Docker. `../database/example.sql` should be set to the path of the data that should be preloaded.

```bash
docker run -dit --name database -p 5432:5432 -e POSTGRES_PASSWORD=default -v ../database/example.sql:/docker-entrypoint-initdb.d/example.sql postgres
```

In order to run the backend in a container, Docker needs to be installed and the image needs to be built.

```bash
docker build . -t backend
```

Once built, the container can be run in the background. The `DATABASE_ADDRESS` environment variable can be set to the actual address of the database.

```bash
docker run -dit --name backend -p 8080:8080 -e DATABASE_ADDRESS="localhost:5432" backend
```
