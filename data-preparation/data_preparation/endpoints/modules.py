""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: modules.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The module api and router of the data preparation api
-----------------------------------------------------------------------------
"""

from fastapi import APIRouter
from data_preparation.dummy import create_module_blueprints
from data_preparation.models.modules import ModuleBlueprint


router = APIRouter(
    prefix="/modules",
    tags=["Modules"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def list_modules() -> list[ModuleBlueprint]:
    """
    Get the list of modules in a given category, based on input filters
    """
    return create_module_blueprints()
