""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_edit_metadata.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2024
description: The pytest file for testing editing meta data
-----------------------------------------------------------------------------
"""

import pytest
import pandas as pd
from data_preparation.core.modules_repository.edit_metadata import (
    EditColumnName,
    EditDataType,
)
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def sample_input_data():
    df = pd.DataFrame(
        {
            "subject_id": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 8, 1, 2, 1],
            "subject": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 8, 1, 2, 1],
            "age": [
                17.0,
                90.1,
                20.2,
                12.3,
                18.4,
                25.5,
                30.6,
                17.7,
                90.8,
                20.9,
                12.0,
                64.1,
                17.2,
                90.3,
                17.4,
            ],
            "sex": [
                "M",
                "F",
                "M",
                "F",
                "M",
                "F",
                "M",
                "M",
                "F",
                "M",
                "F",
                "F",
                "M",
                "F",
                "M",
            ],
            "date": [
                "2023-10-04 12:00:00",
                "2023-10-04 12:01:00",
                "2023-10-04 12:02:00",
                "2023-10-04 12:03:00",
                "2023-10-04 12:04:00",
                "2023-10-04 12:05:00",
                "2023-10-04 12:06:00",
                "2023-10-04 12:07:00",
                "2023-10-04 12:08:00",
                "2023-10-04 12:09:00",
                "2023-10-04 12:10:00",
                "2023-10-04 12:11:00",
                "2023-10-04 12:12:00",
                "2023-10-04 12:13:00",
                "2023-10-04 12:14:00",
            ],
            "sex_boolean": [
                "M",
                1,
                "M",
                True,
                0,
                1,
                False,
                "M",
                1,
                "M",
                1,
                1,
                "M",
                True,
                "M",
            ],
            "value1": [12, 2, 3, 5, 90, 23, 65, 23, 76, 2, 10, 8, 22, 15, 5],
            "value2": [23, 14, 65, 3, 76, 12, 76, 35, 43, 8, 12, 20, 12, 9, 10],
        }
    )
    metadata = {
        "keys": ["subject_id"],
        "features": [
            {
                "name": "age",
                "type": "numerical",
            },
            {
                "name": "date",
                "type": "time",
            },
            {
                "name": "subject",
                "type": "numerical",
            },
            {"name": "sex", "type": "categorical"},
            {"name": "sex_boolean", "type": "string"},
            {"name": "value1", "type": "numerical"},
            {"name": "value2", "type": "numerical"},
        ],
    }
    return df, metadata


def sample_output_data1():
    df = pd.DataFrame(
        {
            "subject_id": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 8, 1, 2, 1],
            "subject": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 8, 1, 2, 1],
            "age": [17, 90, 20, 12, 18, 25, 30, 17, 90, 20, 12, 64, 17, 90, 17],
            "sex": [
                "M",
                "F",
                "M",
                "F",
                "M",
                "F",
                "M",
                "M",
                "F",
                "M",
                "F",
                "F",
                "M",
                "F",
                "M",
            ],
            "date": [
                "12:00:00",
                "12:01:00",
                "12:02:00",
                "12:03:00",
                "12:04:00",
                "12:05:00",
                "12:06:00",
                "12:07:00",
                "12:08:00",
                "12:09:00",
                "12:10:00",
                "12:11:00",
                "12:12:00",
                "12:13:00",
                "12:14:00",
            ],
            "sex_boolean": [
                False,
                True,
                False,
                True,
                False,
                True,
                False,
                False,
                True,
                False,
                True,
                True,
                False,
                True,
                False,
            ],
            "value1": [12, 2, 3, 5, 90, 23, 65, 23, 76, 2, 10, 8, 22, 15, 5],
            "value2": [23, 14, 65, 3, 76, 12, 76, 35, 43, 8, 12, 20, 12, 9, 10],
        }
    )
    dtype_dict = {
        "subject_id": "int64",
        "subject": "int64",
        "age": "int64",
        "sex": "object",
        "date": "object",
        "sex_boolean": "bool",
        "value1": "int64",
        "value2": "int64",
    }
    df = df.astype(dtype_dict)
    metadata = {
        "keys": ["subject"],
        "features": [
            {
                "name": "age",
                "type": "numerical",
            },
            {
                "name": "date",
                "type": "time",
            },
            {
                "name": "subject_id",
                "type": "numerical",
            },
            {"name": "sex", "type": "categorical"},
            {"name": "sex_boolean", "type": "categorical"},
            {"name": "value1", "type": "numerical"},
            {"name": "value2", "type": "numerical"},
        ],
    }
    return df, metadata


def sample_output_data2():
    df = pd.DataFrame(
        {
            "subject_id": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 8, 1, 2, 1],
            "subject": [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                1.0,
                2.0,
                3.0,
                4.0,
                8.0,
                1.0,
                2.0,
                1.0,
            ],
            "age": [
                17.0,
                90.1,
                20.2,
                12.3,
                18.4,
                25.5,
                30.6,
                17.7,
                90.8,
                20.9,
                12.0,
                64.1,
                17.2,
                90.3,
                17.4,
            ],
            "sex": [
                "M",
                "F",
                "M",
                "F",
                "M",
                "F",
                "M",
                "M",
                "F",
                "M",
                "F",
                "F",
                "M",
                "F",
                "M",
            ],
            "date": ["2023-10-04"] * 15,
            "sex_boolean": [
                False,
                True,
                False,
                True,
                False,
                True,
                False,
                False,
                True,
                False,
                True,
                True,
                False,
                True,
                False,
            ],
            "value1": [12, 2, 3, 5, 90, 23, 65, 23, 76, 2, 10, 8, 22, 15, 5],
            "value2": [23, 14, 65, 3, 76, 12, 76, 35, 43, 8, 12, 20, 12, 9, 10],
        }
    )
    dtype_dict = {
        "subject_id": "int64",
        "subject": "float64",
        "age": "float64",
        "sex": "object",
        "date": "object",
        "sex_boolean": "bool",
        "value1": "int64",
        "value2": "int64",
    }
    df = df.astype(dtype_dict)
    metadata = {
        "keys": ["subject_id"],
        "features": [
            {
                "name": "age",
                "type": "numerical",
            },
            {
                "name": "date",
                "type": "time",
            },
            {
                "name": "subject",
                "type": "numerical",
            },
            {"name": "sex", "type": "text"},
            {"name": "sex_boolean", "type": "categorical"},
            {"name": "value1", "type": "numerical"},
            {"name": "value2", "type": "numerical"},
        ],
    }
    return df, metadata


def write_input_data_to_repo(
    *, data, metadata, project_name, result_repo, input_socket_name
):
    result_repo.add(
        project_name=project_name,
        module_id=input_socket_name,
        data_type=ResultTypes.DATAFRAME,
        results=data,
        append=False,
    )
    result_repo.add(
        project_name=project_name,
        module_id=input_socket_name,
        data_type=ResultTypes.DICT,
        results=metadata,
    )


# Modules
def get_edit_data_types(
    *,
    input_socket_name,
    project_name,
    result_repo,
    columns_to_edit=None,
    new_data_types=None,
):
    module = EditDataType(
        inputs=[
            Socket(name="input1", value=input_socket_name),
        ],
        config={
            "column_names": ModuleConfigParameter(
                id="column_names",
                description="The column's name to be edit",
                name="column_names",
                type="string",
                required=True,
                value=columns_to_edit,
                multipleValues=True,
            ),
            "new_data_types": ModuleConfigParameter(
                id="new_data_types",
                description="The new data type name or the list of data types.",
                name="new_data_types",
                required=True,
                type="string",
                value=new_data_types,
                multipleValues=True,
            ),
        },
        parent_project=project_name,
        result_repo=result_repo,
    )
    return module


def get_edit_column_names(
    *,
    input_socket_name,
    project_name,
    result_repo,
    old_columns=None,
    new_columns=None,
    old_keys=None,
    new_keys=None,
):
    module = EditColumnName(
        inputs=[
            Socket(name="input1", value=input_socket_name),
        ],
        config={
            "column_names": ModuleConfigParameter(
                id="column_names",
                description="list of column names that will be edited",
                name="column_names",
                type="string",
                required=False,
                value=old_columns,
                multipleValues=True,
            ),
            "new_column_names": ModuleConfigParameter(
                id="new_column_names",
                description="list of column names that will be edited",
                name="new_column_names",
                required=False,
                type="string",
                value=new_columns,
                multipleValues=True,
            ),
            "keys": ModuleConfigParameter(
                id="keys",
                description="The key's name to be edit or the list of key names to be edit",
                name="keys",
                type="string",
                required=False,
                value=old_keys,
                multipleValues=True,
            ),
            "new_keys": ModuleConfigParameter(
                id="new_column_names",
                description="The new keys",
                name="new_keys",
                required=False,
                type="string",
                value=new_keys,
                multipleValues=True,
            ),
        },
        parent_project=project_name,
        result_repo=result_repo,
    )
    return module

#Tests
@pytest.mark.parametrize(
    "columns_datatype",
    [
        (
            ["subject", "subject_id", "sex_boolean", "date", "age"],
            ["key", "integer", "boolean", "time", "integer"],
            sample_output_data1(),
        ),
        (
            [
                "subject",
                "sex",
                "date",
                "sex_boolean",
            ],
            ["float", "string", "date", "boolean"],
            sample_output_data2(),
        ),
    ],
)
def test_run_successful_edit_dtypes(existing_project, result_repo, columns_datatype):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """

    # Generate a sample input csv file
    input_socket_name = "mock_input_file"
    df, metadata = sample_input_data()
    write_input_data_to_repo(
        data=df,
        metadata=metadata,
        project_name=existing_project,
        result_repo=result_repo,
        input_socket_name=input_socket_name,
    )
    module = get_edit_data_types(
        input_socket_name=input_socket_name,
        project_name=existing_project,
        result_repo=result_repo,
        columns_to_edit=columns_datatype[0],
        new_data_types=columns_datatype[1],
    )

    module.run()

    assert module.valid_results

    output_data = result_repo.get(
        project_name=existing_project,
        module_id=module.id,
        data_type=ResultTypes.DATAFRAME,
    )

    output_metadata = result_repo.get(
        project_name=existing_project, module_id=module.id, data_type=ResultTypes.DICT
    )
    
    expected_df=columns_datatype[2][0]
    expected_meta=columns_datatype[2][1]  

    # Compare df
    assert output_data.equals(expected_df), "DataFrames are not equal."
    # Compare metadata
    assert output_metadata["keys"] == expected_meta["keys"]
    assert sorted(output_metadata["features"], key=lambda x: x["name"]) == sorted(
        expected_meta["features"], key=lambda x: x["name"]
    )



    module.invalidate_output()


