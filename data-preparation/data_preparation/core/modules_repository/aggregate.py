""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: aggregate.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for a aggregating and transforming the data
-----------------------------------------------------------------------------
"""
from collections import Counter
from functools import reduce
import math
import logging
from numpy import median, mean
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from .new_column import (string_to_function,
                         get_operation_output_type)


__all__ = ["AggregateAndTransform"]
_logger = logging.getLogger(__name__)


def most_common(values):
    values = values.dropna()
    return Counter(values).most_common(1)[0][0] if not values.empty else float("nan")


def least_common(values):
    values = values.dropna()
    return Counter(values).most_common()[-1][0] if not values.empty else float("nan")

def xor(values):
    values = values.dropna()
    return reduce(lambda x, y: x^y, values) if not values.empty else float("nan")


def binary_and(values):
    values = values.dropna()
    return reduce(lambda x, y: x&y, values) if not values.empty else float("nan")


def binary_or(values):
    values = values.dropna()
    return reduce(lambda x, y: x | y, values) if not values.empty else float("nan")


_operators = {
   "sum": {
        "method": sum,
        "output_type": "numerical",
        "allowed_input_type": ["numerical"]
    },
    "average": {
        "method": mean,
        "output_type": "numerical",
        "allowed_input_type": ["numerical"]
    },
    "median": {
        "method": median,
        "output_type": "numerical",
        "allowed_input_type": ["numerical"]
    }, 
    "min": {
        "method": min,
        "output_type": ["numerical", "categorical"],
        "allowed_input_type": ["numerical", "time"]
    },
    "max": {
        "method": max,
        "output_type": ["numerical", "categorical"],
        "allowed_input_type": ["numerical","time"]
    },
    "product": {
        "method": math.prod,
        "output_type": "numerical",
        "allowed_input_type": ["numerical"]
    },
    "all": {
        "method": all,
        "output_type": "categorical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
    "binary_and": {
        "method": binary_and,
        "output_type": "categorical",
        "allowed_input_type": ["numerical", "categorical"]
    },
    "any": {
        "method": any,
        "output_type": "categorical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
    "binary_or": {
        "method": binary_or,
        "output_type": "categorical",
        "allowed_input_type": ["numerical", "categorical"]
    },
    "binary_xor": {
        "method": xor,
        "output_type": "categorical",
        "allowed_input_type": ["numerical", "categorical"]
    },
    "most_common": {
        "method": most_common,
        "output_type": "categorical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
    "least_common": {
        "method": least_common,
        "output_type": "categorical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
}

class AggregateAndTransform(Node):
    """
    Aggregate and transform the data (from various time points) to one column.
    """
    NAME = "aggregateAndTransform"
    DESCRIPTION = "Aggregates the data (from various time points) to one column and a single row."
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be filtered",
            "required": True,
        },
    ]
    PARAMETERS = {
        "grouping_keys": {
            "id": "grouping_keys",
            "name": "grouping keys",
            "description": """The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
            "type": "string",
            "required": True,
            "value": ["result"],
            "multipleValues": True
        },
        "operator": {
            "id": "operator",
            "name": "operator",
            "description": "The operator to be applied to the columns",
            "type": "string",
            "required": False,
            "value": ["sum"],
            "allowedValues": set(_operators.keys()),
            "multipleValues": True
        },
        "column": {
            "id": "column",
            "name": "column",
            "description": "The column to apply the operation on",
            "type": "string",
            "required": True,
            "value": None
        },
        "output_column_name": {
            "id": "output_column_name",
            "name": "output column name",
            "description": "The name of the output column that is generated.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
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
        output_metadata = {
            "keys": [],
            "features": []
        }
        if self.inputs and self.inputs[0].name:
            grouping_columns = self.parameters["grouping_keys"].value
            if isinstance(grouping_columns, str):
                grouping_columns = [grouping_columns]
            in_meta = input_metadata[self.inputs[0].name]
            
            features = {}
            for feat in in_meta["features"]:
                features[feat["name"]] = feat["type"]

            for key in grouping_columns:
                if key in in_meta["keys"]:
                    output_metadata["keys"].append(key)
                else:
                    if key not in features:
                        raise ValueError(f"The {key} could not be found in the input table.")
                    output_metadata["features"].append({
                        "name": key,
                        "type": features[key]
                    })

            names = self._get_output_column_names()
            ops = self.parameters["operator"].value

            input_column = self.parameters["column"].value
            if input_column not in features:
                raise ValueError(f"The {input_column} could not be found in the input table.")
            
            input_type = features[input_column]
            if isinstance(ops, str):
                ops = [ops]
            for op in ops:
                output_metadata["features"].append({
                    "name": names[op]["column_name"],
                    "type": get_operation_output_type(op, input_type=input_type, operators=_operators)
                })

            return output_metadata

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run(self) -> None:
        """
          Implement the logic to aggregate the values in a given column.
        """
        super().run()

        column = self.parameters["column"].value
        grouping_columns = self.parameters["grouping_keys"].value
        if isinstance(grouping_columns, str):
            grouping_columns = [grouping_columns]

        names = self._get_output_column_names()
        names = {
            col["column_name"]: col["function"] for col in names.values()
        }
        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                result = chunk.groupby(grouping_columns)[column].agg(**names)
                result = result.reset_index()
                if not self.write_output(result):
                    raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to add new column: %s", e)
            raise Exception(f"Failed to add new column: {e}") from e

    def _get_output_column_names(self):
        ops = self.parameters["operator"].value
        if isinstance(ops, str):
            ops = [ops]
        output_column_name = self.parameters["output_column_name"].value
        column = self.parameters["column"].value

        functions = [string_to_function(op, operators=_operators)
                     for op in ops]

        if output_column_name:
            if len(output_column_name) != len(functions):
                raise ValueError("The columns_name should have the same length as the 'functions'.")
            names = {
                op: {
                   "column_name": output_column_name[i],
                   "function": functions[i]
                } for i, op in enumerate(ops)
            }
        else:
            names = {
                       op: {
                           "column_name": f'{column}_{op}',
                           "function": functions[i]
                       } for i, op in enumerate(ops)
                    }
        return names



class AggregateAndTransformMulti(Node):
    """
    Aggregate and transform the data (from various time points) to one column.
    """
    NAME = "aggregate-and-transform-multi-columns"
    DESCRIPTION = "Aggregates the data (from various time points) to one column and a single row."
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be filtered",
            "required": True,
        },
    ]
    PARAMETERS = {
        "grouping_keys": {
            "id": "grouping_keys",
            "name": "grouping keys",
            "description": """The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
            "type": "string",
            "required": True,
            "value": ["result"],
            "multipleValues": True
        },
        "operator": {
            "id": "operator",
            "name": "operator",
            "description": "The operator to be applied to the columns",
            "type": "string",
            "required": False,
            "value": "sum",
            "allowedValues": set(_operators.keys()),
            "multipleValues": False
        },
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": "The column(s) to apply the operation on",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "output_column_name": {
            "id": "output_column_name",
            "name": "output column name",
            "description": "The name of the output column that is generated.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
    }
    
    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        output_metadata = {
            "keys": [],
            "features": []
        }
        if self.inputs and self.inputs[0].name:
            grouping_columns = self.parameters["grouping_keys"].value
            if isinstance(grouping_columns, str):
                grouping_columns = [grouping_columns]
            in_meta = input_metadata[self.inputs[0].name]
            for key in grouping_columns:
                if key in in_meta["keys"]:
                    output_metadata["keys"].append(key)
                else:
                    for feat in in_meta["features"]:
                        if feat["name"] == key:
                            column_type = feat["type"]
                            break
                    else:
                        raise ValueError(f"The {key} could not be found in the input table.")
                    output_metadata["features"].append({
                        "name": key,
                        "type": column_type
                    })

            names = self._get_output_column_names()
            op = self.parameters["operator"].value

            columns = self.parameters["columns"].value
            input_column_types = {}
            for feat in in_meta["features"]:
                if feat["name"] in columns:
                    input_column_types[feat["name"]] = feat["type"]

            for in_col_name, out_col_name in zip(columns, names):
                output_metadata["features"].append({
                    "name": out_col_name,
                    "type": get_operation_output_type(op,
                                                      input_type=input_column_types[in_col_name],
                                                      operators=_operators)
                })

            return output_metadata

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run(self) -> None:
        """
          Implement the logic to aggregate the values in a given column.
        """
        super().run()

        columns = self.parameters["columns"].value
        if isinstance(columns, str):
            columns = [columns]
        grouping_columns = self.parameters["grouping_keys"].value
        if isinstance(grouping_columns, str):
            grouping_columns = [grouping_columns]

        op = self.parameters["operator"].value
        operation = string_to_function(op, operators=_operators)

        names = self._get_output_column_names()
        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                result = chunk.groupby(grouping_columns)[columns].agg(operation)
                result.columns = names
                result = result.reset_index()
                if not self.write_output(result):
                    raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to add new column: %s", e)
            raise Exception(f"Failed to add new column: {e}") from e

    def _get_output_column_names(self):
        op = self.parameters["operator"].value
        output_column_name = self.parameters["output_column_name"].value
        columns = self.parameters["columns"].value
                    
        if output_column_name:
            if len(output_column_name) != len(columns):
                raise ValueError("The columns_name should have the same length as the 'columns'.")
            return output_column_name
        return [f'{column}_{op}' for column in columns]
