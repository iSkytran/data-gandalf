# Frontend for Data Gandalf

## Running Locally

In order to run the backend locally, Node will need to be installed. The following steps can then be run to get the frontend running.

1. Install the dependencies.

    ```bash
    npm install
    ```

2. Run the frontend. This will run in development mode.

    ```bash
    npm dev
    ```

3. Access the webpage though [127.0.0.1:3000](127.0.0.1:3000).

## Running with Docker

1. In order to run the backend in a container, Docker needs to be installed and the image needs to be built.

    ```bash
    docker build . -t frontend
    ```

2. Once built, the container can be run in the background. This will run in production mode.

    ```bash
    docker run -dit --name frontend -p 3000:3000 frontend
    ```

3. The webpage can then be accessed at [127.0.0.1:3000](127.0.0.1:3000).
