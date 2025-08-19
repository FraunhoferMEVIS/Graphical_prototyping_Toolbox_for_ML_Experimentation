# KI-FDZ: DATA_DESCRIPTOR

## Running the App

This is the ai sandbox backend.

For this tool, you need a python version of 3.10 or newer.
First, install the requirements by running:

```
pip install -r requirements/requirements_core.txt
```

Then from this folder, run

```
python -m serve
```

The api will be accessible via http://127.0.0.1:8000. For changing the default port, you can define the port in an environment variable names as "DATA_DESCRIPTOR_PORT" or start the app as following, for example, the default port number is changed to 8080:

```
DATA_DESCRIPTOR_PORT="8080" python -m serve
```

<Temporary>: Until creating a new service for the methods_repository, to be able to run the created MLfow projet, you need to add the "methods_repository" to your PYTHONPATH:

```
export PYTHONPATH=${PYTHONPATH}:<path-to-the folder-containing-this-file>
```

## Build Docker

docker build -t fdz_mimic_data_descriptor .
