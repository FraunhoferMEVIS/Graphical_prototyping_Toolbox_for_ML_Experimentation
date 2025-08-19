""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: conftest.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for configuring the inputs for the tests
-----------------------------------------------------------------------------
"""

import os
import shutil
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_preparation.core.results_repository import FileResultsRepository, ResultTypes
from data_preparation.repositories.project_repository import \
        FileProjectRepository
from data_preparation.repositories.network_repository import FileNetworkRepository
from data_preparation.core.network import Network
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER, DATA_PREPARATION_CSV_REPO

_EXAMPLE_PROJECT_NAME = "example_project"
_network_repository = FileNetworkRepository(DATA_PREPARATION_PROJECTS_FOLDER)
_project_repository = FileProjectRepository()
_result_repository = FileResultsRepository()


@pytest.fixture(scope="session")
def result_repo():
    return _result_repository


@pytest.fixture
def existing_project() -> str:
    # setup before test
    _project_repository.add(_EXAMPLE_PROJECT_NAME)
    _network_repository.add(
        _EXAMPLE_PROJECT_NAME,
        Network.load_network(
            _EXAMPLE_PROJECT_NAME,
            {
                "modules": [],
                "connections": [],
            }
        ),
    )

    yield _EXAMPLE_PROJECT_NAME

    # cleanup after test
    _network_repository.delete(_EXAMPLE_PROJECT_NAME)
    _project_repository.delete(_EXAMPLE_PROJECT_NAME, force=True)


def sample1():
    df = pd.DataFrame({
        'subject_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'age': [17, 90, 20, 12, 18, 25, 30, 40, 14, 85],
        'sex': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'M'],
        'test': [0, 1, 0, 0, 0, 0, 0, 1, 1, 0]})
    
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
                "name": "test",
                "type": "categorical"
            }
        ]
    }
    return df, metadata


def sample2():
    df = pd.DataFrame({
        'subject_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'code': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
        'systolic_blood_pressure': [102, 135, 112, 120, 115, 135, 118, 122, 146, 148],
        'diastolic_blood_pressure': [75, 91, 90, 85, 83, 88, 72, 78, 97, 82],
        'test': [9.5, 11.9, 8.9, 5.1, 12.0, 5.5, 2.4, 5.7, 9.0, 4.2],
        'test_unit': ['x', 'y', 'x', 'y', 'x', 'x', 'x', 'x', 'x', 'y'],
    })
    
    metadata = {
        'keys': ['subject_id'],
        'features':[
            {
                "name": "code",
                "type": "categorical"
            },
            {
                "name": "systolic_blood_pressure",
                "type": "numerical"
            },
            {
                "name": "diastolic_blood_pressure",
                "type": "numerical"
            },
            {
                "name": "test",
                "type": "numerical"
            },
            {
                "name": "test_unit",
                "type": "categorical"
            }
        ]
    }
    return df, metadata

def sample2_with_missing_values():
    df = pd.DataFrame({
        'subject_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'code': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
        'systolic_blood_pressure': [102, 135, 112, 120, 115, 135, 118, 122, 146, 148],
        'diastolic_blood_pressure': [75, 91, 90, 85, 83, 88, 72, 78, 97, 82],
        'test': [9.5, 11.9, 8.9, 5.1, 12.0, None, 2.4, 5.7, None, 4.2],
        'test_unit': ['x', 'y', 'x', 'y', 'x', None, 'x', 'x', None, 'y'],

    })
    
    metadata = {
        'keys': ['subject_id'],
        'features':[
            {
                "name": "code",
                "type": "categorical"
            },
            {
                "name": "systolic_blood_pressure",
                "type": "numerical"
            },
            {
                "name": "diastolic_blood_pressure",
                "type": "numerical"
            },
            {
                "name": "test",
                "type": "numerical"
            },
            {
                "name": "test_unit",
                "type": "categorical"
            }
        ]
    }
    return df, metadata


def longitudinal_data():
    df = pd.DataFrame({
        'subject_id': [1,    2,   3,   4,   5,   6,   7,   1,    2,  3,   4,   8,   1,   2,   1],
        'age':        [17,   90, 20,  12,  18,  25,  30,  17,   90, 20,  12,  64,  17,  90,  17],
        'sex':        ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'F', 'M', 'F', 'F', 'M', 'F', 'M'],
        'value1':     [12,   2,   3,   5,   90, 23,  65,   23,  76,  2,   10,  8,   22,  15,  5],
        'value2':     [23,  14,  65,   3,   76, 12,  76,   35,  43,  8,   12, 20,   12,   9, 10],
        'diagnoses':  ['196', 'V08', '200', 'O987', 'M800', '199', 'C77', 'K767', 'F32', 'C80',
                       'K721', 'H35', 'V02', 'K055', 'E012'],
        'date':       ['2020-02-03', '2020-02-04', '2020-02-04', '2020-02-05', '2020-02-05',
                       '2020-02-06', '2020-02-07', '2020-02-08', '2020-01-04', '2020-01-24',
                       '2020-03-04', '2020-03-05', '2020-02-01', '2020-02-03', '2020-02-02']
    })
    metadata = {
        "keys": ["subject_id"],
        "features": [
            {
                "name": "age",
                "type": "numerical",
            },
            {
                "name": "sex",
                "type": "categorical"
            },
            {
                "name": "value1",
                "type": "numerical"
            },
            {
                "name": "value2",
                "type": "numerical"
            },
            {
                "name": "diagnoses",
                "type": "categorical"
            }
        ]
    }
    return df, metadata


def sample3():
    df = pd.DataFrame({
        'subject_id': [1, 2, 1, 1, 2, 2, 1, 1,2],
        'event_time1': pd.to_datetime([
            '2021-01-01 01:00', '2021-01-01 02:00', '2021-01-01 12:00',
            '2021-01-01 13:00', '2021-01-01 14:00', '2021-01-01 15:00',
            '2021-01-01 16:00', '2021-01-01 17:00', '2021-01-01 18:00'
        ]),
        'event_time2': pd.to_datetime([
            '2021-01-01 10:30', '2021-01-01 11:00', '2021-01-01 12:30',
            '2021-01-01 13:30', '2021-01-01 14:30', '2021-01-01 15:30',
            '2021-01-01 16:30', '2021-01-01 17:30', '2021-01-01 18:30'
        ]),
        'assigned_timewindow': [0, 1, 6, 6, 7, 7, 8, 8, 9],
        'value1':[0.5, 2, 6, 6.5, 7, 22, 8, 10, 55],
        'value2':[3, 1, 5, 10, 8, 2, 8, 10, 12],
    })
    
    metadata = {
        'keys': ['subject_id'],
        'features': [
            {
                "name": "event_time1",
                "type": "time"
            },
            {
                "name": "event_time2",
                "type": "time"
            },
            {
                "name": "assigned_timewindow",
                "type": "numerical"
            },
            {
                "name": "value1",
                "type": "numerical"
            },
            {
                "name": "value2",
                "type": "numerical"
            }
        ]
    }
    return df, metadata


def write_table(table, metadata, project_name, table_name):
    _result_repository.add(project_name=project_name,
                    module_id=table_name,
                    data_type=ResultTypes.DATAFRAME,
                    results=table,
                    append=False)
    
    _result_repository.add(project_name=project_name,
                    module_id=table_name,
                    data_type=ResultTypes.DICT,
                    results=metadata)


@pytest.fixture
def sample_input_table1(existing_project):
    table_name = "mock_input_file1"
    df, metadata = sample1()
    write_table(df, metadata, existing_project, table_name)

    yield table_name


@pytest.fixture
def sample_input_table2(existing_project):
    table_name = "mock_input_file2"
    df, metadata = sample2()
    write_table(df, metadata, existing_project, table_name)

    yield table_name


@pytest.fixture
def sample_input_table2_with_missing_values(existing_project):
    table_name = "mock_input_file2"
    df, metadata = sample2_with_missing_values()
    write_table(df, metadata, existing_project, table_name)

    yield table_name


def generate_csv_data_repo():
    if not os.path.exists(DATA_PREPARATION_CSV_REPO):
        os.makedirs(DATA_PREPARATION_CSV_REPO)


@pytest.fixture
def sample_csv_file():
    generate_csv_data_repo()
    dataset_name = "example"
    table_name = "sample_data.csv"
    dataset_folder = os.path.join(DATA_PREPARATION_CSV_REPO, dataset_name)
    if not os.path.exists(dataset_folder):
        os.mkdir(dataset_folder)
    filepath = os.path.join(dataset_folder, table_name)
    df, _ = sample1()
    df.to_csv(filepath, index=False)
    yield f"{dataset_name}:{table_name}"
    os.remove(filepath)
    
    if len(os.listdir(dataset_folder)) == 0:
        shutil.rmtree(dataset_folder)
        if len(os.listdir(DATA_PREPARATION_CSV_REPO)) == 0:
            shutil.rmtree(DATA_PREPARATION_CSV_REPO)


@pytest.fixture
def sample_longitudinal_data(existing_project):
    table_name = "mock_longitudinal_input"
    df, metadata = longitudinal_data()
    write_table(df, metadata, existing_project, table_name)

    yield table_name


@pytest.fixture
def sample_input_table3(existing_project):
    table_name = "mock_input_file3"
    df, metadata = sample3()
    write_table(df, metadata, existing_project, table_name)

    yield table_name
