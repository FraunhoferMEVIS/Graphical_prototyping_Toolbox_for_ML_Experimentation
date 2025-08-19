""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: network_service.py
author: Lucas Rebscher
date: 12/2023
description: The network service
-----------------------------------------------------------------------------
"""
from data_preparation.models.network import (
                Module as ModuleModel, 
                ModuleConfig, 
                Connection, Network as NetworkModel,
                Column, 
                ColumnType,
                TablePage)
from data_preparation.repositories.network_repository import \
                                        NetworkRepository
from data_preparation.core.network import Network
from data_preparation.exceptions import (ModuleNotExistsError, ResultNotFound,
                                         NotVisualizationModule, ModuleWithoutOutputTable)


class NetworkService:
    """
    This service offers methods to perform actions, validations and manipulation on a network.

    It doesn't know about how a network is stored, it's only manipulating the network object directly while
    using further dependencies to orchestrate use cases.
    """

    def __init__(self, network_repository: NetworkRepository):
        self._network_repository = network_repository

    @staticmethod
    def create_network(project_id: str, network_dict: dict) -> Network:
        network = Network.load_network(project_id, network_dict)
        return network

    @staticmethod
    def load_network_from_api(project_id: str, network_model: NetworkModel) -> Network:
        """
        Generates a network from a network model
        """
        return Network.load_network(project_id, network_model.model_dump())

    @staticmethod
    def save_network_to_api(network: Network) -> NetworkModel:
        """
        Generates a network model from a network
        """
        network_dict = network.as_dict()
        return NetworkModel(
            id = network.id,
            modules = network_dict["modules"],
            connections = network_dict["connections"]
        )

    def add_module(self, project_id: str, new_module_request: ModuleModel) -> ModuleModel:
        network = self._network_repository.get(project_id)
        new_module = network.add_module(new_module_request)
        self._network_repository.add(project_id, network)
        return ModuleModel(**new_module)

    def get_module(self, project_id: str, module_id: str) -> ModuleModel:
        """
        Returns the module with the given id in the given project.
        raises ValueError if the project or the module do not exist.
        """
        network = self._network_repository.get(project_id)
        module = network.get_module(module_id)
        return ModuleModel(**module.as_dict())

    def delete_module(self, project_id: str, module_id: str) -> Network:
        """
        Deletes a module and all its connections from the network.
        """
        network = self._network_repository.get(project_id)
        network.delete_module(module_id)
        self._network_repository.add(project_id, network)
        return network

    def get_module_config(self, project_id: str, module_id: str) -> ModuleConfig:
        """
        Returns the configuration of the module with the given id in the given project.
        """
        network = self._network_repository.get(project_id)
        module = network.get_module(module_id)
        return ModuleConfig(parameters=module.parameters)

    def update_module(
        self, project_id: str, module_id: str, updated_module: ModuleModel
    ) -> ModuleModel:
        """
        Changes the module with the given id in the given project.
        """
        network = self._network_repository.get(project_id)
        updated_module = network.update_module(module_id, updated_module)
        self._network_repository.add(project_id, network)
        return ModuleModel(**updated_module)

    def update_module_config(
        self, project_id: str, module_id: str, updated_config: ModuleConfig
    ) -> ModuleConfig:
        """
        Changes the configuration of the module with the given id in the given project.
        """
        network = self._network_repository.get(project_id)
        config = network.update_module_config(module_id, updated_config)
        self._network_repository.add(project_id, network)
        return ModuleConfig(**config)

    def add_connection(self, project_id: str, connection: Connection):
        """
        Connects two modules in the network.
        """
        network = self._network_repository.get(project_id)
        network = network.connect_modules(connection)
        self._network_repository.add(project_id, network)
    
    def delete_connection(self, project_id: str, connection_id: str):
        """
        Disconnects two modules in the network.
        """
        network = self._network_repository.get(project_id)
        network = network.disconnect_modules(connection_id)
        self._network_repository.add(project_id, network)
        return network

    def run(self, project_id: str, module_id: str = None):
        """
        Runs the network or a single module.
        If module_id is None, the entire network is run.
        """
        network = self._network_repository.get(project_id)
        network = network.run(module_id)
        self._network_repository.add(project_id, network)
    
    def _get_module(self, project_id: str, module_id: str):
        network = self._network_repository.get(project_id)
        if module_id not in network.modules:
            raise ModuleNotExistsError
        module = network.modules[module_id]
        return module

    def get_module_output_plot(self, project_id: str, module_id: str):
        """
        Returns the output of the visualization modules with the
        given module_id, in the project_id.
        """
        module = self._get_module(project_id, module_id)
        if module.is_visualization_module():
            try:
                return module.get_output()
            except ValueError as e:
                raise ResultNotFound from e 
        raise NotVisualizationModule(f"The given module ({module_id}) is not a visualization module.")

    def get_module_output_table(self, project_id: str, module_id: str,
                                page: int, size: int):
        """
        returns the given page with the specified size of the output of the modules that
        generate a table as output 
        """
        module = self._get_module(project_id, module_id)
        if len(module.OUT_SOCKETS) == 0 and module.NAME != "export":
            raise ModuleWithoutOutputTable(
                f"The given module ({module_id}) doesn't have any output as table.")
        try:
            df = module.get_output(page=page, size=size)
        except ValueError as e:
            raise ResultNotFound from e
        dtypes = df.dtypes
        
        columns = {}
        for column_name, column_type in dtypes.items():
            if column_type.kind in {'i', 'f'}:
                columns[column_name] = ColumnType.NUMBER
            elif column_type == bool:
                columns[column_name] = ColumnType.BOOL
            else:
                columns[column_name] = ColumnType.STRING

        df = df.fillna(value="")
        return TablePage(
            columns=[
                    Column(name=column_name, type=column_type) for column_name, column_type in columns.items()
                ],
            data=df.to_dict(orient='records'),
    )
