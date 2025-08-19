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
from copy import deepcopy
import pytest
from starlette.testclient import TestClient
from aisandbox_server import app
from src.backend.project import AISANDBOX_PROJECTS_FOLDER


@pytest.fixture(scope='module')
def client():
    """
    client for testing the app
    """
    yield TestClient(app)


PROJECT_NAME = "example"
USERNAME = "etag"
TARGET_COL = "y"
SPLIT_CONFIG = {
    "ratio": [0.75, 0.15, 0.1],
}
IMPUTATION_CONFIG = [
        {
            "name": "Median",
            "all_numerical": True
        }]

NEW_FEATURE = [
        {"name": "day_of_the_week", "column_name": "pickup_dow",
         "parameters": {"base_column_name": "tpep_pickup_datetime"}},
        {"name": "hour", "column_name": "pickup_hour",
         "parameters": {"base_column_name": "tpep_pickup_datetime"}},
        {"name": "duration", "column_name": "trip_duration",
         "parameters": {"base_column_name": "tpep_dropoff_datetime",
                        "eventdate_column_name": "tpep_pickup_datetime"}},
        {"name": "operate", "column_name": "diff",
         "parameters": {"first_column_name": "dropoff_zip",
                        "second_column_name": "pickup_zip",
                        "operator_": 'sub'}},
        {"name": "round", "column_name": "diff_rounded",
         "parameters": {"base_column_name": "difference",
                        "decimals": "1"}},
        {"name": "maximum", "column_name": "max_numeric",
         "parameters": {"column_list": ["trip_distance",
                                        "pickup_zip"],
                        "axis": "columns"}},
        {"name": "flag", "column_name": "flag_num",
         "parameters": {"base_column_name": "trip_distance",
                        "condition_value":  1000,
                        "operator_":  'le'}},
        {"name": "flag", "column_name": "flag_column",
         "parameters": {"base_column_name": "trip_distance",
                        "condition_value": "dropoff_zip",
                        "operator_": 'ge'}},
        {"name": "is_element", "column_name": "elem",
         "parameters": {"base_column_name": "trip_distance",
                        "elements": [1000, 10001, 'e']}},
        {"name": "min", "column_name": "earliest_date",
         "parameters": {"column_list": ['tpep_dropoff_datetime',
                                        'tpep_pickup_datetime'],
                        "axis": 'all'}},
        {"name": "convert_timediff_to_unit",
         "column_name": "trip_duration_in_sec",
         "parameters": {"base_column_name": "tpep_dropoff_datetime",
                        "eventdate_column_name": "tpep_pickup_datetime",
                        "unit": 's'}},
        {"name": "name_of_the_day", "column_name": "pickup_day",
         "parameters": {"base_column_name": "tpep_pickup_datetime"}},
        {"name": "recenter_time_wrt_t0", "column_name": "recentered_drop_off",
         "parameters": {"base_column_name": "tpep_pickup_datetime",
                        "eventdate_column_name": "tpep_dropoff_datetime"}},
        {"name": "recenter_wrt_weekdays_in_unit",
         "column_name": "recentered_drop_off_wrt_weekdays_in_sec",
         "parameters": {"base_column_name": "tpep_pickup_datetime",
                        "eventdate_column_name": "tpep_dropoff_datetime",
                        "unit": 's'}},
        {"name": "time_window", "column_name": "drop_off_time_window_in_h",
         "parameters": {"base_column_name": "tpep_pickup_datetime",
                        "eventdate_column_name": "tpep_dropoff_datetime",
                        "period": 1,
                        "time_length": 24,
                        "unit": 'h'}},]

REGRESSION_METRICS_CONFIG = [
        {
            "name": "root_mean_squared_error",
            "greater_is_better": True,
            "threshold": 10
        }]
CLASSIFICATION_METRICS_CONFIG = [
        {
            "name": "f1_score",
            "greater_is_better": True,
            "threshold": 0.6
        }]

