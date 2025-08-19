""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: edit_metadata.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2024
description: The module for editing meta data, i.e., renaming columns, changing data type 
-----------------------------------------------------------------------------
"""

import logging
from abc import ABC, abstractmethod
import uuid
import json
from pandas import DataFrame, to_datetime
from data_preparation.core.modules_repository.base_node import Node
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import (
    ResultsRepository,
    FileResultsRepository,
    ResultTypes,
)
from data_preparation.exceptions import ResultNotFound


__all__ = ["EditColumnName", "EditDataType"]
_logger = logging.getLogger(__name__)


class EditMetaData(Node, ABC):

    @abstractmethod
    def run_for_page(self, page: DataFrame) -> DataFrame:
        raise NotImplementedError

    @abstractmethod
    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        raise NotImplementedError

    def run(self) -> None:
        """
        The run method of the module. It reads the input file and filters
        the table based on the column name and the value.
        """
        super().run()
        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata()
        )
        self.write_metadata(output_meta)

        try:
            # Read the input file
            for chunk in self._results_repo.get(
                self.parent_project,
                self.inputs[0].value,
                ResultTypes.DATAFRAME,
                chunksize=self._CHUNKSIZE,
            ):

                result = self.run_for_page(chunk)
                # Write the result to the output file
                if not self.write_output(result, append=True):
                    self.error_message = (
                        f"Failed to write output for module {self.NAME}"
                    )
                    _logger.error(self.error_message)
                    raise IOError(self.error_message)
            self.valid_results = True
        except NameError as e:
            self.error_message = f"Error in the selected name: {e}"
            _logger.error(self.error_message)
            raise NameError(self.error_message) from e
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except ResultNotFound as e:
            self.error_message = f"Input not found for module {self.NAME}."
            _logger.error(self.error_message)
            raise ResultNotFound(self.error_message) from e
        except Exception as e:
            self.error_message = (
                f"Error during {self.__class__.__name__} execution: {e}"
            )
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e


class EditDataType(EditMetaData):
    """
    The module as base class to edit data types.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be one input socket.
    :param config: The module's configurations, the column_name or the list of column_names that should be removed.
    """

    NAME = "edit-data-type"
    DESCRIPTION = "Edit Data Type"
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to change data types.",
            "required": True,
        }
    ]
    PARAMETERS = {
        "column_names": {
            "id": "column_names",
            "name": "column's names",
            "description": "The column's name to be edit",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True,
        },
        "new_data_types": {
            "id": "new_data_types",
            "name": "new data types",
            "description": "The new data type or the list of data types.",
            "type": "string",
            "required": True,
            "value": None,
            "allowedValues": {
                "uuid",
                "key",
                "float",
                "integer",
                "string",
                "boolean",
                "json",
                "time",
                "date",
                "timestamp",
                "interval",
            },
            "multipleValues": True,
        },
    }

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        if self.inputs and self.inputs[0].name:
            output_metadata = input_metadata[self.inputs[0].name]

            column_names = into_list(self.parameters["column_names"].value)
            new_data_types = into_list(self.parameters["new_data_types"].value)

            def datatypes_in_meta(datatype: str) -> str:
                if datatype in {"integer", "float"}:
                    return "numerical"
                if datatype in {"boolean"}:
                    return "categorical"
                if datatype in {"json", "string"}:
                    return "text"
                if datatype in {"time", "timestamp", "date"}:
                    return "time"
                if datatype in {"interval"}:
                    return "interval"
                raise ValueError("Unsupported data type")

            if len(column_names) != len(new_data_types):
                raise ValueError(
                    f"The lengths of '{column_names}' and '{new_data_types}' do not match."
                )

            for column_name, datatype in zip(column_names, new_data_types):
                for feature in output_metadata["features"]:
                    if feature["name"] == column_name:
                        if datatype in {"uuid", "key"}:
                            output_metadata["keys"].append(column_name)
                            output_metadata["features"].remove(feature)
                        else:
                            feature["type"] = datatypes_in_meta(datatype)
                        break
                else:
                    for key in output_metadata["keys"]:
                        if key == column_name:
                            if datatype in {"uuid", "key"}:
                                key["type"] = datatype
                            else:
                                output_metadata["features"].append(
                                    {
                                        "name": column_name,
                                        "type": datatypes_in_meta(datatype),
                                    }
                                )
                                output_metadata["keys"].remove(key)
                            break
                    else:
                        raise ValueError(
                            f"Feature '{column_name}' does neither exist in features nor key."
                        )
            return output_metadata
        raise TypeError(
            "Please check if the inputs are connected and the results are ready!"
        )

    def run_for_page(self, page: DataFrame) -> DataFrame:
        column_names = into_list(self.parameters["column_names"].value)
        new_data_types = into_list(self.parameters["new_data_types"].value)

        def convert_column(df, column_name, data_type):
            if column_name not in df.columns:
                raise ValueError("Column not found in DataFrame")

            if data_type == "uuid":
                return df[column_name].apply(lambda x: str(uuid.UUID(x)))
            if data_type == "key":
                return df[column_name]
            if data_type in {"float", "integer"}:
                return (
                    df[column_name].astype(float)
                    if "float" in data_type
                    else df[column_name].astype(int)
                )
            if data_type in {"string"}:
                return df[column_name].astype(str)
            if data_type == "boolean":
                ##check that again
                return df[column_name].str.lower().isin([True, "true", "1"])
            if data_type in {"json"}:
                return df[column_name].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
            if data_type in {"time"}:
                return to_datetime(df[column_name]).dt.time
            if data_type in {"date"}:
                return to_datetime(df[column_name]).dt.date
            if data_type in {"timestamp"}:
                return to_datetime(df[column_name])
            if data_type == "interval":
                return df[column_name]
            raise ValueError("Unsupported data type")

        for column, datatype in zip(column_names, new_data_types):
            page[column] = convert_column(page, column, datatype)
        return page


class EditColumnName(EditMetaData):
    """
    The module to edit column names.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be one input socket.
    :param config: The module's configurations, the column_name or the list of column_names that should be removed.
    """

    NAME = "edit-column-name"
    DESCRIPTION = "Edit Column Names"
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to edit column names.",
            "required": True,
        }
    ]
    PARAMETERS = {
        "column_names": {
            "id": "column_names",
            "name": "column's names",
            "description": "The column's name to be edit or the list of columns' names to be edit",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True,
        },
        "new_column_names": {
            "id": "new_column_names",
            "name": "new column's names",
            "description": "The new column's name or the list of new columns' names. The length of column names and new column names must be equal.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True,
        },
        "keys": {
            "id": "keys",
            "name": "column's names",
            "description": "The key name to edit or the list of key names to edit",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True,
        },
        "new_keys": {
            "id": "new_keys",
            "name": "new keys's names",
            "description": "The new keys's name or the list of new key names. The length of keys and new keys must be equal.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True,
        },
    }

    def __init__(
        self,
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
        """
        Initializes a DeleteColumns object.

        :param: module_id (str): The unique identifier of the module.
        :param: inputs (list[Socket]): The input sockets of the module.
        :param: parent_project_path (str): The parent project path.
        """
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

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        if self.inputs and self.inputs[0].name:
            output_metadata = input_metadata[self.inputs[0].name]
            change_column_names = into_list(self.parameters["column_names"].value)
            new_column_names = into_list(self.parameters["new_column_names"].value)
            change_keys = into_list(self.parameters["keys"].value)
            new_keys = into_list(self.parameters["new_keys"].value)

            if change_column_names is not None and len(change_column_names) != len(
                new_column_names
            ):
                raise ValueError(
                    f"The lengths of '{change_column_names}' and '{new_column_names}' do not match."
                )
            if change_keys is not None and len(change_keys) != len(new_keys):
                raise ValueError(
                    f"The lengths of '{change_keys}' and '{new_keys}' do not match."
                )

            if change_column_names:
                for old_name, new_name in zip(change_column_names, new_column_names):
                    found = False
                    for feature in output_metadata["features"]:
                        if feature["name"] == old_name:
                            feature["name"] = new_name
                            found = True
                            break
                    if not found:
                        raise ValueError(
                            f"Feature '{old_name}' does not exist in features."
                        )
            if change_keys:
                for old_key, new_key in zip(change_keys, new_keys):
                    if old_key in output_metadata["keys"]:
                        output_metadata["keys"][
                            output_metadata["keys"].index(old_key)
                        ] = new_key
                    else:
                        raise ValueError(f"Key '{old_key}' does not exist in keys.")
            return output_metadata
        raise TypeError(
            "Please check that the inputs are connected and the results are ready!"
        )

    def run_for_page(self, page: DataFrame) -> DataFrame:
        column_names = into_list(self.parameters["column_names"].value)
        keys = into_list(self.parameters["keys"].value)
        new_column_names = into_list(self.parameters["new_column_names"].value)
        new_keys = into_list(self.parameters["new_keys"].value)
        old_names = combine_lists(column_names, keys)
        new_names = combine_lists(new_column_names, new_keys)
        return page.rename(columns=dict(zip(old_names, new_names)))


def into_list(var):
    if isinstance(var, str):
        return [var]
    if not var:
        return None
    return var


def combine_lists(*args):
    combined = []
    for arg in args:
        if arg:
            combined.extend(arg)
    return combined
