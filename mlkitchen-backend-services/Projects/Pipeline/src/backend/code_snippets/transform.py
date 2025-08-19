""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: transform.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The code for running transformation on the input data
-----------------------------------------------------------------------------
"""
import os
from pandas import DataFrame
import yaml
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from methods_repository import get_column_transformers, ModuleFinder


def transformer_fn():
    """
    Returns an *unfitted* transformer that defines ``fit()`` and \
    ``transform()`` methods. The transformer's input and output \
    signatures should be compatible with scikit-learn transformers.
    """

    steps = get_function_transformers()

    if (transformer := get_drop_columns_transformer()):
        steps.append(transformer)

    with open(os.path.join('steps', 'attributes.yml'),
              'r', encoding="utf-8") as stream:
        attributes = yaml.safe_load(stream)

    if column_transformers := get_column_transformers(attributes):
        steps.append(column_transformers)

    if (transformer := get_feature_selection_transformer()):
        steps.append(transformer)

    return Pipeline(steps=steps)