REGRESSION_ESTIMATOR = {
        "name": "RandomForestRegressor",
        "library": "sklearn",
        "language": "python"
    }

REGRESSION_ESTIMATOR_LIST = [{
        "name": "RandomForestRegressor",
        "library": "sklearn",
        "language": "python"
    },
    {
        "name": "SVR",
        "library": "sklearn",
        "language": "python"
    }]

CLASSIFICATION_ESTIMATOR = {
        "name": "RandomForestClassifier",
        "library": "sklearn",
        "language": "python"
    }


FEATURE_SELECTION_ESTIMATOR = {
        "name": "SelectFromModel",
        "library": "sklearn",
        "language": "python",
        "parameters":  {
            "estimators": [
                {
                    'name': "RandomForestClassifier",
                    'parameters': {
                        "C": 1.0,
                        "epsilon": 0.2,
                        }
                }
            ],
            "max_features": 4
        }
    }


FEATURE_SELECTION_STATISTICAL = {
    "name": "SelectKBest",
    "library": "sklearn",
    "language": "python",
    "parameters": {
        'score_func': 'mutual_info_regression',
        'k': 4
    }}


def example_input_regression_config():
    """
    example input config for the regression recipe
    """
    return {
            "project": {
                "name": PROJECT_NAME
            },
            "config": {
                "username": USERNAME,
                "description": "example regression config",
                "task": "regression",
                "target_col": TARGET_COL,
                "split": SPLIT_CONFIG,
                "imputation": IMPUTATION_CONFIG,
                "metrics": REGRESSION_METRICS_CONFIG,
                "primaryMetric": REGRESSION_METRICS_CONFIG[0]["name"],
                "feature_selection": FEATURE_SELECTION_STATISTICAL,
                "estimator": REGRESSION_ESTIMATOR,
                "new_feature": NEW_FEATURE,
                }
            }


@pytest.fixture(scope="function")
def example_input_config():
    """
    example input config for the regression recipe
    """
    return {
        'regression': example_input_regression_config(),
        'classification': example_input_classification_config(),
    }


@pytest.fixture(scope="function")
def example_config_multiple_estimator():
    """
    example input config for the regression recipe
    with multiple estimators as input
    """
    example_regression_config = example_input_regression_config()
    example_regression_config['config']['estimator'] = \
        REGRESSION_ESTIMATOR_LIST
    return example_regression_config


def example_input_classification_config():
    """"
    example input classification config for classification recipe
    """
    return {
        "project": {
            "name": PROJECT_NAME
        },
        "config": {
            "username": USERNAME,
            "description": "example classification config",
            "task": "classification",
            "target_col": TARGET_COL,
            "positive_class": 1,
            "split": SPLIT_CONFIG,
            "imputation": IMPUTATION_CONFIG,
            "metrics": CLASSIFICATION_METRICS_CONFIG,
            "feature_selection": FEATURE_SELECTION_ESTIMATOR,
            "primaryMetric": CLASSIFICATION_METRICS_CONFIG[0]["name"],
            "estimator": CLASSIFICATION_ESTIMATOR,
        }
    }


@pytest.fixture(scope="function")
def expected_recipe():
    """
    example input config for the regression recipe
    """
    return {
        'regression': expected_regression_recipe(),
        'classification': expected_classification_recipe(),
    }


