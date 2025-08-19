""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: modules.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The Data Descriptors' endpoints for Modules to load data
-----------------------------------------------------------------------------
"""

# from typing import List
from fastapi import APIRouter


router = APIRouter(
    prefix="/scripts",
    tags=["Modules"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list_of_new_features_modules():
    """
    Get the list of features
    """
    return


@router.post("/new_module")
async def define_new_module(script, parameters):
    """
    Defining a new function to compute a new feature,
    based on existing ones
    """
    return
