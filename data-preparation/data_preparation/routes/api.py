""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: api.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: the api of the data preparation with the related routers
-----------------------------------------------------------------------------
"""

from fastapi import APIRouter
from data_preparation.endpoints import modules, network, project, session, script, execute


router = APIRouter()
router.include_router(project.router)
router.include_router(modules.router)
router.include_router(network.router)
router.include_router(session.router)
router.include_router(script.router)
router.include_router(execute.router)