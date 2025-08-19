""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: dependencies.py
author: Lucas Rebscher
date: 12/2023
description: The exceptions
-----------------------------------------------------------------------------
Dependency Setup options:

    1. FastAPI's Depends() function (e.g. pass class that holds state or function that returns same instance)
        - using Depends for every dependency allows us to easily swap out dependencies during testing
    2. plain python module directly imported without using Depends() in endpoint
        - have to rely on monkeypatching to swap out dependencies
    3. IOC/DI package
        - extra package but helps to wire dependencies and provides clean patern

The approach taken in this module:
    
    - provide a get-function for every dependency
    - use lru_cache to construct singleton where desired
    - don't initialize dependency on module import

    See also example for dependency & get-function in FastAPI docs 
        (https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables) 
"""

from functools import lru_cache
from data_preparation.repositories.network_repository import \
    InMemoryNetworkRepository, \
    FileNetworkRepository, \
    NetworkRepository
from data_preparation.repositories.project_repository import \
    FileProjectRepository, \
    InMemoryProjectRepository, \
    ProjectRepository
from data_preparation.services.network_service import NetworkService
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER


@lru_cache
def get_network_repository() -> NetworkRepository:
    if True:
        return FileNetworkRepository(DATA_PREPARATION_PROJECTS_FOLDER)
    return InMemoryNetworkRepository()


@lru_cache
def get_network_service() -> NetworkService:
    return NetworkService(get_network_repository())


@lru_cache
def get_project_repository() -> ProjectRepository:
    if True:
        return FileProjectRepository()
    return InMemoryProjectRepository()
