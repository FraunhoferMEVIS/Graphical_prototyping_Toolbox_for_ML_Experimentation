""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: network.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk, Lucas Rebscher
date: 10/2023
description: The network api and router of the data preparation api
-----------------------------------------------------------------------------
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from starlette.concurrency import run_in_threadpool
from data_preparation.dependencies import get_network_repository, get_network_service
from data_preparation.exceptions import (ModuleExistsError,
                ModuleNotExistsError, NetworkNotFoundError,
                ResultNotFound, ConnectionNotExistsError,
                NotVisualizationModule, ModuleWithoutOutputTable)
from data_preparation.models.network import (
        Connection, Module, ModuleConfig, Network as NetworkModel,
        TablePage, RenderedVisualization)
from data_preparation.repositories.network_repository import \
                                            NetworkRepository
from data_preparation.services.network_service import NetworkService


router = APIRouter(
    prefix="/network",
    tags=["Network"],
    responses={404: {"description": "Not found"}},
)
_logger = logging.getLogger(__name__)


@router.get("/{project}")
async def get_current_network(
    project: str,
    network_repository: NetworkRepository = Depends(get_network_repository),
) -> NetworkModel:
    """
    Get the current network json file
    """
    try:
        if not (network:= await run_in_threadpool(network_repository.get, project)):
            raise HTTPException(
                status_code=404,
                detail="Project does not exist. Please create the project, first.",
            )
        _logger.info("Returning the %s's network", project)
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="The project doesn't have any network, create a network first.",
        ) from e
    return network.as_dict()


@router.post("/{project}")
async def create_network(
    project: str,
    network_model: NetworkModel,
    network_repository: NetworkRepository = Depends(get_network_repository),
) -> NetworkModel:
    """
    Create a network
    """
    network = await run_in_threadpool(NetworkService.load_network_from_api,
                                      project, network_model)
    if not (network := await run_in_threadpool(network_repository.add,
                                               project, network)):
        raise HTTPException(
            status_code=404,
            detail="Project does not exist. Please create the project, first.",
        )
    _logger.info("Returning the %s's network", project)
    return NetworkService.save_network_to_api(network)


@router.put("/{project}")
async def update_network(
    project: str,
    network_model: NetworkModel,
    network_repository: NetworkRepository = Depends(get_network_repository),
) -> NetworkModel:
    try:
        network = await run_in_threadpool(
            NetworkService.load_network_from_api, project, network_model)
        if not (_updated_network := network_repository.add(
            project_id=project, network=network
        )):
            raise HTTPException(
                status_code=404,
                detail="Project does not exist. Please create the project, first.",
            )
        return NetworkService.save_network_to_api(_updated_network)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Project does not exist. Please create the project, first.",
        ) from e


@router.post("/{project}/module")
async def add_module(
    project: str,
    module_body: Module,
    network_service: NetworkService = Depends(get_network_service),
) -> Module:
    """
    Adds a module to the network
    """
    try:
        _module = await run_in_threadpool(network_service.add_module, project, module_body)
        _logger.info(
            "Added the module to the network of project %s: %s",
            module_body,
            project,
        )
    except ModuleExistsError as e:
        raise HTTPException(
            status_code=400,
            detail="Module already exists",
        ) from e
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Network of project '{project}' does not exist.",
        ) from e

    return _module


@router.delete("/{project}/module/{module_id}")
async def delete_module(
    project: str,
    module_id: str,
    network_service: NetworkService = Depends(get_network_service),
):
    """
    delete a module from the network and removes the connections
    """
    try:
        await run_in_threadpool(network_service.delete_module, project, module_id)
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="Project does not exist. Please create the project, first.",
        ) from e
    _logger.info("Removing the module from the network")


@router.put("/{project}/module/{module_id}")
async def update_module(
    project: str,
    module_id: str,
    updated_module: Module,
    network_service: NetworkService = Depends(get_network_service),
) -> Module:
    """
    Change the input parameters of a module
    """
    try:
        _updated_module = await run_in_threadpool(network_service.update_module,
                                                  project, module_id, updated_module)
        return _updated_module
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="Project does not exist. Please create the project, first.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404,
            detail="Module does not exist.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with updating the module: {e}"
        ) from e


