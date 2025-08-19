""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: __init__.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: Defines utility functions for creating column transformers (e.g., encoders, imputers) 
                based on attribute settings and dynamically inferring parameter types for algorithms.
                It groups columns with similar preprocessing  requirements into pipelines and uses
                hashing to ensure unique transformation configurations.
-----------------------------------------------------------------------------
"""

import inspect
import json
from typing import Any
from sklearn.compose import make_column_selector
from sklearn.pipeline import Pipeline
from methods_repository.abstraction import ModuleFinder, jsonify_values


def column_selector_by_name(column_names: list[str]):
    pattern = r"^(?:" + "|".join(column_names) + ")$"
    return make_column_selector(pattern=pattern)


def get_column_transformers(attributes: dict) -> list[(str, object, list[str])]:
    """
    get all required transformers for the encoders or imputers defined in the input attributes
    :param attributes: the input attributes and their settings
    """
    column_transformer = {}
    key_columns = []
    for attribute_name, attribute_settings in attributes.items():
        if attribute_settings['type'] == "key":
            key_columns.append(attribute_name)
            continue
        hashed_settings = {"encoders": {
                                "key": "",
                                "method_name": "",
                                "parameters": {}
                            },
                           "imputer": {
                                "key": "",
                                "method_name": "",
                                "parameters": {}
                            }
                           }
        for step in ("encoders", "imputer"):
            if step in attribute_settings:
                for setting in attribute_settings[step]:
                    method_name = setting.get("name")
                    if not method_name:
                        continue
                    parameters = setting.get("parameters", {})

                    hashed_settings[step]["key"] = method_name + __dict_to_str(parameters)
                    hashed_settings[step]["method_name"] = method_name
                    hashed_settings[step]["parameters"] = parameters

        key_name = hashed_settings["encoders"]["key"] + hashed_settings["imputer"]["key"]
        if  key_name not in column_transformer:
            column_transformer[key_name] = {
                "settings": {
                    "encoders": hashed_settings["encoders"],
                    "imputer": hashed_settings["imputer"]
                },
                "columns": [attribute_name]
            }
        else:
            column_transformer[key_name]["columns"].append(attribute_name)


    steps = []
    for setting in column_transformer.values():
        encoders_method_name = setting["settings"]["encoders"]["method_name"]
        encoders_parameters = setting["settings"]["encoders"]["parameters"]
        imputer_method_name = setting["settings"]["imputer"]["method_name"]
        imputer_parameters = setting["settings"]["imputer"]["parameters"]
        columns = setting["columns"]
        # steps = []
        if imputer_method_name:
            if 'columns' not in imputer_parameters:
                imputer_parameters['columns'] = column_selector_by_name(columns)
            steps.append((f"{imputer_method_name}_imputer",
                          ModuleFinder.use_method(
                            'HandlingMissingValues',
                            imputer_method_name,
                            **imputer_parameters)))

        if encoders_method_name:
            if 'columns' not in encoders_parameters:
                encoders_parameters['columns'] = column_selector_by_name(columns)
            steps.append((f"{encoders_method_name}_encoder",
                          ModuleFinder.use_method(
                            'Encoders',
                            encoders_method_name,
                            **encoders_parameters)))
    if steps:
        return ('transformers', Pipeline(steps=steps))
    return None


def __dict_to_str(input_dict: dict) -> str | None:
    """
    Hash a dictionary.

    This function takes a dictionary as input and returns a string that represents a hash of the dictionary.
    The dictionary is first converted to a JSON string with sorted keys, and then this string is returned.

    :param input_dict: The input dictionary to be hashed.
    :return: A string that represents a hash of the input dictionary.
    """
    try:
        unique_str = json.dumps(input_dict, sort_keys=True)
    except TypeError:
        unique_str = repr(input_dict)
    return unique_str



def get_generic_parameter_type_and_options(algorithm: callable, param_name: str, features: Any = None):
    param_type = None
    param_options = None

    default = features.default
    if default is not None and type(default).__name__ in {'int', 'float', 'bool'}:
        param_type = type(default).__name__
    elif hasattr(algorithm, '_parameter_constraints'):
        if param_name not in algorithm._parameter_constraints:
            param_type = None
        elif param_name in {'random_state', 'seed', 'n_jobs'}:
            param_type = 'int'
        else:
            for t in algorithm._parameter_constraints[param_name]:
                if t:
                    if t in {str, int, float}:
                        param_type = t.__name__
                    if t in {list, 'array-like'}:
                        param_type = 'list'
                    if hasattr(t, 'numerator') and hasattr(t, 'denominator'):
                        param_type = 'int' if param_name.startswith('n_') else 'float'
                    if hasattr(t, 'options'):
                        param_type = 'Enum'
                        param_options = [jsonify_values(option) for option in t.options]
                    if hasattr(t, 'left') and hasattr(t, 'right'):
                        param_type = type(t.left).__name__ if 'left' in t.closed else type(t.right).__name__ if t.closed == 'right' else 'float'
    elif features.annotation != inspect._empty:
        if type(features.annotation).__name__ == 'UnionType':
            type_name = features.annotation.__args__[0]
            param_type = str(type_name) if type_name.__name__.startswith('list') else type_name.__name__
        else:
            if type(features.annotation).__name__ == 'EnumType':
                param_options = [opt.name for opt in features.annotation]
            type_name = features.annotation
            param_type = str(features.annotation) if type_name.__name__.startswith('list') else type_name.__name__
    return param_type, param_options


__all__ = ["get_column_transformers"]
