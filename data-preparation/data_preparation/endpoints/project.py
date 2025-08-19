""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: project.py
author: Lucas Rebscher, Elham Taghizadeh
date: 12/2023
description: project endpoints
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from starlette.concurrency import run_in_threadpool
from data_preparation.dependencies import get_network_repository, get_project_repository
from data_preparation.dummy import create_network
from data_preparation.exceptions import ProjectNotFound
from data_preparation.models.project import (
    ProjectGetResponse,
    ProjectPostBody,
    ProjectPostResponse)
from data_preparation.repositories.network_repository import NetworkRepository
from data_preparation.repositories.project_repository import (
    ProjectRepository)


router = APIRouter(
    prefix="/project",
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.post("/dummy-data")
async def add_dummy_data(
    project_repository: ProjectRepository = Depends(get_project_repository),
    network_repository: NetworkRepository = Depends(get_network_repository),
):
    # 'test' is used in frontend as fallback project for testing
    project_repository.add("test")
    network_repository.add("test", create_network())

    return {"message": "Created dummy data."}


@router.post("")
async def create_project(
    project_body: ProjectPostBody,
    replace: bool = False,
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectPostResponse:
    """
    Generate a Project with the given input name
    :param: project is the name of the project that should be created.
    """
    name = project_body.name
    try:
        await run_in_threadpool(project_repository.add, project_body.name)
        _logger.info("Submitting the %s's network", name)
        return ProjectPostResponse(
            message=f"Project {name} with an empty network was created.", status=True
        )

    except FileExistsError as e:
        message = f"""A project with the name {name}, already exist.
                      If you want to replace it with an empty project,
                      call me again with 'replace' set to True"""
        _logger.error(message)
        raise HTTPException(status_code=400, detail=message) from e


@router.get("/{project_name}")
async def get_project(
    project_name: str,
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectGetResponse:
    """
    Gets a project information with the given name.
    """
    try:
        project = await run_in_threadpool(project_repository.get, project_name)
    except ProjectNotFound as e:
        raise HTTPException(status_code=404, detail="Project not found") from e 

    return ProjectGetResponse(name=project)
