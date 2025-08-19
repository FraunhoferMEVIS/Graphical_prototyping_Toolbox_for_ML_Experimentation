
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_aggregate.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the aggregate and transform modules
-----------------------------------------------------------------------------
"""
import pytest
import pandas as pd
from data_preparation.core.modules_repository.aggregate import AggregateAndTransform, AggregateAndTransformMulti
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def sample_input_data():
    df = pd.DataFrame({
        'subject_id': [1,    2,   3,   4,   5,   6,   7,   1,    2,  3,   4,   8,   1,   2,   1],
        'age':        [17,   90, 20,  12,  18,  25,  30,  17,   90, 20,  12,  64,  17,  90,  17],
        'sex':        ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'F', 'M', 'F', 'F', 'M', 'F', 'M'],
        'value1':     [12,   2,   3,   5,   90, 23,  65,   23,  76,  2,   10,  8,   22,  15,  5],
        'value2':     [23,  14,  65,   3,   76, 12,  76,   35,  43,  8,   12, 20,   12,   9, 10]
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
            }
        ]
    }
    return df, metadata


def write_input_data_to_repo(*,
                     data,
                     metadata,
                     project_name,
                     result_repo,
                     input_socket_name):
    result_repo.add(project_name=project_name,
                    module_id=input_socket_name,
                    data_type=ResultTypes.DATAFRAME,
                    results=data,
                    append=False)
    result_repo.add(project_name=project_name,
                    module_id=input_socket_name,
                    data_type=ResultTypes.DICT,
                    results=metadata)


def get_aggregate_module(*,
                         input_socket_name,
                         operator,
                         columns,
                         project_name,
                         result_repo):
    module = AggregateAndTransform(
        inputs=[
            Socket(name="input1", value=input_socket_name),
        ],
        config={
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value=operator,
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=True
            ),
            "column": ModuleConfigParameter(
                id="column",
                type="string",
                value=columns,
                name="column",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=False
            ),
            "grouping_keys": ModuleConfigParameter(
                id="grouping_keys",
                type="string",
                value=["subject_id"],
                name="grouping keys",
                description="""The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
                required=True,
                multipleValues=True
            ),
            # output_column_name is optional
        },
        parent_project=project_name,
        result_repo=result_repo
    )
    return module


def get_multi_aggregate_module(*,
                         input_socket_name,
                         operator,
                         columns,
                         project_name,
                         result_repo):
    module = AggregateAndTransformMulti(
        inputs=[
            Socket(name="input1", value=input_socket_name),
        ],
        config={
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value=operator,
                name="operator",
                description="The operator to be applied to the columns",
                required=False
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=columns,
                name="columns",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=True
            ),
            "grouping_keys": ModuleConfigParameter(
                id="grouping_keys",
                type="string",
                value=["subject_id"],
                name="grouping keys",
                description="""The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
                required=True,
                multipleValues=True
            ),
            # output_column_name is optional
        },
        parent_project=project_name,
        result_repo=result_repo
    )
    return module


@pytest.mark.parametrize("operator", [["average"], ["sum"], ["median"], ["product"], ["min"], ["max"], ["min", "max", "average"]])
def test_run_successful(existing_project, result_repo, operator):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    value_column = 'value1'

    #Generate a sample input csv file
    input_socket_name = "mock_input_file"
    df, metadata = sample_input_data()
    write_input_data_to_repo(data=df,
                     metadata=metadata,
                     project_name=existing_project,
                     result_repo=result_repo,
                     input_socket_name=input_socket_name
                    )
    module = get_aggregate_module(input_socket_name=input_socket_name,
                                  project_name=existing_project,
                                  result_repo=result_repo,
                                  columns=value_column,
                                  operator=operator)

    module.run()

    assert module.valid_results

    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    if isinstance(operator, str):
        operator = [operator]
    for op in operator:
        assert f'{value_column}_{op}' in output_data.columns
    assert len(output_data) == len(set(df['subject_id']))
    module.invalidate_output()



@pytest.mark.parametrize("columns, operator", [(["value1"], "sum"), (["value1", "value2"], "average"), (["value1", "value2"], "max")])
def test_run_successful_multi_column(existing_project, result_repo, columns, operator):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    #Generate a sample input csv file
    input_socket_name = "mock_input_file"
    df, metadata = sample_input_data()
    write_input_data_to_repo(data=df,
                     metadata=metadata,
                     project_name=existing_project,
                     result_repo=result_repo,
                     input_socket_name=input_socket_name
                    )
    module = get_multi_aggregate_module(
                                input_socket_name=input_socket_name,
                                project_name=existing_project,
                                result_repo=result_repo,
                                columns=columns,
                                operator=operator)
    module.run()

    assert module.valid_results

    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    for column in columns:
        assert f'{column}_{operator}' in output_data.columns
    assert len(output_data) == len(set(df['subject_id']))
    module.invalidate_output()
