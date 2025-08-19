""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: NewColumns.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for a adding a new column to a table
-----------------------------------------------------------------------------
"""
import logging
import pandas as pd
from pandas import DataFrame, Series
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes


__all__ = ["AssignTimewindow"]
_logger = logging.getLogger(__name__)

class AssignTimewindow(Node):
    """
    Generate a new column based on event t_0  and period length, a timewindow is assigned.
    """
    NAME = "assign-timewindow"
    DESCRIPTION = "Generate a new column based on event t_0  and period length, a timewindow is assigned."
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be assigned to a timewindow",
            "required": True,
        },
    ]
    PARAMETERS = {
        "time_column": {
            "id": "time_column",
            "name": "time_column",
            "description": """The time_column which is the base to identify the time window, which is assigned""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "time_window": {
            "id": "time_window",
            "name": "time_window",
            "description": """The time_window which indicates the window tshe event belongs to with respect to starting time and period""",
            "type": "string",
            "required": False,
            "value": "new_time_iterator_column",
            "multipleValues": False
        },
        "start_time": {
            "id": "start_time",
            "name": "start_time",
            "description": """The timewindow is based on the start time, which can be a column or a fixed value""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
         "time_unit": {
            "id": "time_unit",
            "name": "time_unit",
            "description": "The unit of the period, e.g. minutes, days",
            "type": "string",
            "required": True,
            "value": "hours",
            "allowedValues": ["hours","minutes","seconds","days","weeks","months","years"],
            "multipleValues": False
        },
         "number_period": {
            "id": "number_period",
            "name": "number_period",
            "description": "The number of periods",
            "type": "integer",
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
            new_column_name=self.parameters["time_window"].value
            new_column_type =  "numerical"
            output_metadadata['features'].append(
                {
                    "name": new_column_name,
                    "type": new_column_type
                })
            return output_metadadata
        raise TypeError("Please check that the inputs are connected and the results are ready!")
    
    
    def run(self) -> None:
        """ """
        super().run()

        time_column = self.parameters["time_column"].value
        t0 = self.parameters["start_time"].value
        time_unit = self.parameters["time_unit"].value
        number_period = self.parameters["number_period"].value
        time_window = self.parameters["time_window"].value
      
        output_meta = self.define_output_metadata(input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)
        try:
           for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                chunk[time_window] = (assign_to_timewindow(chunk,time_column, t0, number_period, time_unit))
                if not self.write_output(chunk):
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
        except Exception as e:
            _logger.error("Failed to add new column: %s", e)
            raise Exception(f"Failed to add new column (module {self.NAME}): {e}") from e

def assign_to_timewindow(df: DataFrame, t:str, t0:str, number_period, time_unit):
    if t0 in df.columns:
        return  get_time_window(df[t], df[t0], number_period, time_unit)
    return  get_time_window(df[t], t0, number_period, time_unit)

def convert_to_datetime(t0: Series |str ):
    if isinstance(t0, pd.Series):
        return convert_column_to_datetime(t0)
    if isinstance(t0, (pd.Timestamp, str)):
        return convert_value_to_datetime(t0)
    raise TypeError("Input must be a pandas Series or a single value of type datetime or str.")

def convert_value_to_datetime(t0):
    return  pd.Timestamp(t0)

def convert_column_to_datetime(column: Series):
    if pd.api.types.is_datetime64_any_dtype(column):
        return column
    if pd.api.types.is_string_dtype(column):
        column = pd.to_datetime(column, errors='coerce')
        if column.isna().any():
            raise ValueError("Some values could not be converted to datetime.")
        return column
    else:
        raise TypeError(f"Column must be of type string or datetime, but got {column.dtype}")

def get_timedelta(t:Series, t0: Series |str ):
    t0_= convert_to_datetime(t0)
    t_=convert_column_to_datetime(t)
    return t_-t0_

def define_period(number:int, time_unit:str):
    time_unit_mappings = {
        'hours': 'h',
        'minutes': 'min',
        'seconds': 'S',
        'days': 'D',
        'weeks': 'W',
        'months': 'M',
        'years': 'Y'
    }
    return f"{number}{time_unit_mappings[time_unit]}"
    
def get_period(number:int, time_unit:str):
    period=define_period(number,time_unit)
    return pd.to_timedelta(period)
    
def get_time_window(t:Series,t0: Series |str , number:int, time_unit:str):
    period_timedelta = get_period(number, time_unit)
    timedeltas=get_timedelta(t,t0)
    timewindows = (timedeltas // period_timedelta)
    return timewindows
