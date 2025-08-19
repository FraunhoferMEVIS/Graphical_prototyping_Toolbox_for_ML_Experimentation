
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_filters.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the Filter modules
-----------------------------------------------------------------------------
"""
import pytest
from data_preparation.core.modules_repository.filters import (
        FilterByColumnValues, FilterByCondition
    )
from data_preparation.models.network import Socket, \
                                    ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def test_run_successful_numerical(existing_project, result_repo, sample_input_table1):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """ 
    # Set up Filter_By_Column_Values module with mock inputs
    module = FilterByColumnValues(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
        ],
        config={
            "column_name": ModuleConfigParameter(
                id="column_name",
                type="string",
                value="subject_id",
                name = "column's name",
                description= "The column's name to be filtered",
                multipleValues = False,
                allowedValues = None,
                required = True
            ),
            "values": ModuleConfigParameter(
                id="values",
                type="string",
                value=[4],
                name="value",
                description="The value should be equal to this value to be filtered",
                required=True,
                multipleValues=True
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
    assert len(df_result) == 1
    assert df_result['subject_id'].unique() == [4]


def test_run_successful_filter_string(existing_project, result_repo, sample_input_table1):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """ 
    # Set up Filter_By_Column_Values module with mock inputs
    module = FilterByColumnValues(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
        ],
        config={
            "column_name": ModuleConfigParameter(
                id="column_name",
                type="string",
                value="sex",
                name = "column's name",
                description= "The column's name to be filtered",
                multipleValues = False,
                allowedValues = None,
                required = True
            ),
            "values": ModuleConfigParameter(
                id="values",
                type="string",
                value=["F"],
                name="value",
                description="The value should be equal to this value to be filtered",
                required=True,
                multipleValues=True
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
    assert len(df_result) == 4
    assert df_result['sex'].unique() == ['F']

@pytest.mark.parametrize("expression_cols_validlength", [
            # Test for no input column
            ("1 < 2", [], 10),
            # test for one single column
            ("10 < x1 <15", ["test"], 2),
            # test filtering based on two columns
            ("floor((x1+x2)/2) > 100", ["systolic_blood_pressure", "diastolic_blood_pressure"], 6),
            # test agains three input columns
            ("(x1+x2)/2 > x3*10", ["systolic_blood_pressure", "diastolic_blood_pressure", "test"], 7),
            # test 4 input columns and "and" expression
            ("((x1+x2)/2 > x3*10) and x4=='B'", ["systolic_blood_pressure", "diastolic_blood_pressure", "test", "code"], 4)])
def test_run_advanced_filter(existing_project, result_repo,
                             sample_input_table2, expression_cols_validlength):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """ 
    # Set up Filter_By_Column_Values module with mock inputs
    module = FilterByCondition(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=expression_cols_validlength[1],
                name = "column's name",
                description = "The columns' name's to be used for filtering in the condition.",
                required = True,
                multipleValues = True,
            ),
            "conditional_expression": ModuleConfigParameter(
                id="conditional_expression",
                type="string",
                value=expression_cols_validlength[0],
                name="conditional_expression",
                description="""The output of this conditional expression
                    should be True to include the rows in the output column.
                    For example, it can be (a - b) > 5, where 'a' and 'b' correspond
                    to the first column in the 'columns' and 'b' corresponds to the 
                    second input in the 'columns' parameter.
                """,
                required=True,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    assert not module.valid_results
    # Call the run method
    module.run()

    assert module.valid_results

    df_input = result_repo.get(
        project_name=existing_project,
        module_id=sample_input_table2,
        data_type=ResultTypes.DATAFRAME
    )
    df_result = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DATAFRAME)
    assert len(df_result) == expression_cols_validlength[2]
    assert all(df_result.columns == df_input.columns)


@pytest.mark.parametrize("expression_cols_validlength", [
            # Test for input column with missing values
            ("x1 is nan", ["test"], 2),
            # test agains three input columns, one with missing values
            ("(x1+x2)/2 > x3*10", ["systolic_blood_pressure", "diastolic_blood_pressure", "test"], 5),
            # test 4 input columns and "and" expression and one with missing values
            ("((x1+x2)/2 > x3*10) and x4=='B'", ["systolic_blood_pressure", "diastolic_blood_pressure", "test", "code"], 3)])
def test_run_advanced_filter_with_missing_inputs(existing_project, result_repo,
                                                 sample_input_table2_with_missing_values,
                                                 expression_cols_validlength):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """ 
    # Set up Filter_By_Column_Values module with mock inputs
    module = FilterByCondition(
        inputs=[
            Socket(name="input1", value=sample_input_table2_with_missing_values),
        ],
        config={
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=expression_cols_validlength[1],
                name = "column's name",
                description = "The columns' name's to be used for filtering in the condition.",
                required = True,
                multipleValues = True,
            ),
            "conditional_expression": ModuleConfigParameter(
                id="conditional_expression",
                type="string",
                value=expression_cols_validlength[0],
                name="conditional_expression",
                description="""The output of this conditional expression
                    should be True to include the rows in the output column.
                    For example, it can be (a - b) > 5, where 'a' and 'b' correspond
                    to the first column in the 'columns' and 'b' corresponds to the 
                    second input in the 'columns' parameter.
                """,
                required=True,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    assert not module.valid_results
    # Call the run method
    module.run()

    assert module.valid_results

    df_input = result_repo.get(
        project_name=existing_project,
        module_id=sample_input_table2_with_missing_values,
        data_type=ResultTypes.DATAFRAME
    )
    df_result = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DATAFRAME)
    assert len(df_result) == expression_cols_validlength[2]
    assert all(df_result.columns == df_input.columns)
