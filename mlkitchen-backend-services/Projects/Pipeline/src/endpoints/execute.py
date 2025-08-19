""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: execute.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The execute api and router of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import os
import uuid
import logging
import subprocess
import shutil
import random
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from kubernetes import client, config, utils
from yaml_replace import YAMLTemplate
from src.backend.methods_list import Steps
from src.backend.project import Project, CookBook
from src.backend.app_config import AISANDBOX_PROJECTS_FOLDER
from src.backend.utilities import get_largest_file_number_in_path



router = APIRouter(
    prefix="/execute",
    tags=["Execute"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)
_logger.info("Projects are going to be saved under %s", AISANDBOX_PROJECTS_FOLDER)

security = HTTPBasic()

@router.post("/all")
async def run_all(name: str, request: Request) -> str:
    """
    Runs the whole recipe. All dfined steps are going to run.
    """
    cookbook = CookBook(name)
    recipes = cookbook.get_list_of_recipes()
    # in case the data is saved after generating the recipes,
    # the splitting and saving profile should be running here!
    if cookbook.is_new_split_needed():
        cookbook._perform_data_split()
    cookbook.save_recipe_profiles()

    splits = cookbook.get_num_splits()
    current_call_archive_num = _current_call_number(name)
    for split_number in range(splits):
        split_number_as_str = str(split_number)
        for recipe in recipes:
            data_file = os.path.join(recipe, "data", "data.parquet")
            if os.path.exists(data_file):
                os.remove(data_file)
            shutil.copy(
                os.path.join(
                    AISANDBOX_PROJECTS_FOLDER, name, "mlkitchen", "data", "data.parquet"
                ),
                data_file,
            )
            run_name = cookbook.get_run_name(recipe, split_number_as_str)

            if os.environ.get("CLUSTER_TYPE", None) == "kubernetes":
                config.load_incluster_config()
                k8s_client = client.ApiClient()
                yaml_path = os.path.join(
                    ".", "src", "backend", "experiment_runner", "runner_job.yaml"
                )
                yaml_as_dict = YAMLTemplate.from_file(yaml_path).render(
                    {
                        "PROJECT_ID": name,
                        "JOB_NAME":name.replace("_", "-").lower() + "-" + str(random.randint(10000, 99999)),
                        "RECIPE": recipe,
                        "SPLIT_NUMBER": split_number_as_str,
                        "MLFLOW_RUN_NAME": run_name,
                        "ARCHIVE_PATH": name
                        + "/mlkitchen/call_history/"
                        + str(current_call_archive_num),
                        "DATA_PROVIDER_URL": os.environ["DATA_PROVIDER_URL"],
                        "RUNNER_IMAGE_TAG": os.environ["RUNNER_IMAGE_TAG"],
                        "RUNNER_IMAGE_NAME": os.environ["RUNNER_IMAGE_NAME"],
                    }
                )
                print(yaml_as_dict)
                response = utils.create_from_dict(k8s_client, data=yaml_as_dict)
                print(response)

    return (
        "Started running "
        + str(len(recipes))
        + " recipes for "
        + str(splits)
        + " splits."
    )


@router.post("/step")
async def run_step(project: Project, step: Steps):
    """
    It's going to run only the specific step.
    The previous steps runs should have been finished successfully.
    input: the step which can be selected from the drop down list.
    """
    _logger.info("Running the %s ...", step)
    project.run_step(step)


@router.get("/status")
async def get_status(project_name: str):
    """
    Get the job's status
    """
    _logger.info("Getting the job status ...")
    project = Project(name=project_name)
    try:
        return project.get_job_status()
    except OSError as e:
        raise HTTPException(404, f"The project {project_name} does not exist") from e


def _current_call_number(project_name: str):
    job_call_history_path = os.path.join(
        AISANDBOX_PROJECTS_FOLDER, project_name, "mlkitchen", "call_history"
    )
    try:
        if not os.path.exists(job_call_history_path):
            os.mkdir(job_call_history_path)
    except OSError as e:
        raise HTTPException(404, f"The project {project_name} does not exist") from e
    num_prev_calls = get_largest_file_number_in_path(job_call_history_path)
    os.mkdir(os.path.join(job_call_history_path, str(num_prev_calls + 1)))
    return num_prev_calls + 1
