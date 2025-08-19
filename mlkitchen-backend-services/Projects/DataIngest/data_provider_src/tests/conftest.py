""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: configuring the tests
-----------------------------------------------------------------------------
"""

import pytest
from starlette.testclient import TestClient
from serve_data_provider import app


@pytest.fixture(scope='module')
def client():
    """
    client for testing the app
    """
    yield TestClient(app)
