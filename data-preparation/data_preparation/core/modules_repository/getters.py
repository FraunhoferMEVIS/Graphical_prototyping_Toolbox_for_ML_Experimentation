""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: getters.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The model for a table getter module
-----------------------------------------------------------------------------
"""
import os
import logging
from copy import deepcopy
import pandas
import psycopg2
from sqlalchemy import create_engine
from data_preparation.core.modules_repository.base_node import (
            Node, Socket, ModuleConfigParameter)
from data_preparation.core.app_config import (
            POSTGRES_DB, POSTGRES_HOST,
            POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD,
            DATA_PREPARATION_CSV_REPO)
from data_preparation.core.results_repository import (
                        ResultsRepository,  FileResultsRepository,
                        DictIO, DataFrameIO)


__all__ = ["GetPostgresTable", "LoadCSVFile"]

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def _add_feature_to_metadata(metadata, feature_name, feature_type):
    if 'features' not in metadata:
        metadata['features'] = []
    # if the feature is already there, don't add it again.
    if feature_name in metadata["keys"]:
        return metadata
    for feature in metadata['features']:
        if feature["name"] == feature_name:
            return metadata
    metadata['features'].append(
        {
            "name": feature_name,
            "type": feature_type
        }
    )
    return metadata


def _copy_input_metadata(input_metadata: dict) -> dict:
    metadata = {
        'data_type': 'tabular',
        'keys': [], # list of str
        'features': [], # list of dicts
    }
    try:
        metadata["keys"] = deepcopy(input_metadata["keys"])
        metadata["features"] = [{
            "name": key,
            "type": val,
        } for key, val in input_metadata["features"].items()]
    except Exception as e:
        message = """The input metadata should follow this pattern:
                        {
                        "keys": ["key1", "key2"],
                        "features": {
                            "feature_name_1": "numerical",
                            "feature_name_2": "categorical",
                                ... 
                        }
                        }
                """
        _logger.error(message)
        raise Exception(message) from e
    return metadata

class GetPostgresTable(Node):
    """
    The module to connect to a postgres database and saves the table as a parquet file.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be a list of two sockets.
                   One socket for the table name and the other one for the schema name.
                   The table name is a mandatory input of type string and 
                   the schema name is an optional string and if not defined,
                   it will be set to "public".
    """
    NAME = "sqlTable"
    DESCRIPTION = "Get a table from a PostgreSQL database"
    IN_SOCKETS = []
    PARAMETERS = {
        "table_name": {
            "id": "table_name",
            "name": "Table",
            "description": "The name of the table in the PostgreSQL database",
            "type": "string",
            "required": True,
            "value": None
        },
        "schema": {
            "id": "schema",
            "name": "Schema",
            "description": "The schema of the PostgreSQL database",
            "type": "string",
            "required": False,
            "value": "public"
        },
    }
    def __init__(self,
                 module_id: str = "",
                 label: str = None,
                 inputs: list[Socket] = None,
                 config: dict[str, ModuleConfigParameter] = None,
                 valid_results: bool = False,
                 position: dict = None,
                 parent_project: str = None,
                 result_repo: ResultsRepository = FileResultsRepository(),
                #  parent_project_path: str = "."
                ):
        super().__init__(
                 module_id=module_id,
                 label=label,
                 inputs=inputs,
                 config=config,
                 valid_results=valid_results,
                 position=position,
                 parent_project=parent_project,
                 result_repo=result_repo,
                 )

    def __get_connection(self, stream=True):
        try:
            if stream:
                engine = create_engine(
                    f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
                conn = engine.connect().execution_options(
                                            stream_results=True)
            else:
                conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, host=POSTGRES_HOST,
                                        port=POSTGRES_PORT, password=POSTGRES_PASSWORD)
            return conn
        except (Exception, psycopg2.DatabaseError) as e:
            self.error_message = f"Error during PostgreSQL module execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e
    
    def get_input_metadata(self) -> dict[str, dict]:
        """
        currently, we do not return anything for the input metadata of postgres table getters
        """
        return None

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        """
        It gets the metada from the postgres table.
        The output dict contains all column names and the
        type of data: key/numerical/categorical.
        """
        if not input_metadata:
            input_metadata = {
                "keys": [],
                "features": {}
            }
        metadata = _copy_input_metadata(input_metadata)
        
        try:
            with self.__get_connection() as connection:
                # Get the table name from the input socket
                table_name = self.parameters["table_name"].value
                # Get the schema name from the input socket
                schema = self.parameters["schema"].value
                
                # get all columns and their types
                query = f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = '{schema}'
                    AND table_name = '{table_name}';"""
                columns = pandas.read_sql(query, connection)

                query = f"""
                    SELECT a.attname
                    FROM   pg_index i
                    JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                        AND a.attnum = ANY(i.indkey)
                    WHERE  i.indrelid = '{schema}.{table_name}'::regclass
                    AND    i.indisprimary;"""

                keys = pandas.read_sql(query, connection)
                if isinstance(keys, pandas.DataFrame):
                    metadata['keys'] = list(keys['attname'])
                else:
                    self.error_message = f"Error during PostgreSQL while acquiring metadata: {keys}"
                    _logger.error(self.error_message)
                    raise Exception(self.error_message)
        except Exception as e:
            self.error_message = f"Error during PostgreSQL while acquiring table info: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e

        for _, column in columns.iterrows():
            if column['column_name'] in metadata['keys'] or \
                column["column_name"] in input_metadata['features']:
                # already added as a key
                continue
            if column["data_type"] in {'uuid', }:
                metadata['keys'].append(column["column_name"])
                continue
            elif column['data_type'] in {
                    'integer', 'bigint', 'smallint', 'double precision', 'money', 
                    'numeric', 'real', 'serial', 'smallserial', 'bigserial'}:
                feature_type = 'numerical'
            elif column["data_type"] in {'character', 'character varying', 'boolean'}:
                feature_type = 'categorical'
            elif column["data_type"] in {'json', 'jsonb', 'text', 'tsquery', 'tsvector', 'xml'}:
                feature_type = 'text'
            elif column["data_type"] in {
                    'time', 'timestamp', 'timestamp without time zone', 'timestamp with time zone'}:
                feature_type = 'time'
            elif column["data_type"] in {'date', }:
                feature_type = 'date'
            elif column['data_type'] in {'interval', }:
                feature_type = 'interval'
            else:
                feature_type = 'other'
            
            metadata = _add_feature_to_metadata(
                                    metadata=metadata, 
                                    feature_name=column["column_name"],
                                    feature_type=feature_type)
        return metadata

    def run(self) -> None:
        """
           Runs the Get_Postgres_Table module.
           If successful, the results will be saved to the OUTPUT socket.
        """
        super().run()

        try:
            output_meta = self.define_output_metadata(
                input_metadata=self.get_input_metadata())
            self.write_metadata(output_meta)

            with self.__get_connection() as connection:
                # Get the table name from the input socket
                table_name = self.parameters["table_name"].value
                # Get the schema name from the input socket
                schema = self.parameters["schema"].value

                query = f"SELECT * FROM {schema}.{table_name};"
                for data in pandas.read_sql(
                        query, connection, chunksize=self._CHUNKSIZE):

                    if not self.write_output(data):
                        _logger.error("Failed to write output for module %s", self.NAME)
                        raise IOError(f"Failed to write output for module {self.NAME}")

            self.valid_results = True
        except Exception as e:
            self.error_message = f"Error during PostgreSQL module execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e


