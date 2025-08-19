""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: methods.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The methods api and router of the ai-sandbox api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter, HTTPException, Query
from src.backend.methods_list import Steps, get_step_modules, \
                                            get_algorithm_metadata, \
                                            Filters, get_step_filters


router = APIRouter(
    prefix="/methods",
    tags=["Methods"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.get("/{step}")
async def get_implemented_methods(step: Steps,
                                  filters: list[Filters] = Query(None)):
    """
    Returns the list of implemented methods in a given step.
    :step: is the name of step in the pipeline
    :filters: is a list of flags to apply as a filter.
    """
    _logger.info("Requesting the list of implemented methods in %s step", step)
    return get_step_modules(step, filters)


@router.get("/step_filters/{step}")
async def get_filters_of_step(step: Steps):
    """
    Returns the list of possible filters for a given step.
    :step: is the name of step in the pipeline
    """
    return get_step_filters(step)


@router.get("/{step}/{alg}")
async def get_method_metadata(step: Steps, alg: str):
    """
    call to get the metadata (including the help and the input parameters)
    for the requested algorithm in the given step.
    :step: The name of the step
    :alg: name of the algorithm
    :raises HTTPException: if the step is not defined or alg is not
    implemented
    """
    _logger.info("Requesting the help for %s method.", alg)
    try:
        return get_algorithm_metadata(step, alg)
    except ValueError as e:
        raise HTTPException(status_code=422,
                            detail=f"The {step} and/or {alg} are not defined."
                            ) from e
