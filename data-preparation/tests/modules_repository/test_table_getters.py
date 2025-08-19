
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_table_getters.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the Get_Postgres_Table module
-----------------------------------------------------------------------------
"""
import pytest
from data_preparation.core.modules_repository.getters import GetPostgresTable, LoadCSVFile
from data_preparation.core.results_repository import ResultTypes
from data_preparation.models.network import ModuleConfigParameter


def test_run_psql_successful(existing_project, result_repo):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    module = GetPostgresTable(
        config={
            "table_name": ModuleConfigParameter(
                id="table_name",
                type="string",
                value="patients",
                name="Table",
                description="The name of the table in the PostgreSQL database",
                required=True,
                multipleValues=False
            ),
            "schema": ModuleConfigParameter(
                id="schema",
                type="string",
                value="mimiciv_hosp",
                name="Schema",
                description="The schema of the PostgreSQL database",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    data = result_repo.get(project_name=existing_project,
                           module_id=module.id,
                           data_type=ResultTypes.DATAFRAME)
    assert len(data) > 0
    module.invalidate_output()


def test_run_psql_failure(existing_project, result_repo):
    """
    The test for the run method of the Get_Postgres_Table module, when the table_name is wrong.
    """
    module = GetPostgresTable(
        config={
            "table_name": ModuleConfigParameter(
                id="table_name",
                type="string",
                value="not_existing_table",
                name="Table",
                description="The name of the table in the PostgreSQL database",
                required=True,
                multipleValues=False
            ),
            "schema": ModuleConfigParameter(
                id="schema",
                type="string",
                value="mimiciv_hosp",
                name="Schema",
                description="The schema of the PostgreSQL database",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    with pytest.raises(Exception):
        module.run()

    assert not module.valid_results
    assert module.error_message != ""


def test_run_csv_importer(existing_project, result_repo, sample_csv_file): 
    module = LoadCSVFile(
        config={
            "table": ModuleConfigParameter(
                id="table",
                type="string",
                value=sample_csv_file,
                name="table",
                description="The path to the file containing data.",
                required=True,
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    data = result_repo.get(project_name=existing_project,
                           module_id=module.id,
                           data_type=ResultTypes.DATAFRAME)
    assert len(data) > 0
    metadata = result_repo.get(
        project_name=existing_project,
        module_id=module.id,
        data_type=ResultTypes.DICT
    )
    assert "keys" in metadata
    assert "features" in metadata
    assert len(metadata["features"]) > 0


    module.update_parameters(
        {
            "table": ModuleConfigParameter(
                id="table",
                type="string",
                value=sample_csv_file,
                name="table",
                description="The path to the file containing data.",
                required=True,
            ),
        }
    )