""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_network.py
author: Elham Taghizadeh, Lucas Rebscher, Melissa Finster, Johannes Bunk
date: 04/2024
description: testing the Network class that are not tested by the endpoint tests
-----------------------------------------------------------------------------
"""


def test_neighbors_forward(existing_project_core_network, existing_module, existing_module2):
    neighbors = existing_project_core_network.neighbors(existing_module, forward=True, backward=False)
    assert neighbors[0].id == existing_module2


def test_neighbors_backward(existing_project_core_network, existing_module, existing_module2):
    neighbors = existing_project_core_network.neighbors(existing_module2, forward=False, backward=True)
    assert neighbors[0].id == existing_module