@router.get("/{project}/module/{module_id}/config")
async def get_module_config(
    project: str,
    module_id: str,
    network_service: NetworkService = Depends(get_network_service),
) -> ModuleConfig:
    """
    Return config of a module.
    """
    try:
        _config = await run_in_threadpool(network_service.get_module_config,
                                          project, module_id)
        return _config
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="Project does not exist. Please create the project, first.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404,
            detail="Module does not exist.",
        ) from e


@router.put("/{project}/module/{module_id}/config")
async def update_module_config(
    project: str,
    module_id: str,
    updated_config: ModuleConfig,
    network_service: NetworkService = Depends(get_network_service),
) -> ModuleConfig:
    """
    Update the config of a module.
    """
    try:
        _updated_config = await run_in_threadpool(network_service.update_module_config,
            project, module_id, updated_config)
        return _updated_config
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="Project does not exist. Please create the project, first.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404,
            detail="Module does not exist.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with setting the input configuration: {e}"
        ) from e


@router.post("/{project}/connection")
async def add_connection(
    project: str,
    connection: Connection,
    network_service: NetworkService = Depends(get_network_service),
):
    """
    connects an input of the module to the output of the other module,
    or vice versa. If automatic execution is set to True,
    the results will be updated automatically.
    """
    try:
        _connection = await run_in_threadpool(network_service.add_connection, project, connection)
        _logger.info("Connected the modules and updated the network")
        return _connection
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project} does not exist.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404, detail=f"The given module(s) doesn't exist: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem while connecting the modules: {e}"
        ) from e

@router.delete("/{project}/connection/{connection_id}")
async def delete_connection(
    project: str,
    connection_id: str,
    network_service: NetworkService = Depends(get_network_service),
):
    try:
        network = await run_in_threadpool(network_service.delete_connection,
                                          project,
                                          connection_id=connection_id)
        _logger.info("Remove connection between two modules")
        return NetworkService.save_network_to_api(network)
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project} does not exist.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404, detail=f"The given module(s) doesn't exist: {e}"
        ) from e
    except ConnectionNotExistsError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Connection {connection_id} doesn't exist: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with deleting the connection: {e}"
        ) from e


@router.get("/{project}/module/{module_id}/table")
async def get_module_table(
    project: str, module_id: str, page: int = 0, size: int = 20,
    network_service: NetworkService = Depends(get_network_service),
) -> TablePage:
    """View underlying data of module page by page.

    - **page**: page selection starting at 0
    - **size**: maximum number of items per page
    """
    try:
        output = await run_in_threadpool(
                            network_service.get_module_output_table,
                            project,
                            module_id,
                            page,
                            size)
        _logger.info("Getting the page number %i with the size of %i for module %s",
                     page, size, module_id)
        return output 
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project} does not exist.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404, detail=f"The given module(s) doesn't exist: {e}"
        ) from e
    except ResultNotFound as e:
        raise HTTPException(
            status_code=400, detail=f"No results found for the given module, please run the module: {e}"
        ) from e
    except ModuleWithoutOutputTable as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with fetching the output table: {e}"
        ) from e


@router.get("/{project}/module/{module_id}/visualize")
async def get_module_visualization(
    project: str, module_id: str,
    network_service: NetworkService = Depends(get_network_service),
) -> RenderedVisualization:
    """Returns a rendered visualization in form of a base64 encoded image.

    Depending on the actual implementation, we could also offer to
    - (1) generate links to images stored in the filesystem
    - (2) return the prepared data an render it in the frontend.
    """
    try:

        encoded_img = await run_in_threadpool(
                                network_service.get_module_output_plot,
                                project,
                                module_id)
        return RenderedVisualization(image=encoded_img)
    except NetworkNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project} does not exist.",
        ) from e
    except ModuleNotExistsError as e:
        raise HTTPException(
            status_code=404, detail=f"The given module(s) doesn't exist: {e}"
        ) from e
    except ResultNotFound as e:
        raise HTTPException(
            status_code=400, detail=f"No results found for the given module, please run the module: {e}"
        ) from e
    except NotVisualizationModule as e:
        raise HTTPException(
            status_code=400, detail=f'Not a Visualization Module: {e}'
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem with fetching the visualization: {e}"
        ) from e
