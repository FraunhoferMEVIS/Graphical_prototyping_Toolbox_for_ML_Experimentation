""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_recipe_endpoint.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: testing the recipe endpoints of the ai-sandbox api
-----------------------------------------------------------------------------
"""
import os
from glob import glob
from copy import deepcopy
from shutil import rmtree
import pytest
from src.backend.project import AISANDBOX_PROJECTS_FOLDER
from src.backend.utilities import load_yaml


@pytest.mark.parametrize("task", ["regression", "classification"])
def test_generate_recepie(client, task, example_input_config,
                          expected_recipe):
    """
    testing generate_regression_recepie
    """
    example_input_task_config = example_input_config[task]
    expected_task_recipe = expected_recipe[task]
    resp = client.post('/recipe/all', json=example_input_task_config)
    if resp.status_code != 200:
        assert resp.text == ""
    assert resp.status_code == 200
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     'mlkitchen'))
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen"))
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen", "data"))
    assert os.path.isfile(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen", "run1", "recipe.yaml"))
    assert os.path.isfile(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen", "cookbook.yaml"))
    generated_cookbook = load_yaml(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen", "cookbook.yaml"))
    assert 'previous' in generated_cookbook
    del generated_cookbook['previous']
    assert generated_cookbook == example_input_task_config['config']
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_input_task_config['project']['name'],
                     "mlkitchen", "run1", "profiles"))
    assert os.path.isdir(os.path.join(
                    AISANDBOX_PROJECTS_FOLDER,
                    example_input_task_config['project']['name'],
                    "mlkitchen", "run1", "steps"))

    generated_config = load_yaml(os.path.join(
        AISANDBOX_PROJECTS_FOLDER,
        example_input_task_config['project']['name'],
        "mlkitchen", "run1", "recipe.yaml"
    ))
    assert generated_config == expected_task_recipe
    rmtree(os.path.join(AISANDBOX_PROJECTS_FOLDER,
                        example_input_task_config['project']['name'],
                        "mlkitchen"))


def test_generate_regression_multiple_estimators_recepie(
                            client,
                            example_config_multiple_estimator,
                            expected_regression_recipe_multiple_estimator):
    """
    testing generate_regression_recepie
    """
    resp = client.post('/recipe/all',
                       json=example_config_multiple_estimator)
    assert resp.status_code == 200
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen"))
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen"))
    assert os.path.isdir(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen", "data"))

    runs = glob(
            os.path.join(AISANDBOX_PROJECTS_FOLDER,
                         example_config_multiple_estimator['project']['name'],
                         "mlkitchen", "run*"))

    assert os.path.isfile(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen", "cookbook.yaml"))
    generated_cookbook = load_yaml(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen", "cookbook.yaml"))

    assert 'previous' in generated_cookbook
    del generated_cookbook['previous']
    assert generated_cookbook == example_config_multiple_estimator['config']
    assert len(runs) == len(expected_regression_recipe_multiple_estimator)

    for run_number in runs:
        assert os.path.isfile(
            os.path.join(AISANDBOX_PROJECTS_FOLDER,
                         example_config_multiple_estimator['project']['name'],
                         "mlkitchen", run_number, "recipe.yaml"))
        assert os.path.isdir(
            os.path.join(AISANDBOX_PROJECTS_FOLDER,
                         example_config_multiple_estimator['project']['name'],
                         "mlkitchen", run_number, "profiles"))
        assert os.path.isdir(os.path.join(
                        AISANDBOX_PROJECTS_FOLDER,
                        example_config_multiple_estimator['project']['name'],
                        "mlkitchen", run_number, "steps"))

    for n, expected_config in \
            enumerate(expected_regression_recipe_multiple_estimator):
        generated_config = load_yaml(
            os.path.join(AISANDBOX_PROJECTS_FOLDER,
                         example_config_multiple_estimator['project']['name'],
                         "mlkitchen", f"run{n+1}", "recipe.yaml"))
        assert generated_config == expected_config
    rmtree(
        os.path.join(AISANDBOX_PROJECTS_FOLDER,
                     example_config_multiple_estimator['project']['name'],
                     "mlkitchen"))


@pytest.mark.parametrize("task", ["regression", "classification"])
def test_wrong_input(client, task, example_input_config):
    """
    testing wrong_input resulting in error
    """
    example_input_task_config = example_input_config[task]
    config_without_project = deepcopy(example_input_task_config)
    del config_without_project["project"]
    assert client.post('/recipe/all',
                       json=config_without_project).status_code == 422

    config_without_task = deepcopy(example_input_task_config)
    del config_without_task["config"]["task"]
    resp = client.post('/recipe/all',
                       json=config_without_task)
    assert resp.status_code == 422
    config_with_wrong_task = deepcopy(example_input_task_config)
    config_with_wrong_task["config"]["task"] = "arbitrary"
    assert client.post('/recipe/all',
                       json=config_with_wrong_task).status_code == 422

    config_without_target_col = deepcopy(example_input_task_config)
    del config_without_target_col["config"]["target_col"]
    assert client.post('/recipe/all',
                       json=config_without_target_col).status_code == 422


@pytest.mark.parametrize("task", ["regression", "classification"])
def test_acceptable_missing_steps(client, task, example_input_config):
    """
    testing if some of inputs can be missing without error
    """
    example_input_task_config = example_input_config[task]
    config_without_imputation = deepcopy(example_input_task_config)
    del config_without_imputation["config"]["imputation"]
    assert client.post('/recipe/all',
                       json=config_without_imputation).status_code == 200

    config_without_estimator = deepcopy(example_input_task_config)
    del config_without_estimator["config"]["estimator"]
    assert client.post('/recipe/all',
                       json=config_without_estimator).status_code == 200
    rmtree(os.path.join(AISANDBOX_PROJECTS_FOLDER,
                        example_input_task_config['project']['name'],
                        "mlkitchen"))


@pytest.mark.parametrize("task", ["regression", "classification"])
def test_recipe_getter(client, task, example_input_config):
    """
    testing if the recipe getter works as expected
    """
    project_name = example_input_config[task]['project']['name']
    example_input_task_config = example_input_config[task]
    resp = client.post('/recipe/all', json=example_input_task_config)
    assert resp.status_code == 200
    resp = client.get(f'/recipe/get_config/?project_name={project_name}')
    assert resp.status_code == 200
    generated_cookbook = resp.json()
    del generated_cookbook['previous']
    assert generated_cookbook == example_input_task_config['config']
    rmtree(os.path.join(AISANDBOX_PROJECTS_FOLDER,
                        example_input_task_config['project']['name'],
                        "mlkitchen"))
    # test for none existing projects
    resp = client.get(f'/recipe/get_config/?project_name={project_name}')
    assert resp.status_code == 404
