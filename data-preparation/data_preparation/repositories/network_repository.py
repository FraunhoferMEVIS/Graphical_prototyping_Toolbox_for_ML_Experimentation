""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: network_repository.py
author: Lucas Rebscher
date: 12/2023
description: The network repositry
-----------------------------------------------------------------------------
"""
import os
from abc import ABC, abstractmethod
from data_preparation.core.network import Network
from data_preparation.core.app_config import SERVICE_NAME
from data_preparation.exceptions import NetworkNotFoundError, ProjectNotFound
from data_preparation.core.utils import save_json, load_json


class NetworkRepository(ABC):
    @abstractmethod
    def add(self, project_id: str, network: Network) -> Network:
        raise NotImplementedError

    @abstractmethod
    def get(self, project_id: str) -> Network:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: str):
        raise NotImplementedError

    @abstractmethod
    def deleteAll(self):
        raise NotImplementedError


class InMemoryNetworkRepository(NetworkRepository):
    """A simple in-memory implementation of the NetworkRepository.

    Can be used during unit testing & in ongoing development.
    """

    def __init__(self):
        self._networks = {}

    def add(self, project_id: str, network: Network) -> Network:
        self._networks[project_id] = network
        return network

    def get(self, project_id: str) -> Network:
        if project_id in self._networks:
            return self._networks[project_id]
        return None

    def delete(self, project_id: str):
        if project_id in self._networks:
            del self._networks[project_id]

    def deleteAll(self):
        self._networks = {}


class FileNetworkRepository(NetworkRepository):
    """
    A File system implementation of the NetworkRepository.
    The network will be saved to the file system, and loaded from there.
    """
    def __init__(self, storage_path: str) -> None:
        super().__init__()
        self._storage_path = storage_path

    def add(self, project_id: str, network: Network) -> Network:
        project_path = os.path.join(self._storage_path, project_id, SERVICE_NAME)
        if not os.path.exists(project_path):
            raise ProjectNotFound

        save_json(path=os.path.join(project_path,
                                    'network.json'), 
                  data=network.as_dict())
        return network
    
    def get(self, project_id: str) -> Network:
        network_path = os.path.join(self._storage_path,
                                    project_id,
                                    SERVICE_NAME,
                                    'network.json')
        if os.path.exists(network_path):
            network = load_json(network_path)
            return Network.load_network(project_id, network)
        
        raise NetworkNotFoundError

    def delete(self, project_id: str) -> None:
        network_path = os.path.join(self._storage_path,
                                    project_id,
                                    SERVICE_NAME,
                                    'network.json')
        if os.path.exists(network_path):
            os.remove(network_path)

    def deleteAll(self):
        pass
