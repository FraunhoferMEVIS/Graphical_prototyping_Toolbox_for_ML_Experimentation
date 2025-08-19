""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: script.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The network api and router of the data preparation api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter


router = APIRouter(
    prefix="/script",
    tags=["Script"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.get("/")
async def get_script(project: str):
    """
    Generates the script from network
    """
    _logger.info("Generating the script of project %s ...", project)
