""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: execute.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The execute api and router of the data preparation api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from starlette.concurrency import run_in_threadpool
from data_preparation.services.network_service import NetworkService
from data_preparation.dependencies import get_network_service
from data_preparation.exceptions import ModuleNotExistsError, ResultNotFound


router = APIRouter(
    prefix="/execute",
    tags=["Execute"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.post("/{project}")
async def run_network(project: str,
                      network_service: NetworkService = Depends(get_network_service)):
    """
    Runs the entire network and saves the results.
    """
    try:
        await run_in_threadpool(network_service.run, project)
        _logger.info("Running %s ...", project)
    except SyntaxError as e:
        raise HTTPException(status_code=404, detail="Syntax Error in the expression!") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e

@router.post("/{project}/{module_id}")
async def run_module(project: str,
                     module_id: str,
                     network_service: NetworkService = Depends(get_network_service)):
    _logger.info("Running the module %s in project %s", module_id, project)
    try:
        await run_in_threadpool(network_service.run, project, module_id)
    except ModuleNotExistsError as e:
        raise HTTPException(status_code=404, detail="Module not found") from e
    except TypeError as e:
        raise HTTPException(status_code=400, detail="Module not connected!") from e
    except ResultNotFound as e:
        raise HTTPException(status_code=400, detail="The results of the previous modules are not valid, yet!") from e
    except SyntaxError as e:
        raise HTTPException(status_code=404, detail="Syntax Error in the expression!") from e
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except NameError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
