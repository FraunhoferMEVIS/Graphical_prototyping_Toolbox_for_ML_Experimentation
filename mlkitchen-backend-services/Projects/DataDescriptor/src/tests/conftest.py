""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: configuring the tests
-----------------------------------------------------------------------------
"""
import os
import shutil
import pytest
from starlette.testclient import TestClient
from serve import app

TEST_PROJECT = 'test_project'
SAMPLE_METADATA = {
  "data_type": ["tabular"],
  "target": "trip_duration",
  "keys": [],
  "features": [
    {
      "name": "pickup_dow",
      "type": "categorical"
    },
    {
      "name": "pickup_hour",
      "type": "categorical"
    },
    {
      "name": "trip_distance",
      "type": "numerical"
    },
    {
      "name": "trip_duration",
      "type": "numerical"
    }
  ]
}


@pytest.fixture(scope='module')
def client():
    """
    client for testing the app
    """
    yield TestClient(app)


@pytest.fixture(scope="function")
def sample_metadata():
    return SAMPLE_METADATA


@pytest.fixture(scope="function")
def sample_project():
    yield TEST_PROJECT

    if os.path.exists(os.path.join('projects', TEST_PROJECT)):
      shutil.rmtree(os.path.join('projects', TEST_PROJECT))
