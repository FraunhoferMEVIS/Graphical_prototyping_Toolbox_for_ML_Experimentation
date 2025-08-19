# Data Preparation

This Service is developed to help the user with preparing the data for machine learning.

## Build Docker

```bash
docker build -t <your-registry>/ki-fdz/data_preparation .
```

## Getting Started

Target Python version: 3.11

#### Install requirements

```bash
pip install -r requirements/requirements_core.txt
pip install -r requirements/requirements_tests.txt
```

#### Start development server

```bash
uvicorn main:app --reload
```

#### Execute tests

Tests in _./tests/modules_repository_ require a running local PostgreSQL instance on port _5432_

1. Build postgres image

```bash
cd tests/modules_repository
docker build -t postgres .
```

2. Run postgres container in background

```bash
sudo docker run -p 5432:5432  -d --name postgres_test -e POSTGRES_DB=mimmiciv -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres
```

3. Execute tests in root directory

```bash
pytest --cov-report html --cov=data_preparation
```

View test coverage report in `htmlcov/index.html`.

Optionally, add `--ignore tests/modules_repository` to skip PostgreSQL integration tests.

## Roadmap

- API for the service
- Network concept
- Define a base class for the modules
- Generate multiple modules that could be added to the network
- Implement the functionality to add/remove/edit modules in the network
- Option for working with the entire dataset or only a subset
- Turn on and off the automatic computation of each module's output
- Session management

## License

[] Add License Here
