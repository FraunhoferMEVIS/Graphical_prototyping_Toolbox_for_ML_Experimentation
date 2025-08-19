""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: comorbidity.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for getting comorbidities of patients as True or False
-----------------------------------------------------------------------------
"""
import logging
from dateutil import parser
import pandas
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes


__all__ = ["Comorbidity"]
_logger = logging.getLogger(__name__)


class Comorbidity(Node):
    """
    Generate a comorbidity table for an existing or not existing comorbidity.
    """
    NAME = "comorbidity"
    DESCRIPTION = """Generate a new Table based on the input list of ICD codes \
        and the values of a column. Each row if this table contains the input \
        keys combination and the presence ot not presence of the disease."""
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be filtered",
            "required": True,
        },
    ]
    PARAMETERS = {
        "column": {
            "id": "column",
            "name": "column",
            "description": "The column of ICD code.",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "keys": {
            "id": "keys",
            "name": "keys",
            "description": "The keys to be used for grouping. If not given, \
                all keys of input table are used for grouping.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "disease_name": {
            "id": "disease_name",
            "name": "disease_name",
            "description": """The name of disease, a new column with this name will be created \
                with True/False values for presence of the value in the list of ICD
                codes for a specific patient.""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "icd_codes": {
            "id": "icd_codes",
            "name": "icd_codes",
            "description": "The list of ICD codes of the specific diseas.",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "time_dependent": {
            "id": "time_dependent",
            "name": "time_dependent",
            "description": """A flag to extract the comorbidity per input subject/key combination or \
                based on history at each point. For example, if the value is True, and the patient caught
                COVID in 2020, the comorbidity column will have a False value until 2020 and True \
                from 2020 on. If False, the comorbidity column is going to have a value of True for \
                all time points.
                Note: Default value is False. If set to True, then the parameter for time_column is mandatory.
                """,
            "type": "boolean",
            "required": False,
            "value": False,
            "multipleValues": False
        },
        "time_column": {
            "id": "time_column",
            "name": "time_column",
            "description": """It's used, if the value of time_dependent parameter is True. \
                it's used to sort the data ascending.
            """,
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        }
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
            keys = self._get_in_keys(input_metadata)
            disease_name = self.parameters["disease_name"].value
            output_metadata = {
                "keys": keys,
                "features": [
                    {
                        "name": disease_name,
                        "type": "categorical"
                    }
                ]
            }
            return output_metadata

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run_for_page(self, page):
        """
        Implement the comorbidity extraction for an input chunk of data.
        """
        column = self.parameters["column"].value
        disease_name = self.parameters["disease_name"].value
        keys = self._get_in_keys()
        time_dependent = self.parameters["time_dependent"].value or False
        time_column = self.parameters["time_column"].value

        disease_icd_codes = self.parameters["icd_codes"].value

        columns = keys + [column]
        if time_column:
            columns += [time_column]
        result = page.loc[:, columns].copy()
        result[column] = result[column].astype("string")
        result[disease_name] = False
        
        result[disease_name] = result[disease_name].where(~result[column].str.startswith(tuple(disease_icd_codes)), True)
        result = result.drop(columns=[column])
        if not time_dependent:
            result = result.groupby(keys).max().reset_index()
        else:
            if time_column is None:
                raise ValueError("""If the value of 'time_dependent' is set to True, a column \
                                 name should be provided to sort the data per group.""")
            try:
                result[time_column] = result[time_column].map(parser.parse)
            except TypeError:
                _logger("The given column, %s doesn't have the time format. Using it as it is for sorting.",
                        time_column)
            result[disease_name] = result.sort_values(by=[time_column]).groupby(keys)[disease_name].cummax()
        return result


    def run(self) -> None:
        """
          Implement the logic to run the module based on the input configuration.
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
            _logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to run module: %s", e)
            raise Exception(f"Failed to run module: {e}") from e

    def _get_in_keys(self, input_metadata=None) -> list[str]:
        """
        Get the input keys or indices of the table, based on user's input.
        """
        if (keys := self.parameters["keys"].value) is None:
            if input_metadata is None:
                input_metadata=self.get_input_metadata()
            if self.inputs and self.inputs[0].name:
                input_metadata = input_metadata[self.inputs[0].name]
            keys = input_metadata["keys"]
        if isinstance(keys, str):
            keys = [keys]
        return keys