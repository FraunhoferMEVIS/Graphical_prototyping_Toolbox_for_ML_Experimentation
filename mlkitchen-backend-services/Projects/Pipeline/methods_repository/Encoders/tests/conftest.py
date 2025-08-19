""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The test configurations for the Encoder's unit tests
-----------------------------------------------------------------------------
"""

import pytest
from pandas import DataFrame
from sklearn.datasets import fetch_california_housing


@pytest.fixture(scope="function")
def categorical_data():
    data = DataFrame(
        {
            "gender": ["F", "M", "M", "F", "F", "F", "M", "F", "M"],
            "unit": ["B", "A", "B", "A", "B", "A", "A", "A", "A"],
            "ICD": ["I05", "I10", "I05", "N003", "W02", "I05", "98", "N003",
                    "X34"],
            "Type": [1, 2, 3, 2, 3, 1, 2, 1, 1]
        }
    )
    return data


@pytest.fixture(scope="function")
def target_categorical():
    y = DataFrame(
        {
            "target": [0, 1, 1, 1, 0, 0, 1, 1, 0]
        }
    )
    return y


@pytest.fixture(scope="function")
def target_numerical():
    y = DataFrame(
        {
            "target": [0.3, 1.0, 0.1, 0.4, 0.6, 1.0, 0.25, 0.35, 0.05]
        }
    )
    return y


@pytest.fixture(scope="function")
def numerical_data():
    return fetch_california_housing(as_frame=True)


@pytest.fixture(scope="function")
def grouped_numerical_data():
    return DataFrame({
        "ID": [1, 1, 1, 1, 1, 2, 2, 2, 2],
        "gender": ["F", "M", "M", "F", "F", "F", "M", "F", "M"],
        "unit": ["B", "A", "B", "A", "B", "A", "A", "A", "A"],
        "value1": [10, 11, 13, 8, 9, 1, 2, 1, 5],
        "value2": [2, 2, 3, 5, 6, 7, 8, 9, 10]
    })