def expected_regression_recipe(n=1):
    """
    expected regression recipe output, based on above sample input.
    """
    _project_path = os.path.join(AISANDBOX_PROJECTS_FOLDER, PROJECT_NAME,
                                 "mlkitchen", f"run{n}")
    estimetor_name = REGRESSION_ESTIMATOR['name'].lower()
    return {
        "recipe": "regression/v1",
        "target_col": TARGET_COL,
        "primary_metric": REGRESSION_METRICS_CONFIG[0]["name"],
        "steps": {
            "ingest": {
                "using": "parquet",
                "location": os.path.join(_project_path, "data",
                                         "data.parquet"),
            },
            "split": {
                "using": "custom",
                "split_method": "split_fn"
            },
            "transform": {
                "transformer_method": "transformer_fn"
            },
            "train": {
                "using": "custom",
                "estimator_method":
                    f"estimator_{estimetor_name}"
                },
            "evaluate": {
                "validation_criteria": [{
                    "metric": metric["name"],
                    "threshold": metric["threshold"],
                } for metric in REGRESSION_METRICS_CONFIG]
            },
            "register": {
                "allow_non_validated_model": True,
                "model_name": f"{PROJECT_NAME}_regression_{estimetor_name}"
            },
            "ingest_scoring": {
                "location": os.path.join(_project_path, 'data',
                                         'data.parquet'),
                "using": "parquet"
            },
            "predict": {
                "output": {
                    "location": os.path.join(_project_path,
                                             'data', 'sample_output.parquet'),
                    "using": "parquet"
                }
            },
        },
        "custom_metrics": [
            {
                "function": f"{metric['name']}_",
                "greater_is_better": metric["greater_is_better"],
                "name": metric["name"],
            } for metric in REGRESSION_METRICS_CONFIG],
    }


def expected_classification_recipe(n=1):
    """
    expected classification recipe, based on above input
    """
    _project_path = os.path.join(AISANDBOX_PROJECTS_FOLDER, PROJECT_NAME,
                                 "mlkitchen", f"run{n}")
    estimator_name = CLASSIFICATION_ESTIMATOR['name'].lower()
    return {
        "recipe": "classification/v1",
        "target_col": TARGET_COL,
        "primary_metric": CLASSIFICATION_METRICS_CONFIG[0]["name"],
        "positive_class":
            example_input_classification_config()["config"]["positive_class"],
        "steps": {
            "ingest": {
                "using": "parquet",
                "location": os.path.join(_project_path, "data",
                                         "data.parquet"),
            },
            "split": {
                "using": "custom",
                "split_method": "split_fn"
            },
            "transform": {
                "transformer_method": "transformer_fn"
            },
            "train": {
                "using": "custom",
                "estimator_method":
                    f"estimator_{estimator_name}",
                "resampling_minority_percentage": 0.000001
            },
            "evaluate": {
                "validation_criteria": [{
                    "metric": metric["name"],
                    "threshold": metric["threshold"],
                } for metric in CLASSIFICATION_METRICS_CONFIG]
            },
            "register": {
                "allow_non_validated_model": True,
                "model_name": f"{PROJECT_NAME}_classification_{estimator_name}"
            },
            "ingest_scoring": {
                "location": os.path.join(_project_path,
                                         'data', 'data.parquet'),
                "using": "parquet"
            },
            "predict": {
                "output": {
                    "location": os.path.join(_project_path,
                                             'data', 'sample_output.parquet'),
                    "using": "parquet"
                }
            },
        },
        "custom_metrics": [
            {
                "function": f'{metric["name"]}_',
                "greater_is_better": metric["greater_is_better"],
                "name": metric["name"],
            } for metric in CLASSIFICATION_METRICS_CONFIG],
    }


@pytest.fixture(scope="function")
def expected_regression_recipe_multiple_estimator():
    """
    expected regression recipe output, based on above sample input.
    """
    expected_result = []
    for n, estimator in enumerate(REGRESSION_ESTIMATOR_LIST):
        estimetor_name = estimator['name'].lower()
        template_recipe = expected_regression_recipe(n+1)
        sample_recipe = deepcopy(template_recipe)
        sample_recipe['steps']['train']['estimator_method'] = \
            f"estimator_{estimetor_name}"
        sample_recipe['steps']['register']['model_name'] = \
            f"{PROJECT_NAME}_regression_{estimetor_name}"
        expected_result.append(sample_recipe)
    return expected_result
