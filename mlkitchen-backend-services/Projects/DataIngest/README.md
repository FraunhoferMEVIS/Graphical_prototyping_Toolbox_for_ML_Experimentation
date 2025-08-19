# KI-FDZ: DATA_DESCRIPTOR

## Running the App

This is the Data Provider for ai sandbox.

For this tool, you need a python version of 3.10 or newer.
First, install the requirements by running:

```
pip install -r requirements/requirements_core.txt
```

Then from this folder, run

```
python -m serve
```

The api will be accessible via http://127.0.0.1:8088. For changing the default port, you can define the port in an environment variable names as "Data_INGEST_PORT" or start the app as following, for example, the default port number is changed to 8080:

```
Data_INGEST_PORT="8080" python -m serve
```

<Temporary>: Until creating a new service for the methods_repository, to be able to run the created MLfow projet, you need to add the "methods_repository" to your PYTHONPATH or creating a symbolic link (shortcut) to it in the current folder:

```
export PYTHONPATH=${PYTHONPATH}:<path-to-the folder-containing-this-file>
```

or

```
ln -s <path-to-parent-of-this-folder>/Pipeline/methods_repository .
```
