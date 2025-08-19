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
import sys
import pytest
import pandas as pd
from starlette.testclient import TestClient

# add parent directory to sys path to import 'main' and 'data_preparation'.
# https://docs.python-guide.org/writing/structure/#test-suite
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_preparation.dependencies import \
                        get_network_repository, \
                        get_network_service, \
                        get_project_repository
from data_preparation.core.network import Network
from data_preparation.models.network import \
                        Module, \
                        ModuleConfig, \
                        ModuleConfigParameter, \
                        ParameterValueType, \
                        Connection
from data_preparation.repositories.network_repository import \
                        FileNetworkRepository
from data_preparation.repositories.project_repository import \
                        FileProjectRepository
from data_preparation.services.network_service import NetworkService
from data_preparation.core.project import Project
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER
from data_preparation.core.results_repository import \
                    FileResultsRepository, ResultTypes
from main import app


_EXAMPLE_PROJECT_NAME = "example_project"
_network_repository = FileNetworkRepository(DATA_PREPARATION_PROJECTS_FOLDER)
_project_repository = FileProjectRepository()
_network_service = NetworkService(_network_repository)
_EXISTING_MODULE_ID = "f6b3f237-dc49-4c06-91f5-6f7cf33aa0c7"
_EXISTING_VISUALIZATION_MODULE_ID = "0000-1111"
_NEW_MODULE_ID = "test_123"
_EXISTING_CONNECTION_ID = "be0a2e4e-5b57-4884-9a4a-0aadb54f00f8"

app.dependency_overrides[get_network_service] = lambda: _network_service
app.dependency_overrides[get_project_repository] = lambda: _project_repository
app.dependency_overrides[get_network_repository] = lambda: _network_repository


@pytest.fixture(scope="module")
def client():
    """
    client for testing the app
    """
    yield TestClient(app)


@pytest.fixture
def project():
    return Project.create_project(_EXAMPLE_PROJECT_NAME, replace=True)


@pytest.fixture
def empty_project() -> str:
    """A project without a network."""

    project_name = "empty-project"
    _project_repository.add(project_name)

    yield project_name

    _network_repository.deleteAll()
    _project_repository.deleteAll()


def add_sample_table_to_project(project_name):
    df = pd.DataFrame({
        'subject_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'age': [17, 90, 20, 12, 18, 25, 30, 40, 14, 60],
        'sex': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
        'diagnosis_code': ['I10', 'I15', 'I10', 'I11', 'I19', 'I12', 'I18', 'I09', 'I15', 'I19']})
    metadata = {
        'keys': ['subject_id'],
        'features':[
            {
                "name": "age",
                "type": "numerical"
            },
            {
                "name": "sex",
                "type": "categorical"
            },
            {
                "name": "diagnosis_code",
                "type": "categorical"
            }
        ]
    }
    result_repo = FileResultsRepository()
    result_repo.add(project_name=project_name,
                    module_id="test",
                    data_type=ResultTypes.DATAFRAME,
                    results=df,
                    append=False)
    # metadata:
    result_repo.add(project_name=project_name,
                    module_id="test",
                    data_type=ResultTypes.DICT,
                    results=metadata)
    return result_repo


@pytest.fixture
def existing_project() -> str:
    # setup before test
    _project_repository.add(_EXAMPLE_PROJECT_NAME)
    _network = Network.load_network(
        _EXAMPLE_PROJECT_NAME,
        {
            "modules":[
                Module(
                    id=_EXISTING_MODULE_ID,
                    label="Diagnoses Filter",
                    position={"x": 100.0, "y": 0.0},
                    config=ModuleConfig(
                        parameters={
                            "column_name": ModuleConfigParameter(
                                id="column_name",
                                type=ParameterValueType.STRING,
                                value="diagnosis_code",
                                name = "column's name",
                                description= "The column's name to be filtered",
                                multipleValues = False,
                                allowedValues = None,
                                required = True
                            ),
                            "values": ModuleConfigParameter(
                                id="values",
                                type=ParameterValueType.STRING,
                                value=["I10", "I11", "I12"],
                                name="value",
                                description="The value should be equal to this value to be filtered",
                                required=True,
                                multipleValues=True
                            ),
                        }
                    ),
                    blueprint="filter-by-value",
                    input_sockets=[
                        {
                            "name": "input1",
                            "value": "test",
                            "required": True,
                        }
                    ],
                    output_sockets=[],
                ),
            ],
            "connections": []
        }
    )
    _network_repository.add(
        _EXAMPLE_PROJECT_NAME,
         _network,
    )

    result_repo = add_sample_table_to_project(_EXAMPLE_PROJECT_NAME)
    yield _EXAMPLE_PROJECT_NAME

    result_repo.delete(project_name=_EXAMPLE_PROJECT_NAME, module_id="test")
    _network_repository.delete(_EXAMPLE_PROJECT_NAME)
    _project_repository.delete(_EXAMPLE_PROJECT_NAME, force=True)


@pytest.fixture
def existing_module() -> str:
    yield _EXISTING_MODULE_ID


@pytest.fixture
def existing_visualization_module() -> str:
    yield _EXISTING_VISUALIZATION_MODULE_ID


@pytest.fixture
def existing_module2() -> str:
    return _NEW_MODULE_ID


@pytest.fixture
def new_module_request():
    config = {
        "id": _NEW_MODULE_ID,
        "label": "my-label",
        "position": {"x": 100.0, "y": 0.0},
        "blueprint": "new-column",
        "input_sockets": [],
        "output_sockets": [],
    }
    return config


