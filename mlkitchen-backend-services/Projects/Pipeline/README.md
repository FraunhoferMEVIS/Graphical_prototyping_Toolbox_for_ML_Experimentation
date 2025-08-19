# KI-FDZ: AI-Sandbox

## Running the App

This is the ai sandbox backend.

For this tool, you need a python version of 3.10 or newer.
First, install the requirements by running:

```
pip install -r requirements.txt
```

Then from this folder, run

```
python -m aisandbox_server
```

The api will be accessible via http://127.0.0.1:8000. For changing the default port, you can define the port in an environment variable names as "AISANDBOX_PORT" or start the app as following, for example, the default port number is changed to 8080:

```
AISANDBOX_PORT="8080" python -m aisandbox_server
```

<Temporary>: Until creating a new service for the methods_repository, to be able to run the created MLfow projet, you need to add the "methods_repository" to your PYTHONPATH:

```
export PYTHONPATH=${PYTHONPATH}:<path-to-the folder-containing-this-file>
```

## Development

If you want to add more algorithms to each step of the recipe, you can add them in the [steps](./steps) and then the specific folder of the step.

If a new step should be defined, in addition to adding a new folder, it is required too add the name to the [steps/names.py](./steps/names.py) file.

## Build Docker

docker build -t fdz_ai_sandbox .
