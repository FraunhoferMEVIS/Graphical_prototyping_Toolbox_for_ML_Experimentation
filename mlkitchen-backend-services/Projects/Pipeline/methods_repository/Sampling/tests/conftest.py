""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The test configurations for the Sampling unit tests
-----------------------------------------------------------------------------
"""

import os
import pytest
from sklearn.datasets import load_iris, fetch_california_housing, \
                             load_breast_cancer
import pandas as pd
import numpy as np


@pytest.fixture(scope="function")
def iris_dataset():
    return load_iris(as_frame=True)


@pytest.fixture(scope="function")
def house_prices():
    return fetch_california_housing(as_frame=True)


@pytest.fixture(scope="function")
def breast_cancer():
    return load_breast_cancer(as_frame=True)


@pytest.fixture(scope="function")
def example_patients():
    example_data_set = pd.read_csv(os.path.join("methods_repository",
                                                "DataSplitting", "tests",
                                                "sample_patients.txt"),
                                   sep=" ")
    example_data_set.set_index(['subject_id', 'hadm_id', 'period'],
                               inplace=True)
    example_data_set['gender'] = np.where(example_data_set.gender == 'F', 1, 0)
    return example_data_set.dropna()
