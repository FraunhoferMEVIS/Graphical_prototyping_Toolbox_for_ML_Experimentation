""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: methods_list.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The main functionality to get information about the developed
             methods
-----------------------------------------------------------------------------
"""

from enum import Enum
from typing import Annotated
import inspect
import importlib
from fastapi import Depends
from methods_repository import get_generic_parameter_type_and_options
from methods_repository.config_models import ProgrammingLanguages
from methods_repository.abstraction import get_algorithm_list, jsonify_values
from src.models.methods import MethodMetadata, MethodParameters, Steps


def get_step_filters(step: Steps):
    filters = set()
    for language in ProgrammingLanguages:
        for _, definition in \
                get_algorithm_list(step.value, language.value).items():
            filters.update((definition['flags'])
                           if 'flags' in definition else [])
    return [f if isinstance(f, str) else f.value for f in filters]


class Filters(str, Enum):
    """
    list of all possible filters
    """
    _ignore_ = 'step filters_set definition language algorithm member cls'
    cls = vars()
    filters_set = set()
    for step in Steps:
        for language in ProgrammingLanguages:
            for algorithm, definition in \
                 get_algorithm_list(step.value, language.value).items():
                filters_set.update(get_step_filters(step))
    for member in filters_set:
        if issubclass(type(member), Enum):
            cls[member.name] = member.value
        elif isinstance(member, str):
            cls[member] = member


def filter_methods_by_flags(methods: dict,
                            filters: list[Filters],
                            step: Steps
                            ) -> list[dict]:
    """
    Filters the list of methods, that are represented as dictionaries with a
    list of filters. Each method dictionary, can have multiple keys,
    including the "name", "import", and optionally "flags".
    If the "flags" of the given contain all input filters list,
    then the method will be returned as output.
    example methods = [
      "VarianceThreshold": {
            "import": "sklearn.feature_selection",
            "name": "VarianceThreshold",
            "flags": [TaskTypes.feature_selection],
        },
        "AffinityPropagation": {
            "import": "sklearn.cluster",
            "name": "AffinityPropagation",
            "flags": [TaskTypes.clustering],
        },
        "AgglomerativeClustering": {
            "import": "sklearn.cluster",
            "name": "AgglomerativeClustering",
            "flags": [TaskTypes.clustering],
        }
    ]
    let's assume that filters = [clustering]
    then the output will be:
    "AffinityPropagation": {
            "import": "sklearn.cluster",
            "name": "AffinityPropagation",
            "flags": [TaskTypes.clustering],
        },
        "AgglomerativeClustering": {
            "import": "sklearn.cluster",
            "name": "AgglomerativeClustering",
            "flags": [TaskTypes.clustering],
        }
    """
    step_filters = get_step_filters(step)
    filters_of_step = [f for f in filters
                       if f in step_filters]
    filtered_methods = []
    for method, value in methods.items():
        for f in filters_of_step:
            if "flags" not in value:
                break
            if f.lower() in value["flags"]:
                filtered_methods.append(method)
    return filtered_methods


def get_step_modules(step: Steps,
                     filters: Annotated[Filters, Depends(get_step_filters)]
                     ) -> dict:
    """
    returns the list of implemented algorithms in a given step, based on the
    input filters.
    If no filters are given, the list of all algorithms are returned.
    """
    if step not in Steps:
        raise TypeError()
    module = importlib.import_module(
        f'methods_repository.{step.value}.{step.value}')
    implemented_algorithms = getattr(module, 'List_of_Algorithms')
    algorithms = []
    for language in implemented_algorithms:
        algorithms.append({
            "language": language.value,
            "algorithms": filter_methods_by_flags(
                    implemented_algorithms[language],
                    filters, step) if filters else
            list(implemented_algorithms[language])
        })
    return {"algorithms": algorithms}


def _get_param_doc(algorithm: callable, param_name: str):
    return None


def get_step_parameters_and_options(step: Steps, algorithm_name: str, parameter) -> dict:
    """
    Get the type and options of the parameter for the given algorithm in the given step.
    """
    param_type, param_options = None, None
    step_module = importlib.import_module(
        f"methods_repository.{step.value}.{step.value}")
    if hasattr(step_module, "get_parameter_type_and_options"):
        param_type, param_options = step_module.get_parameter_type_and_options(algorithm_name, parameter)
    
    return param_type, param_options


def _get_min_max_values(algorithm, param_name):
    param_min = param_max = None
    
    if hasattr(algorithm, '_parameter_constraints'):
        if param_name not in algorithm._parameter_constraints:
            return param_min, param_max
        
        for t in algorithm._parameter_constraints[param_name]:
            if t:
                if hasattr(t, 'left'):
                    param_min = t.left
                if hasattr(t, 'right'):
                    param_max = t.right
    return param_min, param_max


def _get_algorithm_parameters(algorithm, indices_of_input_data, step = None):
    parameters = []            
    input_variables = inspect.signature(algorithm)
    for n, (key, val) in enumerate(input_variables.parameters.items()):
        if key in {'kwargs', '_', 'args'} or step == Steps.Distributions and key == 'kwds':
            continue
        if n in indices_of_input_data:
            val_decoded = 'NOT_FOR_FRONTEND'
        elif val.default is inspect._empty:
            val_decoded = "MANDATORY_INPUT"
        else:
            val_decoded = jsonify_values(val.default)


        param_type, options = get_generic_parameter_type_and_options(algorithm, key, val)
        if param_type is None:
            # Get step specific parameter type and options
            param_type, options = get_step_parameters_and_options(step, algorithm.__name__, key)

        if (param_type) is None:
            # if the type is not found, skip the parameter to use the default value
            if val_decoded not in {'MANDATORY_INPUT'}:
                continue
            
        if param_type in {'int', 'float'}:
            param_min, param_max = _get_min_max_values(algorithm, key)
        else:
            param_min = param_max = None

        parameters.append(MethodParameters(
            name=key,
            type=param_type,
            default=val_decoded,
            help=_get_param_doc(algorithm, key),
            options=options,
            min=param_min,
            max=param_max
        ))
    return parameters


def get_algorithm_metadata(step: Steps, alg: str) -> MethodMetadata:
    """
    find the help and parameters for a given algorithm in a given step.
    """
    if step not in Steps:
        raise TypeError()

    step_module = importlib.import_module(
        f"methods_repository.{step.value}.{step.value}")

    for language in ProgrammingLanguages:
        if language in step_module.List_of_Algorithms and \
             alg in step_module.List_of_Algorithms[language]:
            algorithm_info = step_module.List_of_Algorithms[language][alg]
            algorithm = getattr(
                importlib.import_module(algorithm_info['import']),
                algorithm_info['name']
            )
            module_help = inspect.getdoc(algorithm).split('\nExamples\n--------', maxsplit=1)[0]

            # Get the input parameters of the method
            indices_of_input_data = []
            if hasattr(step_module, 'INDICES_OF_DATA_INPUT'):
                indices_of_input_data = step_module.INDICES_OF_DATA_INPUT

            return MethodMetadata(
                programming_language=language,
                step = step,
                name = alg,
                help = module_help,
                parameters = _get_algorithm_parameters(algorithm, indices_of_input_data, step=step),
            )

    raise ValueError(f"Invalid algorithm: {alg} for the Step: {step.value}.")

