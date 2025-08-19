""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The test configurations for the HandlingMissingValues unit tests
-----------------------------------------------------------------------------
"""

import pytest
from .samples import patient1, patient2, patient2_imputed


@pytest.fixture(scope="function")
def example_train_patient():
    return patient1


@pytest.fixture(scope="function")
def example_test_patient():
    return patient2


@pytest.fixture(scope="function")
def example_test_patient_imputed():
    return patient2_imputed
