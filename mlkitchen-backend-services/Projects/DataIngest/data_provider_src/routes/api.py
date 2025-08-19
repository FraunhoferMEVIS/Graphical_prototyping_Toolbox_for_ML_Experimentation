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
from data_provider_src.endpoints import data

router = APIRouter()
router.include_router(data.router)
