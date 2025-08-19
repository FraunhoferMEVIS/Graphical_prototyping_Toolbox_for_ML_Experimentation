""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: results.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The results api and router of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter
from src.backend.project import Project


router = APIRouter(
    prefix="/results",
    tags=["Results"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.get("/")
async def results_as_json(project: Project):
    """
    Gets the results as a json structure
    """
    _logger.info("Preparing the results ...")
    return project.get_results()


@router.get("/report")
async def results_as_pdf(project: Project):
    """
    Gets the report as a pdf file
    """
    _logger.info("Preparing the report ...")
    return project.get_report()
