
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_merge.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the merge-table modules
-----------------------------------------------------------------------------
"""
from data_preparation.core.modules_repository.merge import MergeTables
from data_preparation.models.network import Socket, \
                                    ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def test_run_successful_inner_join(existing_project, result_repo,
                                   sample_input_table1, sample_input_table2):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    # Set up Filter_By_Column_Values module with mock inputs
    module = MergeTables(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
            Socket(name="input2", value=sample_input_table2),
        ],
        config={
                "how": ModuleConfigParameter(
                id="how",
                name="how",
                description="""The join can be Inner or Outer.""",
                type="string",
                required=False,
                value="Inner",
                allowedValues={"Inner", "Outer"},
            ),
            "left_keys": ModuleConfigParameter(
                id="left_keys",
                type="string",
                value=["subject_id"],
                name = "left_keys",
                description= """The merge is done based on equality of this column/these columns \
                on the left input table, to a corresponding column in the right table.""",
                multipleValues = True,
                required = True
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    assert not module.valid_results
    # Call the run method
    module.run()

    assert module.valid_results

    df_result = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DATAFRAME)
    assert len(df_result) == 10
    # columns with unique name should remain as they are, 
    # columns that are not unique and are not used for joint,
    # should get table name as suffix.
    for column in ('subject_id', 'age', 'sex',
       'systolic_blood_pressure', 'diastolic_blood_pressure',
       f'test_{sample_input_table1}', f'test_{sample_input_table2}'):
        assert column in df_result


def test_run_successful_custom_postfix(existing_project, result_repo,
                                   sample_input_table1, sample_input_table2):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    left_postfix = "left"
    # Set up Filter_By_Column_Values module with mock inputs
    module = MergeTables(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
            Socket(name="input2", value=sample_input_table2),
        ],
        config={
                "how": ModuleConfigParameter(
                id="how",
                name="how",
                description="""The join can be Inner or Outer.""",
                type="string",
                required=False,
                value="Inner",
                allowedValues={"Inner", "Outer"},
            ),
            "left_keys": ModuleConfigParameter(
                id="left_keys",
                type="string",
                value=["subject_id"],
                name = "left_keys",
                description= """The merge is done based on equality of this column/these columns \
                on the left input table, to a corresponding column in the right table.""",
                multipleValues = True,
                required = True
            ),
            "left_postfix": ModuleConfigParameter(
                id="left_postfix",
                type="string",
                value=left_postfix,
                name="left_postfix",
                description="""...""",
                multipleValues=False,
                required=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    assert not module.valid_results
    # Call the run method
    module.run()

    assert module.valid_results

    df_result = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DATAFRAME)
    assert len(df_result) == 10
    # columns with unique name should remain as they are, 
    # columns that are not unique and are not used for joint,
    # should get table name as suffix.
    for column in ('subject_id', 'age', 'sex',
       'systolic_blood_pressure', 'diastolic_blood_pressure',
       f'test_{left_postfix}', f'test_{sample_input_table2}'):
        assert column in df_result


def test_run_successful_outer_join(existing_project, result_repo,
                                   sample_input_table1, sample_input_table2):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    # Set up Filter_By_Column_Values module with mock inputs
    module = MergeTables(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
            Socket(name="input2", value=sample_input_table2),
        ],
        config={
                "how": ModuleConfigParameter(
                id="how",
                name="how",
                description="""The join can be Inner or Outer.""",
                type="string",
                required=False,
                value="Outer",
                allowedValues={"Inner", "Outer"},
            ),
            "left_keys": ModuleConfigParameter(
                id="left_keys",
                type="string",
                value=["subject_id"],
                name = "left_keys",
                description= """The merge is done based on equality of this column/these columns \
                on the left input table, to a corresponding column in the right table.""",
                multipleValues = True,
                required = True
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    assert not module.valid_results
    # Call the run method
    module.run()

    assert module.valid_results

    df_result = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DATAFRAME)
    assert len(df_result) == 10
    # columns with unique name should remain as they are, 
    # columns that are not unique and are not used for joint,
    # should get table name as suffix.
    for column in ('subject_id', 'age', 'sex',
       'systolic_blood_pressure', 'diastolic_blood_pressure',
       f'test_{sample_input_table1}', f'test_{sample_input_table2}'):
        assert column in df_result