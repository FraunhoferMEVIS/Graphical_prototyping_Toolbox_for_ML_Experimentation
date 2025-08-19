""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: network.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The model for a network
-----------------------------------------------------------------------------
"""
from typing import Self
from data_preparation.models.network import Module as ModuleModel, \
                                            ModuleConfig, Connection
from data_preparation.exceptions import ConnectionNotExistsError, \
                                        ModuleNotExistsError, ResultNotFound
from data_preparation.core.modules_repository import generate_module_from_state
from data_preparation.core.results_repository import FileResultsRepository
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER
from data_preparation.core.modules_repository.base_node import Node
from data_preparation.core.signal import Signal


class Network:
    def __init__(self, parent_project: str, storage_path: str = DATA_PREPARATION_PROJECTS_FOLDER) -> None:
        self.id = "network1"
        self.modules = {}
        self.connections = {}
        self._results_repo = FileResultsRepository(storage_path)
        self.parent_project = parent_project

    @classmethod
    def load_network(cls, parent_project: str, structure: dict) -> Self:
        """
        Generates a network from a list of connected modules

        :param structure: A dictionary containing the network structure
        :param parent_project: The project the network belongs to
        """
        if not structure:
            raise ValueError("Network not found")
        new_network = cls(parent_project)
        new_network.id = structure.get("id") or new_network.id
        for module in structure.get("modules"):
            if isinstance(module, dict):
                valid_results = module.get("valid_results", False)
                module = ModuleModel(**module)
            else:
                valid_results = False
            module = generate_module_from_state(module,
                                                new_network.parent_project,
                                                new_network._results_repo,
                                                valid_results=valid_results)
            new_network.modules[module.id] = module
        for connection in structure.get("connections"):
            new_connection = Connection(**connection) if isinstance(connection, dict) else connection
            new_network.connect_modules(new_connection, invalidate=False)
        return new_network

    def run(self, module_id: str=None, auto_apply: bool=True) -> Self:
        """
        Runs a network.
        If module_id is given, it will run only the given network,
        otherwise will run the entire network
        """
        if module_id:
            module = self.get_module(module_id)
            if not module or (not module.ready_to_run() and auto_apply is False):
                raise ResultNotFound(f"Module {module_id} is not ready to run")
            try:
                if not module.ready_to_run():
                    self.propagate_signal(module_id, Signal("run", forward=False, backward=True))
                module.run()
                # invalidate the results of next modules
                self.propagate_signal(module_id, signal=Signal("invalidate", forward=True, backward=False))
            except ResultNotFound as e:
                raise ResultNotFound(f"Module {module_id} is not ready to run") from e
            finally:
                self.modules[module_id] = module
        else:
            processed_modules = set()
            for module in self.modules.values():
                if module in processed_modules or module.valid_results:
                    continue

                if not module.ready_to_run():
                    self.propagate_signal(module.id, Signal("run", forward=False, backward=True))
                
                # if the module isn't still runnable, e.g. due to disconnected input, just ignore it!
                if module.ready_to_run():
                    module.run()
                else:
                    processed_modules.add(module.id)
        return self

    def as_dict(self) -> dict:
        """
        gets a json represontation of the network that can be easily saved to the file.
        """
        result = {
            "id": self.id,
            "parent_project": self.parent_project,
            "modules": [],
            "connections": []
        }
        for val in self.modules.values():
            result["modules"].append(val.as_dict())
        for val in self.connections.values():
            result["connections"].append(val.model_dump())
        return result

    def add_module(self, new_module_request: ModuleModel) -> dict:
        """
        Adds a Module to the network.
        The name is one of the defined Modules in the repository.
        """
        
        new_module = generate_module_from_state(
            new_module_request,
            self.parent_project,
            FileResultsRepository(DATA_PREPARATION_PROJECTS_FOLDER),
            valid_results=False
        )
        self.modules[new_module.id] = new_module
        return new_module.as_dict()
    
    def get_module(self, module_id: str) -> Node:
        """
        Returns the module with the given id in the given project.
        raises ValueError if the project or the module do not exist.
        """
        if module_id in self.modules:
            return self.modules[module_id]
        raise ModuleNotExistsError(f"Module {module_id} not found")
    
    def delete_module(self, module_id: str) -> Self:
        """
        Deletes the module with the given id.
        """
        if module_id in self.modules:
            # invalidate the results of next modules
            self.propagate_signal(self.modules[module_id],
                                  Signal("invalidate", forward=True, backward=False))

            del self.modules[module_id]
            remaining_connections = {}
            for connection in self.connections.values():
                if module_id == connection.sourceModule:
                    target_module = self.modules[connection.targetModule]
                    target_module.disconnect_input(connection.targetSocket)
                elif module_id == connection.targetModule:
                    # The modules don't store the output connections,
                    # so we don't need to update them
                    continue
                else:
                    remaining_connections[connection.id] = connection
            self.connections = remaining_connections
        return self

    def update_module_config(self, module_id: str, new_config: ModuleConfig) -> dict:
        """
        Updates the module with the given id.
        """
        if module_id in self.modules:
            module = self.modules[module_id]
            self.propagate_signal(module_id, Signal("invalidate", forward=True, backward=False))
            module.update_parameters(new_config.parameters)
            self.modules[module_id] = module
            return module.as_dict()["config"]
        raise ValueError(f"Module {module_id} not found")
    
    def update_module(self, module_id: str, new_module: ModuleModel) -> dict:
        """
        Updates the module with the given id.
        """
        if module_id in self.modules:
            module = self.modules[module_id]
            # overwrite only fields that should be modifiable
            module.label = new_module.label
            module.position = new_module.position
            self.modules[module_id] = module
            return module.as_dict()
        raise ValueError(f"Module {module_id} not found")
    
    def connect_modules(self,
                        connection: Connection, invalidate: bool=True) -> Self:
        """
        Connects two modules in the network.

        :param connection: The connection to be added to the network
        :param invalidate: Whether invalidate the target module or mot.
        :return: The updated network
        """
        if connection.id in self.connections:
            raise ValueError(f"Connection {connection.id} already exists")
        self.connections[connection.id] = connection
        target_module = self.modules[connection.targetModule]
        source_module = self.modules[connection.sourceModule]

        source_socket = connection.sourceSocket
        target_socket = connection.targetSocket
        # don't allow both sockets being input or same module as source and target:
        if connection.targetModule == connection.sourceModule or \
           (source_socket in source_module.get_input_sockets_names() and \
            target_socket in target_module.get_input_sockets_names()):
            raise ValueError ("This connection is not permitted.")
        # if the user started connection from output to the input
        if source_socket in source_module.get_input_sockets_names():
            source_module, target_module = target_module, source_module
            target_socket, source_socket = source_socket, target_socket
        # Each module has only one output socket
        self.modules[target_module.id] = target_module.connect_input(
                                            target_socket,
                                            source_module.id,
                                            invalidate=invalidate)
        # invalidate the results of next modules
        if invalidate:
            self.propagate_signal(target_module.id, Signal("invalidate", forward=True, backward=False))
        return self
    
    def disconnect_modules(self, connection_id: str) -> Self:
        """
        Disconnects two modules in the network.

        :param connection_id: The id of the connection to be removed from the network
        :return: The updated network
        """
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            target_module = self.modules[connection.targetModule]
            target_module.disconnect_input(connection.targetSocket)
            del self.connections[connection_id]
            self.propagate_signal(target_module.id, Signal("invalidate", forward=True, backward=False))
            return self
        raise ConnectionNotExistsError(f"Connection {connection_id} not found")
    
    def neighbors(self, module_id: str, forward: bool=True, backward: bool=True) -> list:
        """
        Returns the neighbors of the given module.
        """
        neighbors = []
        for connection in self.connections.values():
            if connection.sourceModule == module_id and forward:
                neighbors.append(self.modules[connection.targetModule])
            if connection.targetModule == module_id and backward:
                neighbors.append(self.modules[connection.sourceModule])
        return neighbors
    
    def propagate_signal(self, module_id: str, signal: Signal) -> Self:
        """
        Propagates the given signal through the network.
        """
        modules = self.neighbors(module_id,
                                 forward=signal.direction['forward'],
                                 backward=signal.direction['backward'])
        for module in modules:
            if signal.is_processed(module):
                # If the signal for the module is already processed:
                continue
            # recursively propagate the signal, if it cannot be processed, yet.
            if not signal.can_be_processed(module):
                self.propagate_signal(module.id, signal)
            signal.process(module)
