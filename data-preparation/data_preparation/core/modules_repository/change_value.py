""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: change_value.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 06/2024
description: The module for changing the value of a column of a table inplace
-----------------------------------------------------------------------------
"""
import logging
import operator
from pandas import DataFrame
from data_preparation.core.modules_repository.utils import (
            get_expression_function, validate_expression_code
        )
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import (
                ResultsRepository,  FileResultsRepository, ResultTypes)
__all__ = ["ConvertUnit"]
__logger = logging.getLogger(__name__)


class ConvertUnit(Node):
    """
    Change the value of a column in place.
    """
    NAME = "convert-unit"
    DESCRIPTION = "Changing the value of a column of a table inplace for unit conversion."
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table",
            "required": True,
        },
    ]
    PARAMETERS = {
        "expression": {
            "id": "expression",
            "name": "expression",
            "description": """The arithmetic expression to be applied to the input column. \
              always use "x" as replacement for the value of the column of interest. \
              For example, expression can be pow(x1, 3)/(sqrt(x)-2).
              You can also set a constant value, just by putting 10, to set all values \
              to number 10.\
              
              The following constants can be used in your expressions:

               nan: for not a number,
               e: for mathematical constant e ~ 2.718281828459045
               inf: for mathematical infinit,
               pi: for the matheatical constant pi ~ 3.141592653589793.

              Here are the supported operators:
               +: adding,
               -: subtracting,
               *: multiplication,
               /: division,
               //: floor division,
               %: remainder of division,
               **: power,
               <<: bitwise shift to the left,
               >>: bitwise shift to the right,

              and the following functions:
                pow: for computing power,
                sqrt: square root,
                floor: the largest integer smaller than or equal to the number,
                ceil: the smallest integer larger than or equal to the number,
                log: natural logarithm. it can be used as log(a, 2), where 2 is the base of logarithm.
            """,
            "type": "string",
            "required": True,
            "value": "add",
        },
        "column": {
            "id": "column",
            "name": "column",
            "description": """The column to be used for the operation, \
                The result will be written on the same column.""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "reference_column": {
            "id": "reference_column",
            "name": "reference_column",
            "description": "The reference column for checking the condition.",
            "type": "string",
            "required": False,
            "value": None
        },
        "condition": {
            "id": "condition",
            "name": "condition",
            "description": """The condition for applying the operator. \
              You can set the condition, in case, you want to apply \
              the changes to the values of a column, based on the \
              value of another column.
            """,
            "type": "string",
            "required": False,
            "value": "==",
            "allowedValues": {"==", "<", ">", "<=", ">=", "!=",
                              "startswith", "endswith", "containes"}
        },
        "reference_value": {
            "id": "reference_value",
            "name": "reference_value",
            "description": """The reference value that the reference column \
                           is checked agains, based on the input condition.""",
            "type": "string",
            "required": False,
            "value": None
        }
    }

    _CONDITION_OPS = {
        "==": operator.eq,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "!=": operator.ne,
        "startswith": lambda x, s: x.startswith(s),
        "endswith": lambda x, s: x.endswith(s),
        "contains": lambda x, s: s in x
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
        # Expecting that the type won't change.
        # Numericals remain numerical and categoricals remain categorical.
        if self.inputs and self.inputs[0].name:
            column = self.parameters["column"].value
            if column in input_metadata[self.inputs[0].name]["keys"]:
                __logger.warning("Changing the keys of the table!")
            return input_metadata[self.inputs[0].name]

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run_for_page(self, page: DataFrame) -> DataFrame:
        column = self.parameters["column"].value
        expression = self.parameters["expression"].value
        # change 'x' to 'x1' to match the expression convention in utils
        if isinstance(expression, str):
            expression = expression.replace('x', 'x1')
        ref_column = self.parameters["reference_column"].value
        ref_value = self.parameters["reference_value"].value
        condition = self.parameters["condition"].value
        validate_expression_code(expression, sample_inputs=(page.iloc[0][column],))
        try:
            col_type = str(page.dtypes[ref_column])
            if 'int' in col_type:
                ref_value = int(ref_value)
            elif 'float' in col_type:
                ref_value = float(ref_value)
        except ValueError:
            __logger("The %s column is numerical. Comparison with %s might not work!",
                        ref_column, ref_value)
        row_indices =  self._CONDITION_OPS[condition](page[ref_column], ref_value)
        page.loc[row_indices, column]  = page.loc[row_indices][column].agg(
            get_expression_function(expression, num_inputs=1)
        )

    def run(self) -> None:
        """
          Implement the logic to add a new column based on the input operator and columns
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
                self.run_for_page(chunk)
                if not self.write_output(chunk):
                    raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as exception:
            self.error_message = f"Failed to write output for module {self.NAME}"
            __logger.error(self.error_message)
            raise IOError(self.error_message) from exception
        except NameError as exception:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {exception}."
            __logger.error(self. error_message)
            raise NameError(self.error_message) from exception
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            __logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except Exception as exception:
            __logger.error("Failed to change the value: %s", exception)
            raise Exception(f"Failed to change the value: {exception}") from exception
