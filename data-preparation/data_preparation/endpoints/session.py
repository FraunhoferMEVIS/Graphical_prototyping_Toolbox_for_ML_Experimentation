""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: session.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The session api and router of the data preparation api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter


router = APIRouter(
    prefix="/session",
    tags=["Sessions"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.get("/")
async def get_current_session(project: str):
    """
    Gets the current session
    """
    return {}


@router.post("/add_session")
async def add_session(project: str):
    """
    Creates a new session based on the latest one.
    """
    return {}


@router.post("/remove_session")
async def remove_session(project: str):
    """
    Removes the latest Session and recover the previous results
    """
    return {}