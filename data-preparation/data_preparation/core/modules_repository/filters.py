""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: filters.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The model for a Filters module
-----------------------------------------------------------------------------
"""
import logging
from pandas import DataFrame
from data_preparation.core.modules_repository.utils import (
            validate_expression_code,
            get_expression_function
        )
from data_preparation.core.modules_repository.base_node import Node
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from data_preparation.exceptions import ResultNotFound


__all__ = ["FilterByColumnValues", "FilterByCondition"]
_logger = logging.getLogger(__name__)


class FilterByColumnValues(Node):
    """
    The module to filter a table by column values.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be a list of three sockets.
                   One socket for the table name, one for the column name and the other one for the value.
                   The table name and the column name are mandatory inputs of type string and 
                   the value is a mandatory input of type string, integer, float or boolean or a list of them.
    """
    NAME = "filter-by-value"
    DESCRIPTION = "Filter a table by column values"
    IN_SOCKETS = [
            {
                "name": "input1",
                "description": "The input table to be filtered",
                "required": True,
            }
        ]
    PARAMETERS = {
        "column_name": {
            "id": "column_name",
            "name": "column's name",
            "description": "The column's name to be filtered",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "values": {
            "id": "values",
            "name": "value",
            "description": "The value should be equal to this value to be filtered",
            "type": "string",
            "required": True,
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
                #  parent_project_path: str = "."
                ):
        """
           Initializes a Filter_By_Column_Values object.

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
            return input_metadata[self.inputs[0].name]

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run(self) -> None:
        """
        The run method of the module. It reads the input file and filters
        the table based on the column name and the value.
        """
        super().run()

        
        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        column_name = self.parameters["column_name"].value
        values = self.parameters["values"].value
        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                column_type = str(chunk.dtypes[column_name])
                if 'int' in column_type:
                    values = [int(val) for val in values]
                elif 'float' in column_type:
                    values = [float(val) for val in values]
                result = chunk[chunk[column_name].isin(values)]
                # Write the filtered result to the output file
                if not self.write_output(result, append=True):
                    self.error_message = f"Failed to write output for module {self.NAME}"
                    _logger.error(self.error_message)
                    raise IOError(self.error_message)
            self.valid_results = True
        except NameError as e:
            self.error_message = f"Error during Filter, {column_name} is not a column of the data (module {self.NAME}): {e}"
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
            self.error_message = f"Error during Filter_By_Column_Values execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e


class FilterByCondition(Node):
    """
    The module to filter a table based on the input condition.
    :param module_id: The unique identifier of the module.
    :param inputs: The input parameters of the module.
    """
    NAME = "filter-by-condition"
    DESCRIPTION = "Advanced filtering of a table based on the input condition"
    IN_SOCKETS = [
            {
                "name": "input1",
                "description": "The input table to be filtered",
                "required": True,
            }
        ]
    PARAMETERS = {
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": "The columns' name's to be used for filtering in the condition (up to 5 columns).",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "conditional_expression": {
            "id": "conditional_expression",
            "name": "conditional_expression",
            "description": """The output of this conditional expression
                should be True to include the rows in the output column.
                For example, it can be (x1 - x2) > 5, where 'x1' and 'x2' correspond
                to the first and second column in the 'columns' parameter, respectively.
                Currently, we support up to 5 inputs for the expression. They should be
                used as x1, x2, x3, x4, and x5.
                If checking against a string, is of interest, please use single 
                quatation mark; e.g. x1 == 'e'.
                Example for time related expressions: '(time(x1) - time(x2)) < timedelta(hours=24)'
                Here are a list of 
                supported constants: pi, e, nan, inf
                supported methods: ceil, floor, log, sqrt, pow, sin, cos, tan, asin, acos, atan, randint, random, time, timedelta
                supported operators: +, -, *, /, **, and, or, not, ^, &, |, ~, >>, << 
                """,
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
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
        """
           Initializes a FilterByCondition object.

           :param: module_id (str): The unique identifier of the module.
           :param: inputs (list[Socket]): The input sockets of the module.
           :param: config: input parameters of the module.
           :param: position: the position of the module in the page (for frontend).
           :param: parent_project_path (str): The parent project path.
           :param: result_repo: the results repository to save the output of the module into it.
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
            return input_metadata[self.inputs[0].name]

        raise TypeError("Please check that the inputs are connected and the results are ready!")
    
    def run_for_page(self, page: DataFrame) -> DataFrame:
        columns = self.parameters["columns"].value
        expression = self.parameters["conditional_expression"].value
        num_inputs = len(columns)
        validate_expression_code(expression=expression,
                                 sample_inputs=(page.iloc[0][col] for col in columns))
        condition = page.apply(lambda row: get_expression_function(
                                    expression=expression,
                                    num_inputs=num_inputs)(**{
                                        f"x{i+1}": row[col] for i, col in enumerate(columns)
                                    }), axis=1)
        return page[condition]


    def run(self) -> None:
        """
        The run method of the module. It reads the input file and filters
        the table based on the column name and the value.
        """
        super().run()
        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                result = self.run_for_page(chunk)
                # Write the filtered result to the output file
                if not self.write_output(result, append=True):
                    self.error_message = f"Failed to write output for module {self.NAME}"
                    _logger.error(self.error_message)
                    raise IOError(self.error_message)
            self.valid_results = True
        except NameError as e:
            self.error_message = f"Error during Filter, column name(s) not valid: {e}"
            _logger.error(self.error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except ResultNotFound as e:
            self.error_message = f"Input not found for module {self.NAME}."
            _logger.error(self.error_message)
            raise ResultNotFound(self.error_message) from e
        except Exception as e:
            self.error_message = f"Error during Filter_By_Column_Values execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e
