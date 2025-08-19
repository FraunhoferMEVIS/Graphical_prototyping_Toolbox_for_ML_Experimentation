""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 08/2023
description: The test configurations for NewFeature unit tests
-----------------------------------------------------------------------------
"""

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing


@pytest.fixture(scope="function")
def house_prices():
    return fetch_california_housing(as_frame=True)


@pytest.fixture(scope="function")
def dataset_with_timeseries():
    def random_datetimes(start, end, sample_size):
        return pd.to_datetime(np.random.randint(start.value//10**9,
                                                end.value//10**9,
                                                sample_size), unit='s')
    sample_size = 30
    ID = range(sample_size)
    startdate = random_datetimes('2015-01-01', '2016-01-01', sample_size)
    enddate = random_datetimes('2016-02-01', '2017-01-01', sample_size)
    return pd.DataFrame(data={'ID': ID,
                              'startdate': startdate,
                              'enddate': enddate})
