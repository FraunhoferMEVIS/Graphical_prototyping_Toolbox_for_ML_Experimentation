""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: select_events.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 07/2024
description: The module for select events in the data 
-----------------------------------------------------------------------------
"""
from pandas import DataFrame
import logging
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from data_preparation.exceptions import ResultNotFound

__all__ = ["SelectEvent"]
_logger = logging.getLogger(__name__)



class SelectEvent(Node):
    """
    Based on the operator only the event with the smallest, biggest value or earliest, latest event is kept.
    """
    NAME = "select-event"
    DESCRIPTION = "Based on the operator only the event with the smallest, biggest value or earliest, latest event is kept"
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
            "value": ["id"],
            "multipleValues": True
        },
        "operator": {
            "id": "operator",
            "name": "operator",
            "description": "The operator to determine the event",
            "type": "string",
            "required": False,
            "value": "latest",
            "allowedValues": ["min","max","latest","earliest"],
            "multipleValues": False
        },
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": "The columns to apply the operation on",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues":True
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
        if self.inputs and self.inputs[0].name:
            return input_metadata[self.inputs[0].name]

        raise TypeError("Please check that the inputs are connected and the results are ready!")
    
    def run_for_page(self, page: DataFrame) -> DataFrame:
        columns = columns_to_list(self.parameters["columns"].value)
        check_matching_datatypes(page[columns])
        operator=self.parameters["operator"].value
        grouping_keys=self.parameters["grouping_keys"].value
        if operator=="min" or operator == "earliest" :
            idx = page.groupby(grouping_keys)[columns].idxmin() 
        elif operator=="max" or operator == "latest" :
            idx = page.groupby(grouping_keys)[columns].idxmax() 
        else:
            raise TypeError("Please check that you choose a valid operator!")
        idx = idx.apply(lambda x: x.iloc[0], axis=1)
        return page.loc[idx]

 

    def run(self) -> None:
        """
        The run method of the module. It reads the input file and filters
        the table based on a selected event for a defined group.
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
        except KeyboardInterrupt as e:
            self.error_message = f"Process interrupted by the user: {e}"
            _logger.error(self.error_message)
            raise KeyboardInterrupt(self.error_message) from e
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except ResultNotFound as e:
            self.error_message = f"Input not found for module {self.NAME}."
            _logger.error(self.error_message)
            raise ResultNotFound(self.error_message) from e
        except Exception as e:
            self.error_message = f"Error during select event execution: {e}"
            _logger.error(self.error_message)
            raise Exception(self.error_message) from e


def columns_to_list(columns):
    if isinstance(columns, str):
        return [columns]
    return columns

def check_matching_datatypes(columns):
    column_types = columns.dtypes.unique()
    if len(column_types) > 1:
            raise TypeError("All columns must have the same data type!")   