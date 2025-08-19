
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_flag.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 07/2024
description: The pytest file for testing the Flag modules
-----------------------------------------------------------------------------
"""
import pytest
from data_preparation.core.modules_repository.flag import (Flag)
from data_preparation.models.network import Socket, \
                                    ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


@pytest.mark.parametrize("expression_cols", [
            # Test for no input column
            ("1 < 2", []),
            # test for one single column
            ("10 < x1 <15", ["test"]),
            # test for flag based on two columns
            ("floor((x1+x2)/2) > 100", ["systolic_blood_pressure", "diastolic_blood_pressure"]),
            # test agains three input columns
            ("(x1+x2)/2 > x3*10", ["systolic_blood_pressure", "diastolic_blood_pressure", "test"]),
            # test 4 input columns and "and" expression
            ("((x1+x2)/2 > x3*10) and x4=='B'", ["systolic_blood_pressure", "diastolic_blood_pressure", "test", "code"])])

def test_run_flag(existing_project, result_repo,
                             sample_input_table2, expression_cols):
    """
    The test for the run method of the Flag module.
    """ 
    # Set up Flag module with mock inputs
    module = Flag(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=expression_cols[1],
                name = "column's name",
                description = "The columns' name's used to apply the condition on.",
                required = True,
                multipleValues = True,
            ),
            "conditional_expression": ModuleConfigParameter(
                id="conditional_expression",
                type="string",
                value=expression_cols[0],
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
            "flag_column_name": ModuleConfigParameter(
            id="flag_column_name",
            type="string",
            value="myflag",
            name="flags column's name",
            description="""The flagged column's name""",
            required=False,
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
    assert len(df_result) == len(df_input)

