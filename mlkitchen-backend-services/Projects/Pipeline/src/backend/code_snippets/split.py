""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: split.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The custom code to get pre-splitted data for each recipe.
The indices are going to be provided via Data Provider Service.
-----------------------------------------------------------------------------
"""

import os
import pickle
import base64
import requests
from pandas import Series, DataFrame


def split_fn(dataset: DataFrame) -> Series:
    """
    The input Dataframe is not required here,
    but it has to be passed in as it is necessary for the MLFlow recipes.
    The splitting algorithms is going to run only once, before starting
    the recipes. The recipes only get the split indices from the
    DataProvider service.
    """
    n = len(dataset)
    if not (DATA_PROVIDER_URL := os.environ.get('DATA_PROVIDER_URL')):
        raise ValueError("""The DataProvider URL is not provided!""")

    SPLIT_NUMBER = os.environ.get('SPLIT_NUMBER') or '0'
    PROJECT_ID = os.environ.get('PROJECT_ID')
    TIME_OUT = 300  # sec
    try:
        # get the splits
        splits = requests.get(
            f'{DATA_PROVIDER_URL}/{PROJECT_ID}/{SPLIT_NUMBER}/indices',
            timeout=TIME_OUT)
        # Check if the response was successful
        splits.raise_for_status()
        splits = pickle.loads(
            base64.b64decode(splits.json()['indices'].encode()))
    except requests.exceptions.Timeout as e:
        raise TimeoutError(
            f"Error: Request timed out after {TIME_OUT} seconds") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e) from e
    total_num_in_split = len(splits)
    if total_num_in_split < n:
        raise Warning("""Some of the samples in the dataset are not used \
                         in either of TRAINING, VALIDATION, or TEST indices.\
                      """)
    if total_num_in_split > n:
        raise IndexError(f"""Too many indices, compared to the number of \
                          samples!
                          n = {n}
                          indices length = {total_num_in_split}""")
    return splits
