""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: new_column.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for a adding a new column to a table
-----------------------------------------------------------------------------
"""
import operator
import logging
import math
import inspect
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes


__all__ = ["NewColumn"]
__logger = logging.getLogger(__name__)


def add(*args):
    return sum(args)


def binary_and(*args):
    result = args[0]
    for arg in args[1:]:
        result &= arg
    return result


def binary_or(*args):
    result = args[0]
    for arg in args[1:]:
        result |= arg
    return result


def binary_xor(*args):
    result = args[0]
    for arg in args[1:]:
        result ^= arg
    return result


def mul(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


def log2(a):
    return math.log(a, 2)


_operators = {
    "+": {
        "method": add,
        "output_type": "numerical"
    }, 
    "add": {
        "method": add,
        "output_type": "numerical"
    },
    "plus": {
        "method": add,
        "output_type": "numerical"
    }, 
    "-": {
        "method": operator.sub,
        "output_type": "numerical"
    },
    "sub": {
        "method": operator.sub,
        "output_type": "numerical"
    },
    "minus": {
        "method": operator.sub,
        "output_type": "numerical"
    },
    "*": {
        "method": mul,
        "output_type": "numerical"
    },
    "mul": {
        "method": mul,
        "output_type": "numerical"
    },
    "times": {
        "method": mul,
        "output_type": "numerical"
    },
    "x": {
        "method": mul,
        "output_type": "numerical"
    },
    "/": {
        "method": operator.truediv,
        "output_type": "numerical"
    },
    "div": {
        "method": operator.truediv,
        "output_type": "numerical"
    },
    "truediv": {
        "method": operator.truediv,
        "output_type": "numerical"
    },
    "//": {
        "method": operator.floordiv,
        "output_type": "numerical",
    },
    "floordiv": {
        "method": operator.floordiv,
        "output_type": "numerical",
    },
    "mod": {
        "method": operator.mod,
        "output_type": "numerical",
    },
    "%": {
        "method": operator.mod,
        "output_type": "numerical",
    },
    "pow": {
        "method": operator.pow,
        "output_type": "numerical",
    },
    "**": {
        "method": operator.pow,
        "output_type": "numerical",
    },
    "<": {
        "method": operator.lt,
        "output_type": "categotical",
    },
    "lt": {
        "method": operator.lt,
        "output_type": "categotical",
    },
    "<=": {
        "method": operator.le,
        "output_type": "categotical",
    },
    "le": {
        "method": operator.le,
        "output_type": "categotical",
    },
    ">": {
        "method": operator.gt,
        "output_type": "categotical",
    },
    "gt": {
        "method": operator.gt,
        "output_type": "categotical",
    },
    ">=": {
        "method": operator.ge,
        "output_type": "categotical",
    },
    "ge": {
        "method": operator.ge,
        "output_type": "categotical",
    },
    "=": {
        "method": operator.eq,
        "output_type": "categotical",
    },
    "eq": {
        "method": operator.eq,
        "output_type": "categotical",
    },
    "equal": {
        "method": operator.eq,
        "output_type": "categorical",
    },
    "==": {
        "method": operator.eq,
        "output_type": "categorical",
    },
    "equals": {
        "method": operator.eq,
        "output_type": "categorical",
    },
    "!=": {
        "method": operator.ne,
        "output_type": "categorical",
    },
    "ne": {
        "method": operator.ne,
        "output_type": "categorical",
    },
    "not equal": {
        "method": operator.ne,
        "output_type": "categorical",
    },
    "neq": {
        "method": operator.ne,
        "output_type": "categorical",
    },
    "&": {
        "method": binary_and,
        "output_type": "numerical",
    },
    "and": {
        "method": binary_and,
        "output_type": "numerical",
    },
    "|": {
        "method": binary_or,
        "output_type": "numerical",
    },
    "or": {
        "method": binary_or,
        "output_type": "numerical",
    },
    "^": {
        "method": binary_xor,
        "output_type": "numerical",
    },
    "xor": {
        "method": binary_xor,
        "output_type": "numerical",
    },
    "<<": {
        "method": operator.lshift,
        "output_type": "numerical",
    },
    "lshift": {
        "method": operator.lshift,
        "output_type": "numerical",
    },
    ">>": {
        "method": operator.rshift,
        "output_type": "numerical",
    },
    "rshift": {
        "method": operator.rshift,
        "output_type": "numerical",
    },
    "not": {
        "method": operator.not_,
        "output_type": "categorical",
    },
    "invert": {
        "method": operator.not_,
        "output_type": "categorical",
    },
    "neg": {
        "method": operator.neg,
        "output_type": "numerical",
    },
    "negative": {
        "method": operator.neg,
        "output_type": "numerical",
    },
    "pos": {
        "method": operator.pos,
        "output_type": "numerical",
    },
    "positive": {
        "method": operator.pos,
        "output_type": "numerical",
    },
    "abs": {
        "method": operator.abs,
        "output_type": "numerical",
    },
    "absolute": {
        "method": operator.abs,
        "output_type": "numerical",
    },
    "round": {
        "method": round,
        "output_type": "numerical",
    },
    "ceil": {
        "method": math.ceil,
        "output_type": "numerical",
    },
    "floor": {
        "method": math.floor,
        "output_type": "numerical",
    },
    "sin": {
        "method": math.sin,
        "output_type": "numerical",
    },
    "cos": {
        "method": math.cos,
        "output_type": "numerical",
    },
    "tan": {
        "method": math.tan,
        "output_type": "numerical",
    },
    "asin": {
        "method": math.asin,
        "output_type": "numerical",
    },
    "acos": {
        "method": math.acos,
        "output_type": "numerical",
    },
    "atan": {
        "method": math.atan,
        "output_type": "numerical",
    },
    "sinh": {
        "method": math.sinh,
        "output_type": "numerical",
    },
    "cosh": {
        "method": math.cosh,
        "output_type": "numerical",
    },
    "tanh": {
        "method": math.tanh,
        "output_type": "numerical",
    },
    "asinh": {
        "method": math.asinh,
        "output_type": "numerical",
    },
    "acosh": {
        "method": math.acosh,
        "output_type": "numerical",
    },
    "atanh": {
        "method": math.atanh,
        "output_type": "numerical",
    },
    "exp": {
        "method": math.exp,
        "output_type": "numerical",
    },
    "log10": {
        "method": math.log10,
        "output_type": "numerical",
    },
    "sqrt": {
        "method": math.sqrt,
        "output_type": "numerical",
    },
    "isinf": {
        "method": math.isinf,
        "output_type": "categorical",
    },
    "isnan": {
        "method": math.isnan,
        "output_type": "categorical",
    },
    "log2": {
        "method": log2,
        "output_type": "categorical",
    }
}


class NewColumn(Node):
    """
    Generate a new column based on the input operator and one or more columns.
    """
    NAME = "new-column"
    DESCRIPTION = "Generate a new column based on the input operator and one or more columns"
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to add column to.",
            "required": True,
        },
    ]
    PARAMETERS = {
        "operator": {
            "id": "operator",
            "name": "operator",
            "description": "The operator to be applied to the columns",
            "type": "string",
            "required": False,
            "value": "+",
            "allowedValues": set(_operators.keys()),
        },
        "new_column": {
            "id": "new_column",
            "name": "new_column",
            "description": """The name of the new column to be created""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": """The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
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
            new_column_name = self.parameters["new_column"].value
            op = self.parameters["operator"].value
            columns = self.parameters["columns"].value
            for feature in output_metadadata['features']:
                if feature['name'] == columns[0]:
                    input_type = feature['type']
                    break
            new_column_type = get_operation_output_type(op, input_type=input_type)
            output_metadadata['features'].append(
                {
                    "name": new_column_name,
                    "type": new_column_type
                })
            return output_metadadata

        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run(self) -> None:
        """
          Implement the logic to add a new column based on the input operator and columns
        """
        super().run()
        if len(self.parameters["columns"].value) < 1:
            raise ValueError("The number of columns should be at least 2")

        op = self.parameters["operator"].value
        columns = self.parameters["columns"].value
        new_column = self.parameters["new_column"].value
        func = string_to_function(op)

        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                chunk[new_column] = chunk.apply(lambda row: func(*row[columns]), axis=1)
                if not self.write_output(chunk):
                    raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            __logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            __logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            __logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            __logger.error("Failed to add new column: %s", e)
            raise Exception(f"Failed to add new column: {e}") from e


