""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The test configurations for the DataSplitting unit tests
-----------------------------------------------------------------------------
"""

import pytest
from .samples import data_set, data_set_ts


@pytest.fixture(scope="function")
def example_data_set():
    return data_set


@pytest.fixture(scope="function")
def example_small_data_set():
    return data_set[:100]

@pytest.fixture(scope="function")
def example_data_set_timeseries():
    return data_set_ts

