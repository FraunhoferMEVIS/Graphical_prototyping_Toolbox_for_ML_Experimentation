""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_network_endpoint.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: testing the network endpoints of the api
-----------------------------------------------------------------------------
"""
import pytest
from data_preparation.core.node import Modules
# from data_preparation.core.project import Project


def test_change_module(client):
    """
    test editing a module in the network
    """


def test_change_invalid_module(client):
    """
    test editing a module that is not in the network
    """


def test_connect_two_modules(client,
                             existing_project: str,
                             new_module_request: dict,
                             connect_modules_request: dict):
    """
    test connecting two modules in the network
    """
    # given
    new_module_request["blueprint"] = "new-column"
    # and
    response = client.post(
        f"/network/{existing_project}/module",
        json=new_module_request,
    )

    # when
    response = client.post(
        f"/network/{existing_project}/connection",
        json=connect_modules_request,
    )

    # then
    assert response.status_code == 200
    
    response = client.get(f"/network/{existing_project}")
    assert response.status_code == 200
    assert len(response.json()["connections"]) == 1
    new_module = next(m for m in response.json()["modules"] if m["id"] == new_module_request["id"])
    assert new_module["input_sockets"][0]["value"] == connect_modules_request["sourceModule"]

def test_remove_connection(client,
                           existing_project_with_connection: str,
                           existing_connection):
    """
    test removing a connection between two modules
    """
    # when
    response = client.delete(
        f"/network/{existing_project_with_connection}/connection/{existing_connection}")

    # then
    assert response.status_code == 200
    response = client.get(f"/network/{existing_project_with_connection}")
    assert response.status_code == 200
    assert len(response.json()["connections"]) == 1


def test_remove_connection_fail(client, existing_project_with_connection: str):
    connection_id_not_exist = "not_existing_id"
    response = client.delete(
        f"/network/{existing_project_with_connection}/connection/{connection_id_not_exist}")

    # then
    assert response.status_code == 404


def test_getting_current_network_for_a_valid_project(client, existing_project: str):
    response = client.get(f"/network/{existing_project}")
    assert response.status_code == 200


def test_creating_network(client, empty_project: str):
    # given
    post_body = {"id": "123",
                 "connections": [],
                 "modules": []}

    # when
    response = client.post(f"/network/{empty_project}", json=post_body)

    # then
    assert response.status_code == 200
    assert response.json() == post_body


def test_getting_network_not_found(client, empty_project: str):
    # when
    response = client.get(f"/network/{empty_project}")

    # then
    assert response.status_code == 404


@pytest.mark.parametrize("module_name", [module_name.value for module_name in Modules])
def test_adding_a_module_to_an_existing_project(
    client, existing_project: str, module_name: str, new_module_request: dict
):
    # given
    new_module_request["blueprint"] = module_name

    # when
    response = client.post(
        f"/network/{existing_project}/module",
        json=new_module_request,
    )

    # then
    assert response.status_code == 200
    new_module = response.json()

    for key in ("id", "label", "blueprint", "position"):
        assert new_module[key] == new_module_request[key]
    assert len(new_module["output_sockets"]) == 1 or len(new_module["input_sockets"]) == 1


def test_updating_an_existing_module(client, existing_project: str):
    # given
    response = client.get(f"/network/{existing_project}")
    data = response.json()
    module = data["modules"][0]

    # when
    module["label"] = "Name Filter"
    put_response = client.put(
        f"/network/{existing_project}/module/{module['id']}",
        json=module,
    )

    # then
    assert put_response.status_code == 200
    assert put_response.json()["label"] == "Name Filter"


def test_deleting_an_existing_module(client, existing_project: str):
    # given
    response = client.get(f"/network/{existing_project}")
    data = response.json()
    module = data["modules"][0]

    # when
    put_response = client.delete(f"/network/{existing_project}/module/{module['id']}")

    # then
    assert put_response.status_code == 200
    updated_network = client.get(f"/network/{existing_project}").json()
    assert module["id"] not in [m["id"] for m in updated_network["modules"]]


def test_deleting_an_existing_module_with_connections(client,
                                                      existing_project_with_connection: str,
                                                     ):
    response = client.get(f"/network/{existing_project_with_connection}")
    data = response.json()
    module = data["modules"][0]

    put_response = client.delete(f"/network/{existing_project_with_connection}/module/{module['id']}")
    assert put_response.status_code == 200
    updated_network = client.get(f"/network/{existing_project_with_connection}").json()
    assert module["id"] not in [m["id"] for m in updated_network["modules"]]
    assert len(updated_network["connections"]) == 0


def test_get_config_of_module(client, existing_project: str, existing_module: str):
    # given
    expected = {
        'parameters': {
            'column_name': {
                'id': 'column_name',
                'name': "column's name",
                'type': 'string',
                'value': 'diagnosis_code',
                'description': "The column's name to be filtered",
                'multipleValues': False,
                'allowedValues': None,
                'required': True
                },
            'values': {
                'id': 'values',
                'name': 'value',
                'type': 'string',
                'value': ['I10', 'I11', 'I12'],
                'description': 'The value should be equal to this value to be filtered',
                'multipleValues': True,
                'allowedValues': None,
                'required': True
                }
        }
    }

    # when
    response = client.get(
        f"/network/{existing_project}/module/{existing_module}/config"
    )

    # then
    assert response.status_code == 200
    assert response.json() == expected


def test_update_config_of_module(client, existing_project: str, existing_module: str):
    """
    test updating the config of a module
    """
    # given
    config = client.get(
        f"/network/{existing_project}/module/{existing_module}/config"
    ).json()

    # when
    NEW_VALUE = "my-new-value"
    param = config["parameters"]["column_name"]
    param["value"] = NEW_VALUE

    config_update = client.put(
        f"/network/{existing_project}/module/{existing_module}/config",
        json=config,
    )

    # then
    assert config_update.status_code == 200
    result_config = config_update.json()
    assert "parameters" in result_config
    assert "column_name" in result_config["parameters"]
    assert "values" in result_config["parameters"]
    assert result_config["parameters"]["column_name"]["value"] == NEW_VALUE


def test_update_network(client, existing_project: str):
    # given
    new_network = {
        "id": "123",
        "connections": [],
        "modules": []
    }

    # when
    response = client.put(f"/network/{existing_project}", json=new_network)

    # then
    assert response.status_code == 200
    assert response.json() == new_network


def get_table_from_endpoint(client, project: str, module_id: str, page: int, size: int):
        return client.get(
            f"/network/{project}/module/{module_id}/table",
            params={'page': page,
                    'size': size}
        )


def test_get_module_output_successfully(client, existing_project: str, existing_module: str):
    """
    test getting a module's output table sucessfully
    """
    # given
    page_number = 0
    page_size = 5
    # if running the module, first
    response = client.post(
        f"/execute/{existing_project}/{existing_module}"
    )
    response = get_table_from_endpoint(client,
                                       project=existing_project,
                                       module_id=existing_module,
                                       page=page_number, size=page_size)
    # then
    assert response.status_code == 200
    table = response.json()
    assert 'columns' in table
    assert 'data' in table
    assert 0 <= len(table['data']) <= page_size

    page_number = 1
    response = get_table_from_endpoint(client,
                                       project=existing_project,
                                       module_id=existing_module,
                                       page=page_number, size=page_size)
    assert response.status_code == 200
    table = response.json()
    assert 'columns' in table
    assert 'data' in table
    assert len(table['data']) == 0


def test_get_module_output_fail(client, existing_project: str, existing_module: str):
    """
    test getting a module's output table sucessfully
    """
    # given
    page_number = 0
    page_size = 5

    response = get_table_from_endpoint(client,
                                       project=existing_project,
                                       module_id=existing_module,
                                       page=page_number, size=page_size)
    # then it should throw bad request error
    assert response.status_code == 400


def get_visualization_from_endpoint(client, project: str, module_id: str):
        return client.get(
            f"/network/{project}/module/{module_id}/visualize"
        )


def test_get_visualization_output_successfully(client, existing_project_with_connection: str,
                                               existing_visualization_module: str):
    """
    test getting a module's output visualization sucessfully
    """
    # if running the module, first
    response = client.post(
        f"/execute/{existing_project_with_connection}/{existing_visualization_module}"
    )
    response = get_visualization_from_endpoint(client,
                                       project=existing_project_with_connection,
                                       module_id=existing_visualization_module
                                    )
    # then
    assert response.status_code == 200
    plot = response.json()
    assert 'image' in plot


def test_get_module_visualize_fail(client,
                                   existing_project_with_connection: str,
                                   existing_visualization_module: str,
                                   existing_module: str
                                ):
    """
    test getting a module's output visualization sucessfully
    """
    # no valid results, yet
    response = get_visualization_from_endpoint(client,
                                       project=existing_project_with_connection,
                                       module_id=existing_visualization_module,
                                    )
    # then it should throw bad request error
    assert response.status_code == 400

    # Given running the entire network
    response = client.post(
        f"/execute/{existing_project_with_connection}/"
    )
    # if get output for non visualization module
    response = get_visualization_from_endpoint(client,
                                       project=existing_project_with_connection,
                                       module_id=existing_module,
                                    )
    # then
    assert response.status_code == 400