""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: data.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The execute api and router of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import os
import logging
from fastapi import APIRouter, UploadFile
from fastapi.exceptions import HTTPException
from src.backend.project import Project
from src.backend.app_config import AISANDBOX_PROJECTS_FOLDER


router = APIRouter(
    prefix="/data",
    tags=["Data"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.post("/{project_id}/file")
async def receive_data_file(project_id: str, file: UploadFile):
    """
    Uploads parquet file for a project with project_id, 
    validating the file format and managing success or error responses accordingly.
    """
    if not file.filename.endswith('.parquet'):
        raise HTTPException(status_code=400,
                            detail='The input file must be in parquet format.')
    _logger.info("Saving the file ...")

    try:
        project = Project(name=project_id)
        project.receive_file(file)
        return {
            "message": f"The input file: {file.filename} was successfully uploaded to {project.name}"
        }
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Problem with uploading the file: {e}") from e