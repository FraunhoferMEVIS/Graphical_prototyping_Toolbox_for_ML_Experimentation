
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_new_column_modules.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the new_column modules
-----------------------------------------------------------------------------
"""
from data_preparation.core.modules_repository.new_column import NewColumn
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def test_run_successful(existing_project, result_repo, sample_input_table2):
    """
    The test for the run method of new columns module.
    """
    
    module = NewColumn(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value="+",
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=False
            ),
            "new_column": ModuleConfigParameter(
                id="new_column",
                type="string",
                value="result",
                name="new_column",
                description="""...""",
                required=True,
                multipleValues=False
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=["systolic_blood_pressure", "diastolic_blood_pressure"],
                name="columns",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=True
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )

    module.run()
    assert module.valid_results

    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    assert 'result' in output_data.columns
    assert list(output_data['result']) == [177, 226, 202, 205, 198, 223, 190, 200, 243, 230]
    module.invalidate_output()

    module = NewColumn(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value="-",
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=False,
            ),
            "new_column": ModuleConfigParameter(
                id="new_column",
                type="string",
                value="result",
                name="new_column",
                description="""...""",
                required=True,
                multipleValues=False
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=["systolic_blood_pressure", "diastolic_blood_pressure"],
                name="columns",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=True
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results

    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    assert 'result' in output_data.columns
    assert list(output_data['result']) == [27, 44, 22, 35, 32, 47, 46, 44, 49, 66]

    metadata = result_repo.get(
        project_name=existing_project,
        module_id=module.id,
        data_type=ResultTypes.DICT
    )
    assert "keys" in metadata
    assert "features" in metadata

    for feature in metadata["features"]:
        if feature["name"] == "result":
            break
    else:
        assert False
    module.invalidate_output()
