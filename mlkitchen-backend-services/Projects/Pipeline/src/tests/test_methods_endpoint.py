""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_methods_endpoint.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: testing the methods endpoints of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import pytest
from src.backend.methods_list import Steps


@pytest.mark.parametrize("step", [step.value for step in Steps])
def test_get_step_methods(client, step):
    """
    test get_step_methods: To test if getting methods of a given step \
    is working as expected
    """
    resp = client.get(f'methods/{step}')
    # check if running
    assert resp.status_code == 200

    # check if the output makes sesne!
    result = resp.json()
    # resp is a dict, containing a key named as "algorithms"
    # resp should contain "algorithms"
    assert "algorithms" in result
    # the resp['algorithms'] is a list. Each member of the list is
    # a dictionary containing the keys: 'langugae' and 'algorithms',
    # which indicate the implemented algorithms belong to
    # which programming language.
    # at least one language's algorithms should be implemented
    assert len(result["algorithms"]) >= 1
    implemented_algs = []
    for lang_algs in result["algorithms"]:
        # all members of the list should contain the keys 'language'
        # and 'algorithms'
        assert 'algorithms' in lang_algs and 'language' in lang_algs
        implemented_algs.extend(lang_algs['algorithms'])
    # At least one algorithm should exist in each defined step
    assert len(implemented_algs) >= 1


@pytest.mark.parametrize("step", [step.value for step in Steps])
def test_get_step_methods_help(client, step):
    """
    test get_step_methods_help: To test if getting the help for a given method
    of a given step is working as expected.
    """
    methods_request = client.get(f'methods/{step}')
    result = methods_request.json()
    implemented_algs = []
    for lang_algs in result["algorithms"]:
        # all members of the list should contain the keys 'language'
        # and 'algorithms'
        implemented_algs.extend(lang_algs['algorithms'])

    for alg in implemented_algs:
        # Test for all implemented algorithms of each step
        help_request = client.get(f'methods/{step}/{alg}')
        # if it is running properly
        if help_request.status_code != 200:
            print(f"Error for {step} and {alg}")
        assert help_request.status_code == 200
        # if the response contains all the necesary keys
        response_as_json = help_request.json()
        assert 'programming_language' in response_as_json and \
               'step' in response_as_json and \
               'name' in response_as_json and \
               response_as_json['name'] == alg and \
               'help' in response_as_json and \
               'parameters' in response_as_json

        for param in response_as_json['parameters']:
            assert 'name' in param and 'type' in param and param['name'] and param['type']

def test_error_on_invalid_step_name(client):
    """
    test invalid step as input
    """
    step = 'ExampleInvalidStepName'
    resp = client.get(f'methods/{step}')
    # check if running
    assert resp.status_code == 422


@pytest.mark.parametrize("step", [step.value for step in Steps])
def test_error_on_step_invalid_method(client, step):
    """
    test catching error on invalid method name
    """
    alg = "ExampleInvalidAlgorithmName"
    help_request = client.get(f'methods/{step}/{alg}')
    assert help_request.status_code == 422
