
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_nodes.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the base Node module
-----------------------------------------------------------------------------
"""
from data_preparation.models.network import Module, Socket
from data_preparation.core.modules_repository.base_node import Node
from data_preparation.core.modules_repository import generate_module_from_state


def test_socket_creation():
    socket = Socket(name="input_1", value="test.csv")
    assert socket.name == "input_1"
    assert socket.value == "test.csv"


def test_node_creation():
    socket = Socket(name="input_1", value="test.csv")
    node = Node(module_id="1", inputs=[socket])
    assert node.id == "1"


def test_node_default_values():
    node = Node()
    assert node.id != ""
    assert node.inputs
    assert len(node.inputs) > 0


def test_generate_module_from_state(result_repo, existing_project):
    state = {
        'id': '1',
        'blueprint': 'base_module',
        'label': 'sample_module',
        'position': {'x': 0, 'y': 0},
        'input_sockets': [
             {
                'name': 'input_1',
                'value': 'test.csv',
                'type': 'file',
                'required': False
            }
        ],
        'output_sockets': []
    }
    node = generate_module_from_state(Module(**state), existing_project, result_repo)
    assert isinstance(node, Node)
    assert node.id == '1'
    assert len(node.inputs) == 1
    assert node.inputs[0]

    node = Node()
    node_dict = node.as_dict()
    result = generate_module_from_state(Module(**node_dict), existing_project, result_repo)
    
    assert isinstance(result, Node)
    assert result.NAME == node.NAME
    assert result.id == node.id
    assert result.inputs == node.inputs
    assert result.valid_results == node.valid_results
