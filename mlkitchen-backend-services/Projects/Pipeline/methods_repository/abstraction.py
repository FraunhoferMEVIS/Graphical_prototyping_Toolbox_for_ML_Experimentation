""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: abstraction.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The abstraction layer for finding modules in the methods
             repository with specified input parameters
-----------------------------------------------------------------------------
"""

import importlib
import inspect
import numpy as np
from .config_models import ProgrammingLanguages, FeatureSelectionTypes


def jsonify_values(val):
    dictionary = {
        "nan": "numpy.nan",
        "None": None,
        "null": None,
        "inf": "numpy.inf",
        "-inf": "-numpy.inf"
    }
    if str(val) in dictionary:
        return dictionary[str(val)]
    if str(val).startswith('<class'):
        return str(val)[8:-2]
    return val


def _import_class_from_package(package_name: str,
                               class_name: str) -> object:
    """
    imports the module for the given method in the package.
    Note: It just returns the imported object.
          The initialization will be running afterwards.
    """
    al = importlib.import_module(package_name)
    module = getattr(al, class_name)
    return module


def _get_input_parameters_of(func: callable):
    return inspect.signature(func).parameters


def _filter_function_kwargs(func: callable, **kwargs):
    function_inputs = _get_input_parameters_of(func)
    function_inputs_names = [
        param.name for param in function_inputs.values()]
    filtered_kwargs = {
        filter_key: _dejsonify_values(kwargs[filter_key])
        for filter_key in function_inputs_names if filter_key in kwargs
    }
    return filtered_kwargs


def _does_expect_parameter_name(func: callable, param_name: str):
    func_inputs = _get_input_parameters_of(func)
    filter_keys = [param.name for param in func_inputs.values()]
    return param_name in filter_keys


def get_algorithm_list(step: str, language: ProgrammingLanguages):
    module = importlib.import_module(f"methods_repository.{step}.{step}")
    algorithm_list = getattr(module, "List_of_Algorithms")
    if language == ProgrammingLanguages.Python:
        return algorithm_list.get(ProgrammingLanguages.Python) or {}
    if language == ProgrammingLanguages.R:
        return algorithm_list.get(ProgrammingLanguages.R) or {}

    raise AttributeError(
        f"The programming language {language}, currently is not supported.")


def get_kernels_list(language: ProgrammingLanguages):
    module = importlib.import_module("methods_repository.Estimator.Estimator")
    algorithm_list = getattr(module, "List_of_Kernels")
    if language.lower() == 'python':
        return algorithm_list[ProgrammingLanguages.Python]
    if language.lower() == 'r':
        return algorithm_list[ProgrammingLanguages.R]

    raise AttributeError(
        f"The programming language {language}, currently is not supported."
        )


def _get_layer_list(language: ProgrammingLanguages):
    module = importlib.import_module("methods_repository.Estimator.Estimator")
    algorithm_list = getattr(module, "List_of_KerasLayers")
    if language.lower() == 'python':
        return algorithm_list[ProgrammingLanguages.Python]
    raise AttributeError(
        f"The programming language {language}, currently is not supported."
        )

def _get_hyper_parameter_tuning_module(tuning_method: str,
                                       objective: object,
                                       language='Python',
                                       **kwargs) -> object:
    """
    This is the fnction that returns the hyper parameter tuning object.
    It should return an object that has a "fit" method that will be required
    for training.
    """
    if 'search_space' not in kwargs:
        raise ValueError(
            "The search_space is a mandatory input for hyperparameter tuning."
        )
    search_space = {}
    for param, setting in kwargs['search_space'].items():
        if not (("values" in setting) ^ ("function" in setting)):
            raise ValueError("Either 'values' or 'function' should " +
                             "be given as the type of the search space " +
                             "for the given parameter.")
        if "values" in setting:
            search_space[param] = setting["values"]
        else:
            algorithms = get_algorithm_list('Distributions',
                                            language)
            if (distribution_name := setting['function']):
                D = _import_class_from_package(
                        algorithms[distribution_name]['import'],
                        algorithms[distribution_name]['name']
                    )
            else:
                raise ValueError(
                    f'{distribution_name} is not a known distribution.')
            if "parameters" in setting:
                parameters = setting["parameters"]
                search_space[param] = D(**parameters)
    del kwargs['search_space']

    algorithm_list = get_algorithm_list('HyperparameterTuning', language)
    if tuning_method in algorithm_list:
        HPT = _import_class_from_package(
                    algorithm_list[tuning_method]['import'],
                    algorithm_list[tuning_method]['name'])
    else:
        raise AttributeError(
            f"{tuning_method} not found in HyperparameterTuning algorithms.")

    if "scoring" in kwargs:
        algorithm_list = get_algorithm_list('Metric', language)
        metric = _import_class_from_package(
            algorithm_list[kwargs["scoring"]]["import"],
            algorithm_list[kwargs["scoring"]]["name"]
        )
        kwargs["scoring"] = metric
    cleaned_args = _filter_function_kwargs(HPT, **kwargs)
    return HPT(objective, search_space, **cleaned_args)


class ModuleFinder():
    @staticmethod
    def use_method(step_mlkitchen: str,
                   method: str,
                   language: ProgrammingLanguages =
                   ProgrammingLanguages.Python,
                   **kwargs):
        algorithm_list = get_algorithm_list(step_mlkitchen, language)

        if method in algorithm_list:
            M = _import_class_from_package(algorithm_list[method]['import'],
                                           algorithm_list[method]['name'])
            # if the module requires one or a set of estimators as input
            if _does_expect_parameter_name(M, "estimator") or \
               _does_expect_parameter_name(M, "estimators"):
                if 'estimator' in kwargs:
                    input_estimators = [kwargs['estimator']]
                    key_name = 'estimator'
                elif 'estimators' in kwargs:
                    input_estimators = kwargs['estimators']
                    key_name = 'estimators'
                else: 
                    input_estimators = None
                    key_name = None
                if input_estimators:
                    estimators = []
                    for e in input_estimators:
                        parameters = e['parameters'] if 'parameters' in e \
                                                     else {}
                        estimator_obj = (e['name'],
                                         ModuleFinder.use_method("Estimator",
                                                                 e['name'],
                                                                 **parameters
                                                                 ))
                        estimators.append(estimator_obj)
                    del kwargs[key_name]
                    if _does_expect_parameter_name(M, "estimator"):
                        kwargs["estimator"] = estimators[0][1]
                    else:
                        kwargs["estimators"] = estimators
            # if the module requires one or several kernels
            if _does_expect_parameter_name(M, "kernel") or \
               _does_expect_parameter_name(M, "kernels"):
                if 'kernel' in kwargs:
                    kernels = []
                    for k in kwargs['kernel']:
                        parameters = k['parameters'] if 'parameters' in k \
                                                     else {}
                        kernels.append(
                            KernelFinder.use_method(k['name'],
                                                    language=language,
                                                    **parameters))
                    del kwargs['kernel']
                    if _does_expect_parameter_name(M, 'kernel'):
                        kwargs['kernel'] = kernels[0]
                    elif _does_expect_parameter_name(M, 'kernels'):
                        kwargs['kernels'] = kernels

            if _does_expect_parameter_name(M, "layers"):
                if 'layers' in kwargs:
                    layers = []
                    for l in kwargs['layers']:
                        parameters = l['parameters'] if 'parameters' in l else {}
                        layers.append(
                            LayerFinder.use_method(l['name'],
                                                    language=language,
                                                    **parameters))
                    kwargs['layers'] = layers

            if (step_mlkitchen == 'FeatureSelection') and \
               (FeatureSelectionTypes.statistical_based in
                    algorithm_list[method]['flags']):
                if 'score_func' in kwargs:
                    algorithms = get_algorithm_list('StatisticalFunctions',
                                                    language)

                    if (scoring_func_name := kwargs['score_func']):
                        S = _import_class_from_package(
                                algorithms[scoring_func_name]['import'],
                                algorithms[scoring_func_name]['name']
                            )
                        kwargs['score_func'] = S
                    else:
                        raise ValueError(
                         f"{scoring_func_name} isn't a known scoring function."
                         )
                else:
                    raise ValueError('Please define a scoring function')

            cleaned_args = _filter_function_kwargs(M, **kwargs)
            M_object = M(**cleaned_args)
            if 'hyper_parameter_tuning' in kwargs:
                return _get_hyper_parameter_tuning_module(
                                    kwargs['hyper_parameter_tuning'],
                                    M_object,
                                    language=language,
                                    **kwargs)
            return M_object
        raise AttributeError(
            f"The method {method} is not supported for {step_mlkitchen}.")


class LayerFinder():
    @staticmethod
    def use_method(layer_name, language="Python", **kwargs):
        layers=[]
        layers_list = _get_layer_list(language)
        if layer_name in layers_list:
            layer_module = _import_class_from_package(
                layers_list[layer_name]['import'],
                layers_list[layer_name]['name'])
            if _does_expect_parameter_name(layer_module, "layers"):
                if 'layers' in kwargs:
                    for l in kwargs['layers']:
                        parameters = l['parameters'] if 'parameters' in l \
                                                     else {}
                        layers.append(LayerFinder.use_method(l['name'],
                                                               **parameters))
                    kwargs['layers'] = layers
            cleaned_args = _filter_function_kwargs(layer_module, **kwargs)
            return layer_module(**cleaned_args)
        raise NotImplementedError(
            f"Layer {layer_name} is not implemented yet.")


class KernelFinder():
    @staticmethod
    def use_method(kernel_name, language="Python", **kwargs):
        kernels = []
        kernels_list = get_kernels_list(language)
        if kernel_name in kernels_list:
            kernel_module = _import_class_from_package(
                kernels_list[kernel_name]['import'],
                kernels_list[kernel_name]['name'])
            if _does_expect_parameter_name(kernel_module, "kernel") or \
               _does_expect_parameter_name(kernel_module, "kernels") or \
               kernel_name in {"Product", "Sum"}:
                if 'kernel' in kwargs:
                    for k in kwargs['kernel']:
                        parameters = k['parameters'] if 'parameters' in k \
                                                     else {}
                        kernels.append(KernelFinder.use_method(k['name'],
                                                               **parameters))
                    del kwargs['kernel']
                    if _does_expect_parameter_name(kernel_module, 'kernel'):
                        kwargs['kernel'] = kernels[0]
                    elif _does_expect_parameter_name(kernel_module, 'kernels'):
                        kwargs['kernels'] = kernels
                    elif kernel_name in {"Product", "Sum"}:
                        kwargs['k1'], kwargs['k2'] = kernels[0], kernels[1]

            cleaned_args = _filter_function_kwargs(kernel_module, **kwargs)
            return kernel_module(**cleaned_args)
        raise NotImplementedError(
            f"Kernel {kernel_name} is not implemented yet.")


class UnitNormalizer():
    @staticmethod
    def convert(from_unit, to_unit):
        Units = {
            "volume": {"ml", "cc", "l", "mm3", "cm3", "m3"},
            "area": {"mm2", "cm2", "m2"},
            "length": {"mm", "cm", "m"},
            "weight": {"g", "gr", "kg"},
        }
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        if to_unit in Units["volume"]:
            ...
        elif to_unit in Units["area"]:
            ...


def _dejsonify_values(val):
    dictionary = {
        "numpy.nan": np.nan,
        "None": None,
        "numpy.inf": np.inf,
        "-numpy.inf": -np.inf,
        "null": None,
        "inf": np.inf,
        "-inf": -np.inf,
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        #"numpy.float128": np.float128,
        "numpy.float64": np.float64,
        "numpy.float32": np.float32,
        "numpy.float16": np.float16,
        "numpy.int16": np.int16,
        "numpy.int64": np.int64,
        "numpy.int32": np.int32,
        "numpy.int8": np.int8,
        "numpy.float_": np.float_,
        "numpy.int_": np.int_,
        "numpy.bool_": np.bool_,
        "numpy.str_": np.str_,
    }
    if str(val) in dictionary:
        return dictionary[str(val)]
    return val
