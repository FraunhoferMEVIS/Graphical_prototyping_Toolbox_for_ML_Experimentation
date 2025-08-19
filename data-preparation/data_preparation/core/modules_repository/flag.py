""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: flag.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 07/2024
description: The model for a Flag module
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


__all__ = ["Flag"]
_logger = logging.getLogger(__name__)


class Flag (Node):
    """
    The module flag creates a new column and flags (=True) a row if the condition is true.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be a list of three sockets.
                   One socket for the table name, one for the column name and the other one for the value.
                   The table name and the column name are mandatory inputs of type string and 
                   the value is a mandatory input of type string, integer, float or boolean or a list of them.
    """
    NAME = "flag-by-condition"
    DESCRIPTION = "Flag a table by column condition"
    IN_SOCKETS = [
            {
                "name": "input1",
                "description": "The input table to be flagged",
                "required": True,
            }
        ]
    PARAMETERS = {
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": "The columns' name's which is used to flag based on the condition (up to 5 columns).",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "conditional_expression": {
            "id": "conditional_expression",
            "name": "conditional_expression",
            "description": """If the output of this conditional expression
                is true the new flag column is flagged as True.
                For example, it can be (x1 - x2) > 5, where 'x1' and 'x2' correspond
                to the first and second column in the 'columns' parameter, respectively.
                Currently, we support up to 5 inputs for the expression. They should be
                used as x1, x2, x3, x4, and x5.
                If checking against a string is of interest, please use single 
                quatation mark; e.g. x1 == 'e'.
                Here are a list of 
                supported constants: pi, e, nan, inf
                supported methods: ceil, floor, log, sqrt, pow, sin, cos, tan, asin, acos, atan, randint, random
                supported operators: +, -, *, /, **, and, or, not, ^, &, |, ~, >>, << 
                """,
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "flag_column_name": {
            "id": "flag_column_name",
            "name": "flags column's name",
            "description": "The flagged column's name",
            "type": "string",
            "required": False,
            "multipleValues": False,
            "value": "flag"
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
           Initializes a Flag object.

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
            output_metadadata = input_metadata[self.inputs[0].name]
            self.new_column_name = self.parameters["flag_column_name"].value
            print(' self.new_column_name', self.new_column_name)
            output_metadadata['features'].append(
                {
                    "name": self.new_column_name,
                    "type": "categorical"
                })
            return output_metadadata

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
        page[ self.new_column_name]=condition
        return page

    def run(self) -> None:
        """
        The run method of the module. It reads the input file and flags e based on the column name and the value.
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
                if not self.write_output(result, append=True):
                    self.error_message = f"Failed to write output for module {self.NAME}"
                    _logger.error(self.error_message)
                    raise IOError(self.error_message)
            self.valid_results = True
        except NameError as e:
            self.error_message = f"Error during Flag, column name(s) not valid: {e}"
            _logger.error(self.error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"Error during Flag, column name(s) not valid: {e}"
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
        except SyntaxError as e:
            self.error_message = f"Syntax Error in the expression: {e}"
            _logger.error(self.error_message)
            raise SyntaxError(self.error_message) from e
        except Exception as e:
            self.error_message = f"Error during flag module execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e
