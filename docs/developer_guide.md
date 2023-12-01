# Data Gandalf Developer Guide

This document serves as a repository of knowledge of how a developer would get up and running with the Data Gandalf application. It also serves as a guide for future development and extensions to the project. This document will be divided up in the different systems that the project consists of. Data Gandalf is divided into three large parts. There is the main web application, a data subsystem, and a model subsystem.

## Main Web Application

The main web application is user facing and allows for browsing all the various datasets. It consists of the database, backend, and frontend. For quick and easy deployment, [Docker](https://www.docker.com/) can be used, and a Docker Compose file [compose.yaml](../compose.yaml) to spin up all all the containers needed. Assuming Docker and Docker Compose are installed, this can be done with

```sh
docker compose up -d
```

### Database

Before the backend can run, a database needs to be running for it to connect to. PostgreSQL is the database that is supported by the project. The database should be populated with the information from [database](../database). The information for a production deployment is in [pg_dump.sql](../database/pg_dump.sql) while [example.sql](../database/example.sql) is for testing purposes.

### Backend

The backend is used for the business logic of main web application. The code for this resides in the [backend](../backend) folder. All the backend needs to run is a version of [Python 3](https://www.python.org/) and its Python dependencies that are listed in [backend/requirements.txt](../backend/requirements.txt). These dependencies include [FastAPI](https://fastapi.tiangolo.com/) and [Microsoft Recommenders](https://github.com/recommenders-team/recommenders). Assuming the current working directory is [backend](../backend), these dependencies can be installed with

```sh
python3 -m pip install -r requirements.txt
```

The backend can then be run with

```sh
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

The backend unit tests are implemented using [pytest](https://docs.pytest.org/) with the [pytest-cov](https://pytest-cov.readthedocs.io/) plugin for coverage. To run these tests, enter

```sh
python3 -m pytest --cov=backend --cov-branch tests -rA
```

The following subsections will delve into the details of the files that comprise the backend.

#### [backend/backend/config.py](../backend/backend/config.py)

This file holds global constants that are used to configure the backend. Some of these configuration values can be overridden using environment variables.

#### [backend/backend/db.py](../backend/backend/db.py)

This file contains functions that can be called to complete CRUD operations with the PostgreSQL database.

#### [backend/backend/main.py](../backend/backend/main.py)

This is the entrypoint to the backend and where the application starts off from. Inside this file is a list of FastAPI REST endpoints that can reached by the frontend. New REST endpoints can be added here by simply adding an annotated function.

#### [backend/backend/models.py](../backend/backend/models.py)

This file contains the [Pydantic](https://docs.pydantic.dev/) schemes used by the REST API for the POST endpoints.

#### [backend/backend/recommender.py](../backend/backend/recommender.py)

This file contains the logic to load in a recommendation model from a serialized file. The model can be called to perform rankings on datasets.

#### [backend/models](../backend/models)

This folder contains the serialized models used for ranking.

#### [backend/tests](../backend/tests)

This folder contains the corresponding unit test code for the backend.

#### [backend/Dockerfile](../backend/Dockerfile)

This file is used to build a container for the backend.

### Frontend

The frontend uses [React](https://react.dev/) and the [Next.js](https://nextjs.org/) frameworks to render a web page using the data from the backend. The code for the frontend resides is the [frontend](../frontend) folder. In order to run the frontend, Node 20 or later must be installed. The dependencies are listed in [frontend/package.json](../frontend/package.json). Assuming the current working directory is [frontend](../frontend), these dependencies can be installed with

```sh
npm install
```

The frontend can then be run with

```sh
npm run dev
```

The frontend end-to-end tests are implemented using [Playwright](https://playwright.dev/). To run these tests, enter

```sh
npx playwright test
```

To run the tests in UI mode, the `--ui` flag can be added.

```sh
npx playwright test --ui
```

The following subsections will delve into the details of the files that comprise the frontend.

#### [frontend/.github/workflows/playwright.yml](../frontend/.github/workflows/playwright.yml)

This file contains the GitHub actions to run the Playwright system tests on pushes to main as well as pull requests to main.

#### [frontend/app](../frontend/app)

This folder contains all of the React code that makes up the frontend. Adding pages to the web application can be done here. In addition to two subfolders, it includes the following files:

* [globals.css](../frontend/app/globals.css): A CSS file defining the global style for the web application.
* [layout.tsx](../frontend/app/layout.tsx): React code applied to all pages in Data Gandalf.
* [page.tsx](../frontend/app/page.tsx): The homepage for Data Gandalf.
* [utilities.tsx](../frontend/app/utilities.tsx): A bundle of useful TypeScript functions.

##### [frontend/app/components](../frontend/app/components)

This folder contains reusable React code that can be used for the various pages. More components can be added here. It includes the following files:

* [filterBar.tsx](../frontend/app/components/filterBar.tsx): A component for filtering datasets.
* [grid.tsx](../frontend/app/components/grid.tsx): A wrapper component for grid items.
* [gridItem.tsx](../frontend/app/components/gridItem.tsx): A component for displaying a single dataset in the grid.
* [gridItemLarge.tsx](../frontend/app/components/grildItemLarge.tsx): A component for showing a lot of data about a dataset.
* [loadingIcon.tsx](../frontend/app/components/loadingIcon.tsx): A component containing an SVG for loading.
* [rating.tsx](../frontend/app/components/rating.tsx): A component for users to rate recommendations.

##### [frontend/app/dataset/[dataset]/page.tsx](../frontend/app/dataset/[dataset]/page.tsx)

This is a dynamic route, a page whose path is determined at runtime, that displays info about a specific dataset and gives recommendations related to that dataset.

#### [frontend/public](../frontend/public)

This folder contains public assets for the web application to use such as favicons.

#### [frontend/tests](../frontend/tests)

This folder contains the Playwright system test cases.

#### [frontend/Dockerfile](../frontend/Dockerfile)

This file is used to build a container for the frontend.

#### [frontend/next.config.js](../frontend/next.config.js)

This file is used to make any configurations to Next.js.

#### [frontend/tailwind.config.ts](../frontend/tailwind.config.ts)

This file is used to make any configurations to Tailwind CSS, the library used to style the web application.

## Data Subsystem

The data subsystem is used by administrators of the system to pull datasets from online sources.

## Model Subsystem

The model subsystem is used by administrators as well to train models from the pulled datasets for the web application to use.