def get_list_of_datasets() -> list[str]:
    """
    Returns the list of all datasets in the repository
    """
    datasets = []
    if os.path.exists(DATA_PREPARATION_CSV_REPO):
        datasets = os.listdir(DATA_PREPARATION_CSV_REPO)
    return datasets


def get_list_of_dataset_tables(dataset: str) -> list[str]:
    """
    Returns the list of files of a specific dataset
    """
    dataset_folder = os.path.join(DATA_PREPARATION_CSV_REPO, dataset)
    if not os.path.exists(dataset_folder):
        raise ValueError("The given dataset doesn't exist")
    tables = [file for file in os.listdir(dataset_folder) if file.endswith('.csv')]
    return tables


def get_list_of_csv(dataset: str = "all") -> list[str]:
    """
    Returns the list of tables in a given dataset or all existing tables
    """
    tables = []
    if dataset == "all":
        datasets = get_list_of_datasets()
    else:
        datasets = [dataset]
    
    for dataset_name in datasets:
        tables.extend([f"{dataset_name}:{filename}" for filename in get_list_of_dataset_tables(dataset_name)])

    return tables


class LoadCSVFile(Node):
    """
    The module to import a file from CSV or Parquet file.
    :param module_id: The unique identifier of the module.
    :param inputs: The input parameters of the module.
                   The input parameter is the file name.
    """
    NAME = "load-csv-file"
    DESCRIPTION = "Get a table from a file"
    IN_SOCKETS = []
    PARAMETERS = {
        "table": {
            "id": "table",
            "name": "table",
            "description": "The name of the table containing data.",
            "type": "string",
            "required": True,
            "value": None,
            "allowedValues": get_list_of_csv()
        },
    }
    def __init__(self,
                 module_id: str = "",
                 label: str = None,
                 inputs: list[Socket] = None,
                 config: dict[str, ModuleConfigParameter] = None,
                 valid_results: bool = False,
                 position: dict = None,
                 parent_project: str = None,
                 result_repo: ResultsRepository = FileResultsRepository(),
                ):
        self._update_list_of_csv()
        super().__init__(
                 module_id=module_id,
                 label=label,
                 inputs=inputs,
                 config=config,
                 valid_results=valid_results,
                 position=position,
                 parent_project=parent_project,
                 result_repo=result_repo,
                 )

    def get_input_metadata(self) -> dict[str, dict]:
        """
        currently, we do not return anything for the input metadata of postgres table getters
        """
        if metadata_file := self._get_file_name(file='json'):
            dict_io = DictIO()
            metadata = dict_io.read(metadata_file)
        else:
            metadata = {
                "keys": [],
                "features": {}
            }
        return metadata

    def _file_reader(self):
        file_io = DataFrameIO()
        filepath = self._get_file_name(file='csv')
        delimiter = ","
        decimal = "." 
        return file_io.read(filepath,
                            delimiter=delimiter,
                            decimal=decimal,
                            chunksize=self._CHUNKSIZE)
    
    def _get_file_name(self, file: str = 'csv'):
        file_name = self.parameters["table"].value
        data_table_combo = file_name.split(":")
        if len(data_table_combo) != 2:
            raise ValueError("Wrong format for the table name. The correct format is 'dataset_name:csv_filename'")
        dataset_name, file_name = data_table_combo[0], data_table_combo[1]
        filepath = os.path.join(DATA_PREPARATION_CSV_REPO,
                                dataset_name, file_name)
        if file == 'json':
            if filepath.endswith('.csv'):
                filepath = filepath[:-4]
            filepath = filepath + '.json'
            if not os.path.exists(filepath):
                return None
        return filepath
        

    def update_parameters(self, new_parameters: dict[str, ModuleConfigParameter]) -> None:
        """
        If the name of the dataset is changed,
        the allowed values for the tables should be updated.
        """
        self._update_list_of_csv()
        super().update_parameters(new_parameters)

    def _update_list_of_csv(self): #, dataset: str = None):
        """
        updates the list of CSV tables
        """
        self.PARAMETERS["table"]["allowedValues"] = get_list_of_csv()

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        """
        It gets the metada from the postgres table.
        The output dict contains all column names and the
        type of data: key/numerical/categorical.
        """
        if not input_metadata:
            input_metadata = {
                "keys": [],
                "features": {}
            }
        metadata = _copy_input_metadata(input_metadata)

        for chunk in self._file_reader():
            # remove features from metadata, if they don't exist in the data:
            metadata["features"] = [feature \
                for feature in metadata['features'] if feature['name'] in chunk.columns
            ]
            metadata["keys"] = [key \
                for key in metadata['keys'] if key in chunk.columns
            ]
            # get all columns and their types
            for column in chunk.columns:
                if column == 'Unnamed: 0':
                    continue
                if (column_type := str(chunk.dtypes[column])) in {'object', 'bool'}:
                    feature_type = "categorical"
                elif 'int' in column_type:
                    num_diff_values = len(set(chunk[column]))
                    # if there are only two or three different values and we have enough rows
                    # or a small ratio of different values to the total number of samples
                    # observed, then the feature is probably categorical:
                    if (num_diff_values <= 3 and len(chunk[column]) >= 10) or \
                       num_diff_values / len(chunk[column]) < 0.05:
                        feature_type = "categorical"
                    else:
                        feature_type = "numerical"
                elif 'float' in column_type:
                    feature_type = "numerical"
                else:
                    feature_type = 'other'
                
                metadata = _add_feature_to_metadata(
                                        metadata=metadata, 
                                        feature_name=column,
                                        feature_type=feature_type)
            break
        return metadata

    def run(self) -> None:
        """
           Runs the module.
        """
        super().run()

        try:
            output_meta = self.define_output_metadata(
                input_metadata=self.get_input_metadata())
            self.write_metadata(output_meta)

            for chunk in self._file_reader():
                if not self.write_output(chunk):
                    _logger.error("Failed to write output for module %s", self.NAME)
                    raise IOError(f"Failed to write output for module {self.NAME}")
            self.valid_results = True
        except Exception as e:
            self.error_message = f"Error during uploading data (module {self.NAME}): {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e
