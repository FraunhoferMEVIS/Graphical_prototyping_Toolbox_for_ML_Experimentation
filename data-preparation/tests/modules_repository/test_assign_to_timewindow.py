
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_assign_to_timewindow.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the timewindow assignment 
-----------------------------------------------------------------------------
"""

from data_preparation.core.modules_repository.assign_to_timewindow import AssignTimewindow
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


def test_run_successful(existing_project, result_repo, sample_input_table3):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    
    module = AssignTimewindow(
        inputs=[
            Socket(name="input1", value=sample_input_table3),
        ],
        config={
            "time_column": ModuleConfigParameter(
                id="time_column",
                type="string",
                value="event_time1",
                name="time_column",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=False
            ),
            "start_time": ModuleConfigParameter(
                id="start_time",
                type="string",
                value="2021-01-01 00:00",
                name="start_time",
                description="""The timewindow is based on the start time, which can be a column or a fixed value""",
                required=True,
                multipleValues=False
            ),
            "time_unit": ModuleConfigParameter(
                id="time_unit",
                type="string",
                value="hours",
                name="time_unit",
                description="""The unit of the period, e.g. minutes, days""",
                required=True,
                multipleValues=False
            ),
            "number_period": ModuleConfigParameter(
                id="number_period",
                type="integer",
                value="2",
                name="number_period",
                description="""The number of periods""",
                required=True,
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
    assert 'new_time_iterator_column' in output_data.columns
    assert list(output_data['new_time_iterator_column']) == [0, 1, 6, 6, 7, 7, 8, 8, 9]
    module.invalidate_output()

    module = AssignTimewindow(
        inputs=[
            Socket(name="input1", value=sample_input_table3),
        ],
        config={
            "time_column": ModuleConfigParameter(
                id="time_column",
                type="string",
                value="event_time2",
                name="time_column",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=False
            ),
            "start_time": ModuleConfigParameter(
                id="start_time",
                type="string",
                value="event_time1",
                name="start_time",
                description="""The timewindow is based on the start time, which can be a column or a fixed value""",
                required=True,
                multipleValues=False
            ),
            "time_unit": ModuleConfigParameter(
                id="time_unit",
                type="string",
                value="minutes",
                name="time_unit",
                description="""The unit of the period, e.g. minutes, days""",
                required=True,
            ),
            "number_period": ModuleConfigParameter(
                id="number_period",
                type="integer",
                value="30",
                name="number_period",
                description="""The number of periods""",
                required=True,
            ),
            "time_window": ModuleConfigParameter(
                id= "time_window",
                name= "time_window",
                description= """The time_window which indicates the window tshe event belongs to with respect to starting time and period""",
                type="string",
                required= False,
                value= "my_timewindow"
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
    assert 'my_timewindow' in output_data.columns
    assert list(output_data['my_timewindow']) == [19,18,1,1,1,1,1,1,1]

    module.invalidate_output()