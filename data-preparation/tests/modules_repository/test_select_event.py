
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_select_events.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 07/2024
description: The pytest file for testing the Select Events modules
-----------------------------------------------------------------------------
"""
from data_preparation.core.modules_repository.select_event import SelectEvent
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes

def test_run_successful(existing_project, result_repo, sample_longitudinal_data):
    """
    The test for the run method of the SelectEvent module.
    """
    
    module = SelectEvent(
        inputs=[
            Socket(name="input1", value=sample_longitudinal_data),
        ],
        config={
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value="latest",
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=False
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=["date"],
                name="columns",
                description="The operator to be applied to the columns",
                required=True,
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
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    df_input = result_repo.get(
        project_name=existing_project,
        module_id=sample_longitudinal_data,
        data_type=ResultTypes.DATAFRAME
    )
    assert module.valid_results
    output_data = result_repo.get(project_name=existing_project,
                                  module_id=module.id,
                                  data_type=ResultTypes.DATAFRAME)
    assert len(output_data) == len(set(df_input['subject_id']))
    module.invalidate_output()