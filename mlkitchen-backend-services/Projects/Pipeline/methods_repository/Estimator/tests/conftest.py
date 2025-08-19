""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The test configurations for the Estimator's unit tests
-----------------------------------------------------------------------------
"""

import pytest
from sklearn.datasets import load_iris, fetch_california_housing
from .samples import  data_set_ts


@pytest.fixture(scope="function")
def iris_dataset():
    return load_iris(as_frame=True)


@pytest.fixture(scope="function")
def house_prices():
    return fetch_california_housing(as_frame=True)


@pytest.fixture(scope="function")
def example_data_set_timeseries():
    return data_set_ts