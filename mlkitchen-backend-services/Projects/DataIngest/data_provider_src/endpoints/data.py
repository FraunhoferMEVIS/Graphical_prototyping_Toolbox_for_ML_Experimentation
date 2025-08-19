""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: features.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The Data Descriptors' endpoints for Features
-----------------------------------------------------------------------------
"""

import pickle
import base64
from fastapi import APIRouter, HTTPException
from data_provider_src.backend import data
from methods_repository.config_models import RecipeConfig


router = APIRouter(
    # prefix="/data",
    tags=["Data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{project_id}/all")
async def get_entire_dataset(project_id: str):
    """
    Get the entire dataset of a given project.
    """
    D = data.load(project_id)
    return D.to_json(orient="records")


@router.get("/{project_id}/{split_number}/train")
async def get_training_data_of_run(project_id: str, split_number: int):
    """
    Get the "TRAINING" dataset of a given run of a project.
    """
    raise NotImplementedError()


@router.get("/{project_id}/{split_number}/validation")
async def get_validation_data_of_run(project_id: str, split_number: int):
    """
    Get the "VALIDATION" dataset of a given run of a projet.
    """
    raise NotImplementedError()


@router.get("/{project_id}/{split_number}/test")
async def get_test_data_of_run(project_id: str, split_number: int):
    """
    Get the "TEST" dataset of a given run of a project.
    """
    raise NotImplementedError()


@router.get("/{project_id}/{split_number}/indices")
async def get_indices_of_split(project_id: str, split_number: int):
    """
    Get the "TEST" dataset of a given run of a project.
    """
    try:
        indices = data.get_split_indices(project_id, split_number)
        # pickled = pickle.dumps(indices)
        # pickled_b64 = base64.b64encode(pickled)
        return {
            "indices": base64.b64encode(pickle.dumps(indices)).decode('utf-8'),
            # indices.to_json(orient="records"),
            "detail": "successful"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args) from e


@router.get("/{project_id}/split_exist")
async def split_exist(project_id: str):
    """
    Check if there is split data from previous runs exist
    """
    return {
        "exists": data.split_data_exists(project_id),
    }


@router.get("/{project_id}/num_folds")
async def get_num_splits(project_id: str):
    """
    Gets the number of folds in the project.
    """
    return {
        "num_folds": data.get_num_splits(project_id),
    }


@router.post("/{project_id}/split")
async def run_split(project_id: str,
                    split_config: RecipeConfig):
    """
    Split the dataset based on the RecipeConfig
    """
    num_splits, msg = data.split(project_id, split_config)
    if num_splits == 0:
        return {"message": msg}
    if num_splits == 1:
        return {"message": ' '.join(("Data was split to TRAINING, VALIDATION,",
                                     "and TEST subsets and saved to the",
                                     "project files."))}
    return {"message": ''.join((f"Data was split to {num_splits} folds",
                                "and saved to project files."))}
