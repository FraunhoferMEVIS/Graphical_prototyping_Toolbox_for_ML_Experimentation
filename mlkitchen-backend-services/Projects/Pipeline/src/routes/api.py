""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: api.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: the api of the ai-sandbox with the related routers
-----------------------------------------------------------------------------
"""

from fastapi import APIRouter
from src.endpoints import execute, recipe, results, methods, data


router = APIRouter()
router.include_router(recipe.router)
router.include_router(data.router)
router.include_router(methods.router)
router.include_router(execute.router)
router.include_router(results.router)
