# DevOps Apprenticeship: The Perfect Productivity Platform

## Getting started

This project has multiple ways of being run (either with Poetry, Docker for Dev or Docker for Prod).

### MongoDB Access
* This application requires a connection to a MongoDB.
* To setup your own, visit https://www.mongodb.com/

### Environment Variables
* Create a file named **.env** at the root directory, with the same layout as **.env.template**.
* Remove the \<change me\> sections and populate values
* in particular:
  * ```MONGO_USERNAME``` and ```MONGO_PASSWORD``` will not be the credentials of your MongoDB account, but rather to a database user you can create in Database Access (can be found in the Security section of the MongoDB portal)
  * ```MONGO_CLUSTER_NAME``` is the name of your cluster (by default this is ```Cluster0```), and ```MONGO_DB_NAME``` will point to the database you wish to use in this cluster.

### Run with Docker (Using Flask for Development)
```bash
$ docker-compose up
```
### Run with Docker (Using Gunicorn for Production)
```bash
$ docker build --target production --no-cache --tag todo-app:prod .
$ docker run -p 5000:5000 --env-file .env todo-app:prod
```
### Run with Poetry (With Python3 installed)
First, download poetry and install dependencies:
```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
$ poetry install
```

Once the all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

### Viewing in Browser
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running Tests

### Test Environment Variables
Create a **.env.test** in the /tests directory with the same field names as the **.env** file, but with appropriate amendments.
### Run with Docker (Using Pytest)
```
docker build --target test --tag my-test-image .
docker run --env-file tests/.env.test my-test-image tests
docker run --env-file .env my-test-image tests_e2e
```

### Download Geckodriver (for End-to-End tests)
You will need to download [geckodriver v0.27.0](https://github.com/mozilla/geckodriver/releases/tag/v0.27.0), and place the geckodriver.exe file at the root directory.

### Running Tests (using Poetry)
We'll be using [pytest](https://pypi.org/project/pytest/) to execute the test files. The pytest package will be installed when executing `poetry install` (see Run with Poetry above).

To run tests, execute the following at the root
```bash
poetry run pytest
```

### Adding Tests

To make sure pytest can detect additional test files, make sure:
* the filename is of the form `test_*.py` or `*_test.py`
* the test methods are prefixed with `test`

## CI/CD Pipeline

This repository uses Travis to build docker images and run tests on both PR branches and master. Any master builds that succeed will automatically deploy to Azure (link to the site [here](https://prod-perfect-productivity-platform.azurewebsites.net))

## Infrastructure (Terraform)

This repository uses Terraform to manage its infrastructure. Any changes in terraform files will be applied to Azure resources automatically when you merge branches into `master`.

If you need to handle changes locally, you can download the [Terraform CLI](https://www.terraform.io/downloads.html).
Basic commands can be learnt [here](https://www.terraform.io/docs/cli/commands/index.html).