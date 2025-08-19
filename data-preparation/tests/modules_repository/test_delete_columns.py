
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_delete_columns.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the module for removing columns
-----------------------------------------------------------------------------
"""
from data_preparation.core.modules_repository.delete_column import DeleteColumns
from data_preparation.models.network import Socket, \
                                    ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def test_run_successful(existing_project, result_repo, sample_input_table1):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """ 
    # Set up Filter_By_Column_Values module with mock inputs
    module = DeleteColumns(
        inputs=[
            Socket(name="input1", value=sample_input_table1),
        ],
        config={
            "column_name": ModuleConfigParameter(
                id="column_name",
                type="string",
                value=["subject_id"],
                name = "column's name",
                description= "The column's name to be removed or the list of columns' names",
                multipleValues = True,
                allowedValues = None,
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
    metadata = result_repo.get(project_name=existing_project,
                                module_id=module.id,
                                data_type=ResultTypes.DICT)
    assert len(df_result.columns) == 3
    assert 'subject_id' not in metadata["keys"]
    assert 'subject_id' not in df_result.columns
