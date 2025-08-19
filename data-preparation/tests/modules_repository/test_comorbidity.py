
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_comorbidity.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 06/2024
description: The pytest file for testing the module for getting comorbidity
-----------------------------------------------------------------------------
"""
from data_preparation.core.modules_repository.comorbidity import Comorbidity
from data_preparation.models.network import Socket, ModuleConfigParameter
from data_preparation.core.results_repository import ResultTypes


DISEASE = 'METSTATIC_CANCER'
ICD_COLUMN = 'diagnoses'
CODES = ["196", "197", "198", "199", 
         "C77", "C78", "C79", "C80"]


def test_run_successful(existing_project, result_repo, sample_longitudinal_data):
    """
    The test for the run method of the ConvertUnit module.
    """
    patients_with_metastatic_cancer = [1, 3, 6, 7]
    module = Comorbidity(
        inputs=[
            Socket(name="input1", value=sample_longitudinal_data),
        ],
        config={
            "column": ModuleConfigParameter(
                id="column",
                type="string",
                value=ICD_COLUMN,
                name="column",
                description="The column of ICD code.",
                required=True,
                multipleValues=False
            ),
            "disease_name": ModuleConfigParameter(
                id="disease_name",
                name="disease_name",
                description="""The name of disease, a new column with this name will be created \
                with True/False values for presence of the value in the list of ICD
                codes for a specific patient.""",
                type="string",
                required=True,
                value=DISEASE
            ),
            "icd_codes": ModuleConfigParameter(
                id="icd_codes",
                name="icd_codes",
                description="The list of ICD codes of the specific diseas.",
                type="string",
                required=True,
                value=CODES,
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
    assert len(output_data.columns) == 2
    assert DISEASE in output_data.columns
    # all patients with metastatic cancer should have comorbidity set to True
    assert all(output_data[output_data['subject_id'].isin(patients_with_metastatic_cancer)][DISEASE])
    # all other patients should have comorbidity set to False
    assert all(~output_data[~output_data['subject_id'].isin(patients_with_metastatic_cancer)][DISEASE])

    module.invalidate_output()



def test_run_time_dependent(existing_project, result_repo, sample_longitudinal_data):
    """
    The test for the run method of the ConvertUnit module.
    """
    patients_with_metastatic_cancer = [1, 3, 6, 7]
    module = Comorbidity(
        inputs=[
            Socket(name="input1", value=sample_longitudinal_data),
        ],
        config={
            "column": ModuleConfigParameter(
                id="column",
                type="string",
                value=ICD_COLUMN,
                name="column",
                description="The column of ICD code.",
                required=True,
                multipleValues=False
            ),
            "disease_name": ModuleConfigParameter(
                id="disease_name",
                name="disease_name",
                description="""The name of disease, a new column with this name will be created \
                with True/False values for presence of the value in the list of ICD
                codes for a specific patient.""",
                type="string",
                required=True,
                value=DISEASE
            ),
            "icd_codes": ModuleConfigParameter(
                id="icd_codes",
                name="icd_codes",
                description="The list of ICD codes of the specific diseas.",
                type="string",
                required=True,
                value=CODES,
                multipleValues=True
            ),
            "time_dependent": ModuleConfigParameter(
                id="time_dependent",
                name="time_dependent",
                description="""A flag to extract the comorbidity per input subject/key combination or \
                based on history at each point. For example, if the value is True, and the patient caught
                COVID in 2020, the comorbidity column will have a False value until 2020 and True \
                from 2020 on. If False, the comorbidity column is going to have a value of True for \
                all time points.
                Note: Default value is False. If set to True, then the parameter for time_column is mandatory.
                """,
                type="boolean",
                required=False,
                value=True,
                multipleValues=False
            ),
            "time_column": ModuleConfigParameter(
                id="time_column",
                name="time_column",
                description="""It's used, if the value of time_dependent parameter is True. \
                it's used to sort the data ascending.
                """,
                type="string",
                required=False,
                value="date",
                multipleValues=False
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
    assert len(output_data.columns) == 3
    assert DISEASE in output_data.columns
    # patients 1 and 3 had a metastatic cancer in their history, so the value changes to True after the first diagnosis
    print(output_data.iloc[[2,7]][DISEASE])
    assert all(output_data.iloc[[2,7]][DISEASE])
    # all other patients should have comorbidity set to False
    assert all(~output_data[~output_data['subject_id'].isin(patients_with_metastatic_cancer)][DISEASE])

    module.invalidate_output()
