""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: features.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The Data Descriptors' endpoints for Features
-----------------------------------------------------------------------------
"""

from fastapi import APIRouter, HTTPException
from src.backend.features import (get_list_of_features, get_feature_type,
                                  get_target)
                                #  add_new_feature_to_project, \
                                #  remove_feature, undo_remove_feature


router = APIRouter(
    prefix="/features",
    tags=["Features"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{project_id}/list")
async def list_of_project_features(project_id: str):
    """
    Get the list of features of a specific project
    """
    try:
        return get_list_of_features(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"The project, {project_id} doesn't exist, or metadata is not defined for it."
        ) from e


@router.get("/{project_id}/get_feature_type")
async def get_type(project_id: str, feature: str):
    """
    Getting type of the requested feature
    """
    try:
        return get_feature_type(project_id, feature)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"The project, {project_id} doesn't exist, or the {feature} is not in defined in the metadata."
        ) from e


@router.get("/{project_id}/get_target_column")
async def get_target_column(project_id: str):
    """
    Getting type of the requested feature
    """
    try:
        target_col = get_target(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"The project, {project_id} doesn't exist, or metadata is not defined for it."
        ) from e
    return target_col


# @router.post("/{project_id}/add")
# async def add_new_feature(project_id: str,
#                           new_feature: List[NewFeatureConfig]):
#     """
#     Add a new feature
#     """
#     return add_new_feature_to_project(project_id, new_feature)


# @router.post("/{project_id}/undo_remove")
# async def undo_feature_removal(project_id: str, feature: str):
#     """
#     Undo removing a specific feature
#     """
#     return undo_remove_feature(project_id, feature)


# @router.delete("/{project_id}/remove")
# async def delete_feature(project_id: str, feature: str):
#     """
#     Remove a feature
#     """
#     return remove_feature(project_id, feature)
