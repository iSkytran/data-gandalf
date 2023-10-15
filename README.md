# Data Gandalf

Data Gandalf is a web application for finding related datasets. The setup instructions to get up and running can be found in the [frontend](./frontend/) and [backend](./backend) folders.

## System Requirements

In order to run Data Gandalf, it is recommended to run the system using [Docker](https://www.docker.com/).

## Running the Whole System

The system can deployed using the Docker Compose command. This will build the Docker images and run the containers as well.

```bash 
docker compose up -d
```

## Running Individual Components

The `compose.yaml` should work out of the box and deploy the whole system, but individual parts of the system can be run independently if desired. Additional instructions can be read in the following files:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend/README.md)

