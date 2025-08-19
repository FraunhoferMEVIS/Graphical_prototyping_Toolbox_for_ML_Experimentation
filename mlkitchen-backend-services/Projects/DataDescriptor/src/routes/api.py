""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: api.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: the api of the data descriptor with the related routers
-----------------------------------------------------------------------------
"""

from fastapi import APIRouter
from src.endpoints import features, modules, configuration


router = APIRouter()
router.include_router(configuration.router)
router.include_router(features.router)
router.include_router(modules.router)