def string_to_function(operator_name: str, operators: dict=None) -> callable:
    """
    converts a string to a function
    :param operator_name: the operator to be converted
    operator can be one of the following: 
        +, -, *, /, %, //, **, &, |, ^, >>, <<, ==, !=, >, <, >=, <=, not, and, or, in, not in, 
        pow, pos, neg, abs, invert, round, floor, ceil, sin, cos, tan, asin, acos, atan,
        sinh, cosh, tanh, asinh, acosh, atanh, exp, log, log10, sqrt, isinf, isnan,
        g, isless, le, ge,
    :param operators: list of pre defined operators. If none, the default one is going to be used.
    """ 
    if operators is None:
        operators = _operators
    if operator_name in operators:
        return operators[operator_name]["method"]
    raise ValueError(f"Unknown operator: {operator_name}")


def get_operation_output_type(operator_name: str, input_type: str, operators: dict=None) -> str:
    """
    converts a string to a function
    :param operator_name: the operator to be converted
    :param input_type: the type of the input
    operator can be one of the following: 
        +, -, *, /, %, //, **, &, |, ^, >>, <<, ==, !=, >, <, >=, <=, not, and, or, in, not in, 
        pow, pos, neg, abs, invert, round, floor, ceil, sin, cos, tan, asin, acos, atan,
        sinh, cosh, tanh, asinh, acosh, atanh, exp, log, log10, sqrt, isinf, isnan,
        g, isless, le, ge,
    :param operators: list of pre defined operators. If none, the default one is going to be used.
    """ 
    if operators is None:
        operators = _operators
    if operator_name in operators:
        output_type = operators[operator_name].get("output_type", None)
        if output_type and isinstance(output_type, str):
            return output_type
        if isinstance(output_type, list):
            if input_type == "categorical" and "categorical" in output_type:
                return "categorical"
            if "numerical" in output_type:
                return "numerical"
    raise ValueError(f"Unknown operator: {operator_name}")


def get_num_inputs(func: callable) -> int:
    """
    returns the number of inputs of a function
    :param func: the function to be checked
    """
    parameters = inspect.signature(func).parameters
    if 'args' in parameters:
        return math.inf
    return len(inspect.signature(func).parameters)
