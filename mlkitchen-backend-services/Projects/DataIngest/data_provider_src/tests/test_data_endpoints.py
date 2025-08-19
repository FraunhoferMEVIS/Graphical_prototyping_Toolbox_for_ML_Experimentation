""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_feature_endpoint.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: Testing if the Data Descriptor's Feature andpoints run
             as expected.
-----------------------------------------------------------------------------
"""
import os
import pytest
import numpy as np
from pandas import DataFrame, read_json
from pandas.testing import assert_frame_equal
from data_provider_src.backend.app_config import AISANDBOX_PROJECTS_FOLDER


def test_get_data_endpoints(client):
    """
    Testing if getting list of features work and the output results
    are meaningful
    """
    project_id = "example_project"
    data = DataFrame(np.random.randint(2, size=200).reshape(50, 4),
                     columns=['A', 'B', 'C', 'Y'])
    data_path = os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                             'mlkitchen', 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    data.to_parquet(os.path.join(data_path, 'data.parquet'))

    resp = client.get(f'{project_id}/all')
    assert resp.status_code == 200

    assert_frame_equal(data, read_json(resp.json()))


@pytest.mark.parametrize("task", ['regression', 'classification'])
def test_run_split_default(client, task):
    """
    Testing the "split" endpoint of the data provider
    """
    project_id = "example_project"
    sample_config = {
        "username": "Foo",
        "description": "Test_split",
        "task": task,
        "target_col": "Y",
        "split": {
            "ratio": [0.75, 0.15, 0.1]
        },
        "metrics": [
            {
                "name": "rmse",
                "threshold": 10
            }
        ],
        "primaryMetric": [
            "rmse",
            "mean_squared_error"
        ],
        "estimator": [
            {
                "name": "RandomForestRegressor",
                "library": "sklearn",
                "language": "python"
            }]
    }
    resp = client.post(f'{project_id}/split', json=sample_config)
    assert resp.status_code == 200


@pytest.mark.parametrize("algorithm", ['KFold', 'LeaveOneOut', 'LeavePOut',
                                       'ShuffleSplit'])
def test_run_split_regression(client, algorithm):
    """
    Testing the "split" endpoint of the data provider
    """
    project_id = "example_project"
    sample_config = {
        "username": "Foo",
        "description": "Test_split",
        "task": 'regression',
        "target_col": "Y",
        "split": {
            "ratio": [0.75, 0.15, 0.1],
            "name": algorithm,
            "parameters": {
                'n_splits': 5,
                'test_size': 0.2
            }
        },
        "metrics": [
            {
                "name": "rmse",
                "threshold": 10
            }
        ],
        "primaryMetric": [
            "rmse"
        ],
        "estimator": [
            {
                "name": "RandomForestRegressor",
                "library": "sklearn",
                "language": "python"
            }]
    }
    resp = client.post(f'{project_id}/split', json=sample_config)
    assert resp.status_code == 200

    for n in range(sample_config["split"]["parameters"]["n_splits"]):
        resp = client.get(f'{project_id}/{n}/indices')
        assert resp.status_code == 200

    # test that not more splits than requested are saved
    n = sample_config["split"]["parameters"]["n_splits"]
    resp = client.get(f'{project_id}/{n}/indices')
    assert resp.status_code == 404


@pytest.mark.parametrize("algorithm", ['StratifiedShuffleSplit'])
def test_run_split_classification(client, algorithm):
    """
    Testing the "split" endpoint of the data provider
    """
    project_id = "example_project"
    sample_config = {
        "username": "Foo",
        "description": "Test_split",
        "task": 'classification',
        "target_col": "Y",
        "split": {
            "ratio": [0.75, 0.15, 0.1],
            "name": algorithm,
            "parameters": {
                'n_splits': 5,
                'test_size': 0.2
            }
        },
        "metrics": [
            {
                "name": "accuracy",
            }
        ],
        "primaryMetric": [
            "accuracy",
        ],
        "estimator": [
            {
                "name": "RandomForestRegressor",
                "library": "sklearn",
                "language": "python"
            }]
    }
    resp = client.post(f'{project_id}/split', json=sample_config)
    assert resp.status_code == 200

    for n in range(sample_config["split"]["parameters"]["n_splits"]):
        resp = client.get(f'{project_id}/{n}/indices')
        assert resp.status_code == 200

    # test that not more splits than requested are saved
    n = sample_config["split"]["parameters"]["n_splits"]
    resp = client.get(f'{project_id}/{n}/indices')
    assert resp.status_code == 404