@pytest.mark.parametrize(
    "columns",
    [
        (["age", "sex"], ["new_age", "new_sex"], ["subject_id"], ["patient_id"]),
        (["age", "sex"], ["new_age", "new_sex"], None, None),
        (None, None, ["subject_id"], ["patient_id"]),
        (None, None, None, None),
        ("age", "new_age", None, None),
    ],
)
def test_run_successful_rename_columns(existing_project, result_repo, columns):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    input_socket_name = "mock_input_file"
    df, metadata = sample_input_data()
    write_input_data_to_repo(
        data=df,
        metadata=metadata,
        project_name=existing_project,
        result_repo=result_repo,
        input_socket_name=input_socket_name,
    )
    module = get_edit_column_names(
        input_socket_name=input_socket_name,
        project_name=existing_project,
        result_repo=result_repo,
        old_columns=columns[0],
        new_columns=columns[1],
        old_keys=columns[2],
        new_keys=columns[3],
    )

    module.run()

    assert module.valid_results

    output_data = result_repo.get(
        project_name=existing_project,
        module_id=module.id,
        data_type=ResultTypes.DATAFRAME,
    )

    new_column_names = columns[1]
    new_keys = columns[3]

    if new_column_names is not None and not isinstance(new_column_names, list):
        new_column_names = [new_column_names]
    if new_keys is not None and not isinstance(new_keys, list):
        new_keys = [new_keys]
    new_names = (new_column_names if new_column_names is not None else []) + (
        new_keys if new_keys is not None else []
    )

    for name in new_names:
        assert f"{name}" in output_data.columns
    module.invalidate_output()
