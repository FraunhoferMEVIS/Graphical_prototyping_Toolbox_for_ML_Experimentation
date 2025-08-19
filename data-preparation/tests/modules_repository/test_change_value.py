
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_change_value.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 06/2024
description: The pytest file for testing the module for changing values in place
-----------------------------------------------------------------------------
"""
import random
import pytest
from data_preparation.core.modules_repository.change_value import ConvertUnit
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


@pytest.mark.parametrize("expression", ["(x+pi)/1000", "sqrt(pow((x) // 2, 3)) + randint(2, 5)", "10"])
def test_run_successful(existing_project, expression, result_repo, sample_input_table2):
    """
    The test for the run method of the ConvertUnit module.
    """

    test_column = 'test'
    ref_column = 'test_unit'
    ref_column_val = 'y'
    
    module = ConvertUnit(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "expression": ModuleConfigParameter(
                id="expression",
                type="string",
                value=expression,
                name="expression",
                description="The expression to be applied to the columns",
                required=True,
            ),
            "column": ModuleConfigParameter(
                id="column",
                type="string",
                value=test_column,
                name="column",
                description="""The column to be used for the operation, \
                The result will be written on the same column.""",
                required=True,
                multipleValues=False
            ),
            "reference_column": ModuleConfigParameter(
                id="reference_column",
                name="reference_column",
                description="The reference column for checking the condition.",
                type="string",
                required=False,
                value=ref_column
            ),
            "condition": ModuleConfigParameter(
                id="condition",
                name="condition",
                description="""The condition for applying the operator. \
                    You can set the condition, in case, you want to apply \
                    the changes to the values of a column, based on the \
                    value of another column.
                """,
                type="string",
                required=False,
                value="==",
                allowedValues={"==", "<", ">", "<=", ">=", "!=",
                               "startswith", "endswith", "containes"}
            ),
            "reference_value": ModuleConfigParameter(
                id="reference_value",
                name="reference_value",
                description="""The reference value that the reference column \
                           is checked agains, based on the input condition.""",
                type="string",
                required=False,
                value=ref_column_val
                )
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    random.seed(1)
    module.run()
    
    assert module.valid_results

    input_data = result_repo.get(
        project_name=existing_project,
        module_id=sample_input_table2,
        data_type=ResultTypes.DATAFRAME
    )
    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    assert all(input_data.columns == output_data.columns)
    assert all(input_data[input_data[ref_column] != ref_column_val] == output_data[output_data[ref_column] != ref_column_val])
    module.invalidate_output()
