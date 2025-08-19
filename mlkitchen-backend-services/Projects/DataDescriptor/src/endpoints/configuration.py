""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: configuration.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 08/2024
description: The Data Descriptors' endpoints for changing the configuration, e.g. meta-data info
-----------------------------------------------------------------------------
"""
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.models.features import MetadataModel
from src.backend.metadata_file import (get_project_metadata,
                                       save_project_metadata)


router = APIRouter(
    prefix="/config",
    tags=["Configuration"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{project_id}")
def get_current_metadata(project_id: str) -> dict:
    """
    Returns the current metadata info of the project.
    """
    try:
        return get_project_metadata(project_id)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"problem in loading the project's metadata: {e}"
                        ) from e


@router.post("/{project_id}")
def set_current_metadata(project_id: str, metadata: MetadataModel):
    """
    Change the current metadata of the project.
    """
    try:
        result = save_project_metadata(project_id,
                                       metadata)
        return {
            'detail': 'metadata was succesfully writtent to the project.',
            'metadata': result
        }
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Problem in saving the input metadata: {e}"
                        ) from e
