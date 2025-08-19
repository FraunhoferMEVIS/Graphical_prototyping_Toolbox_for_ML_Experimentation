""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: recipe.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The recipe api and router of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter, HTTPException
from src.backend.methods_list import Steps
from src.backend.app_config import DATA_DESCRIPTOR_URL
from src.backend.project import Project, CookBook
from src.backend.data_catalog import DataAccess
from src.models.recipe import StepConfig, TargetConfig
from methods_repository.config_models import RecipeConfig


router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.post("/all")
async def post_config(project: Project, config: RecipeConfig):
    _logger.info("Recieved the configuration: %s", config)
    try:
        _logger.info("Recieved the configuration: %s", config)
        return project.create(config)
    except Exception as e:
        raise HTTPException(status_code=400,
                      detail=str(e)) from e


@router.get("/{project_id}/target")
async def get_target_column(project_id: str) -> TargetConfig:
    data_descriptor = DataAccess(data_descriptor_url=DATA_DESCRIPTOR_URL,
                                 project_id=project_id)
    try:
        return data_descriptor.get_target_col()
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with getting the target column: {e}") from e


@router.put("/step/add")
async def set_step(project: Project, step: Steps, algs: StepConfig):
    try:
        _logger.info("Recieved the configuration for %s to use %s", step, algs)
        project.add_step(step, algs)
    except Exception as e:
        raise HTTPException(status_code=400,
                      detail="Failed to save the changes: {e}") from e


@router.delete("/step/delete")
async def delete_step(project: Project, step: Steps):
    _logger.info("Deleting a defined {step}")
    project.delete_step(step)


@router.get("/get_config")
async def get_config(project_name: str):
    _logger.info("Getting the configuration file from the backend ...")
    try:
        config = CookBook(project_name).get_config()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=e.args[0]) from e
    return config


@router.get("/get_missing_steps")
async def get_missing_mandatory_steps(project: Project):
    _logger.info(
        "Getting the list of mandatory steps that are not defined yet ...")
    return project.get_missing_mandatory_steps()
