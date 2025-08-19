""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_sample_timeevents.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: script to test module sample_timeevents
-----------------------------------------------------------------------------
"""

import numpy as np
from data_preparation.core.modules_repository.sample_timeevents import SampleTimeEvents
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


config_fillNaNs={
             "time_window": ModuleConfigParameter(
                id="time_window",
                type="string",
                value=["assigned_timewindow"],
                name="grouping timewindow",
                description="""The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
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
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value=["average","sum"],
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=True
            ),
            "operator_fill_nan": ModuleConfigParameter(
                id="operator_fill_nan",
                type="string",
                value="fill_with_previous_value",
                name="operator_fill_nan",
                description="How to fill generated time windows, e.g. use previous value. If none is chosen, NaN remains.",
                required=False,
                multipleValues=False
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=["all_numerical"],
                name="columns",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=True
            ),
            "refrence_column_fill_nan": ModuleConfigParameter(
                id="refrence_column_fill_nan",
                type="string",
                value=["event_time1"],
                name="refrence_column_fill_nan",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator"""
            ),
        }

config_given_boundaries={
             "time_window": ModuleConfigParameter(
                id="time_window",
                type="string",
                value=["assigned_timewindow"],
                name="grouping timewindow",
                description="""The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
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
            "operator": ModuleConfigParameter(
                id="operator",
                type="string",
                value=["max"],
                name="operator",
                description="The operator to be applied to the columns",
                required=False,
                multipleValues=True
            ),
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=["value1"],
                name="columns",
                description="""The columns to be used for the operation, \
                first value in the list is the output column, the rest \
                are the inputs of the operator""",
                required=True,
                multipleValues=True
            ),
            "upper_bound_timewindow": ModuleConfigParameter(
            id= "upper_bound_timewindow",
            name="upper_bound_timewindow",
            description="The upper bound of the time window range. If not specified, the greatest window is used.",
            type= "integer",
            required= False,
            value= 12),

            "lower_bound_timewindow": ModuleConfigParameter(
            id= "lower_bound_timewindow",
            name="lower_bound_timewindow",
            description="The upper bound of the time window range. If not specified, the greatest window is used.",
            type= "integer",
            required= False,
            value= 5),
            
            "operator_fill_nan": ModuleConfigParameter(
                id="operator_fill_nan",
                type="string",
                value="None",
                name="operator_fill_nan",
                description="How to fill generated time windows, e.g. use previous value. If none is chosen, NaN remains.",
                required=False,
                multipleValues=False
            ),

        }


def test_run_successful(existing_project, result_repo, sample_input_table3):
    """
    The test for the run method of the Filter_By_Column_Values module.
    """
    ##Fill NaNs with previous value
    module = SampleTimeEvents(
        inputs=[
            Socket(name="input1", value=sample_input_table3),
        ],
        config=config_fillNaNs,
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    output_data = result_repo.get(project_name=existing_project,
                                   module_id=module.id,
                                   data_type=ResultTypes.DATAFRAME)
    assert 'value1_average' in output_data.columns
    assert np.allclose(output_data['value1_average'], [0.5,  0.5,  0.5,  0.5,  0.5,  0.5, 6.25,6.5,9.,10.,np.nan, 2.,2., 2.0 , 2.0,  2.0,  2.0 , 14.5 , 22.,55], equal_nan=True)
    module.invalidate_output()

    ##Do not fill NaNs, defined time-window boundaries
    module2 = SampleTimeEvents(
        inputs=[
            Socket(name="input1", value=sample_input_table3),
        ],
        config=config_given_boundaries,
        parent_project=existing_project,
        result_repo=result_repo
    )
    module2.run()
    assert module2.valid_results
    output_data = result_repo.get(project_name=existing_project,
                                   module_id=module2.id,
                                   data_type=ResultTypes.DATAFRAME)
       
    assert 'value1_max' in output_data.columns
    assert np.allclose(output_data['value1_max'], [np.nan,6.5,np.nan,10.,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan, 22.,np.nan,55,np.nan,np.nan,np.nan], equal_nan=True)   
    module2.invalidate_output()