@pytest.fixture
def connect_modules_request():
    config = {
        "sourceModule": _EXISTING_MODULE_ID,
        "targetModule": _NEW_MODULE_ID,
        "sourceSocket": "output1",
        "targetSocket": "input1",
    }
    return config


@pytest.fixture
def existing_project_with_connection() -> str:
    # setup before test
    _project_repository.add(_EXAMPLE_PROJECT_NAME)
    _network = Network.load_network(
        _EXAMPLE_PROJECT_NAME,
        {
            'id': 'network1',
            'modules': [
                    Module(
                        id=_EXISTING_MODULE_ID,
                        label='Diagnoses Filter',
                        config=ModuleConfig(
                            parameters={
                                'column_name': ModuleConfigParameter(
                                    id='column_name',
                                    name="column's name",
                                    type=ParameterValueType.STRING,
                                    value='diagnosis_code',
                                    description="The column's name to be filtered",
                                    multipleValues=False,
                                    allowedValues=None,
                                    required=True
                                ),
                                'values': ModuleConfigParameter(
                                    id='values',
                                    name='value',
                                    type=ParameterValueType.STRING,
                                    value=['I10', 'I11', 'I12'],
                                    description='The value should be equal to this value to be filtered',
                                    multipleValues=True,
                                    allowedValues=None,
                                    required=True
                                )
                            }
                        ),
                        position={'x': 100.0, 'y': 0.0},
                        blueprint='filter-by-value',
                        input_sockets=[{
                            'name': 'input1',
                            'value': 'test'
                        }],
                        output_sockets=[{
                            'name': 'output_1',
                            'value': None
                        }]
                    ),
                    Module(
                        id=_NEW_MODULE_ID,
                        label='my-label',
                        config=ModuleConfig(
                            parameters={
                                'operator': {
                                    'id': 'operator',
                                    'name': 'operator',
                                    'type': 'string',
                                    'value': '+',
                                    'description': 'The operator to be applied to the columns',
                                    'multipleValues': False,
                                    'allowedValues': ['**', '>', 'times', 'rshift', 'gt', 'cosh', \
                                                      'not equal', 'invert', 'ge', 'div', 'ne', 'mul', \
                                                      'negative', 'round', 'lt', '=', 'floordiv', \
                                                      'equal', 'xor', 'sin', 'acosh', 'truediv', 'plus', \
                                                      'sub', '==', 'lshift', 'absolute', 'and', 'atanh', \
                                                      'abs', 'isinf', 'le', 'or', '^', 'log2', '>>', '/', \
                                                      'asin', '>=', 'pow', 'neq', 'tanh', 'atan', 'positive', \
                                                      'ceil', 'acos', 'asinh', '<=', '-', 'floor', 'minus', \
                                                      '&', '<<', 'log10', 'exp', 'sqrt', 'isnan', 'sinh', \
                                                      'not', '<', '+', '!=', 'neg', 'pos', 'tan', 'cos', \
                                                      'eq', '%', '|', '*', 'mod', '//', 'equals', 'add', 'x'
                                    ],
                                    'required': False
                                },
                                'columns': {
                                    'id': 'columns',
                                    'name': 'columns',
                                    'type': 'string',
                                    'value': None,
                                    'description': '''The columns to be used for the operation, \
                                                      first value in the list is the output column, the rest \
                                                      are the inputs of the operator''',
                                    'multipleValues': True,
                                    'allowedValues': None,
                                    'required': True
                                }
                            }
                        ),
                        position={'x': 100.0, 'y': 0.0},
                        blueprint='new-column',
                        input_sockets=[{
                            'name': 'input1',
                            'value': _EXISTING_MODULE_ID
                        }],
                        output_sockets=[{
                            'name': 'output_1',
                            'value': None
                        }]
                ),
                Module(
                    id=_EXISTING_VISUALIZATION_MODULE_ID,
                    label="Pair Plot",
                    position={"x": 100.0, "y": 20.0},
                    config=ModuleConfig(
                        parameters={
                            # all default
                        }
                    ),
                    blueprint="pair-plot",
                    input_sockets=[
                        {
                            "name": "input1",
                            "value": "test",
                            "required": True,
                        }
                    ],
                    output_sockets=[],
                )
            ],
            'connections': [
                Connection(
                    id=_EXISTING_CONNECTION_ID,
                    sourceModule=_EXISTING_MODULE_ID,
                    sourceSocket='output1',
                    targetModule=_NEW_MODULE_ID,
                    targetSocket='input1'
                ),
                Connection(
                    id='connection-000-222',
                    sourceModule=_EXISTING_MODULE_ID,
                    sourceSocket='output1',
                    targetModule=_EXISTING_VISUALIZATION_MODULE_ID,
                    targetSocket='input1'
                )
            ]
        }
    )
    _network_repository.add(
        _EXAMPLE_PROJECT_NAME,
         _network,
    )

    result_repo = add_sample_table_to_project(_EXAMPLE_PROJECT_NAME)
    yield _EXAMPLE_PROJECT_NAME

    # cleanup after test
    result_repo.delete(project_name=_EXAMPLE_PROJECT_NAME, module_id="test")
    _network_repository.delete(_EXAMPLE_PROJECT_NAME)
    _project_repository.delete(_EXAMPLE_PROJECT_NAME, force=True)


@pytest.fixture
def existing_project_core_network(existing_project_with_connection) -> Network:
    network = _network_repository.get(existing_project_with_connection)
    yield network


@pytest.fixture
def existing_connection():
    return _EXISTING_CONNECTION_ID