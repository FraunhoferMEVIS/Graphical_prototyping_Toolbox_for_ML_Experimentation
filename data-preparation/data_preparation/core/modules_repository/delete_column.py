""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: delete_column.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for removing/droping columns
-----------------------------------------------------------------------------
"""
import logging
from pandas import DataFrame
from data_preparation.core.modules_repository.base_node import Node
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from data_preparation.exceptions import ResultNotFound


__all__ = ["DeleteColumns"]
_logger = logging.getLogger(__name__)


class DeleteColumns(Node):
    """
    The module to remove a column from table.
    :param module_id: The unique identifier of the module.
    :param inputs: The input sockets of the module. It should be one input socket.
    :param config: The module's configurations, the column_name or the list of column_names that should be removed.
    """
    NAME = "delete-column"
    DESCRIPTION = "Filter a table by column values"
    IN_SOCKETS = [
            {
                "name": "input1",
                "description": "The input table to remove column from.",
                "required": True,
            }
        ]
    PARAMETERS = {
        "column_name": {
            "id": "column_name",
            "name": "column's name",
            "description": "The column's name to be removed or the list of columns' names",
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
            column_names = self.parameters["column_name"].value
            if isinstance(column_names, str):
                column_names = [column_names]
            column_names = set(column_names)
            output_metadata = {
                "keys": [],
                "features": [],
            }
            for key in input_metadata[self.inputs[0].name]["keys"]:
                if key not in column_names:
                    output_metadata["keys"].append(key)
            for feat in input_metadata[self.inputs[0].name]["features"]:
                if feat["name"] not in column_names:
                    output_metadata["features"].append(feat)
            return output_metadata
        raise TypeError("Please check that the inputs are connected and the results are ready!")
    
    def run_for_page(self, page: DataFrame) -> DataFrame:
        column_names = self.parameters["column_name"].value
        if isinstance(column_names, str):
            column_names = [column_names]
        return page.drop(columns=column_names)

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
                # Write the result to the output file
                if not self.write_output(result, append=True):
                    self.error_message = f"Failed to write output for module {self.NAME}"
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
            self.error_message = f"Error during {self.__class__.__name__} execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e
