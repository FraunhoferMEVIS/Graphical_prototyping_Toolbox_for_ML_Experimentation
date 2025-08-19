""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_execute_endpoint.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: testing the execute endpoints of the api
-----------------------------------------------------------------------------
"""
from data_preparation.core.results_repository import \
                    FileResultsRepository, ResultTypes


def  test_run_network_successfully(client, existing_project: str):
    """
    test run the network
    """
    response = client.post(
        f"/execute/{existing_project}"
    )
    # then
    assert response.status_code == 200


def test_run_module_successfully(client, existing_project: str, existing_module: str):
    """
    test run a module in the network
    """
    response = client.post(
        f"/execute/{existing_project}/{existing_module}"
    )
    # then
    assert response.status_code == 200
    result_repo = FileResultsRepository()
    result = result_repo.get(existing_project, existing_module, ResultTypes.DATAFRAME)
    assert result is not None
    assert len(result) == 4


def test_run_module_not_found(client, existing_project: str):
    """
    test run a module in the network
    """
    response = client.post(
        f"/execute/{existing_project}/not_found_module"
    )
    # then
    assert response.status_code == 404


def test_run_network_fail_not_valid_input(client, existing_project: str, existing_module: str):
    """
    test run a module in the network
    """
    result_repo = FileResultsRepository()
    result_repo.delete(existing_project, 'test') # delete the input

    response = client.post(
        f"/execute/{existing_project}/{existing_module}"
    )
    # then
    assert response.status_code == 400
