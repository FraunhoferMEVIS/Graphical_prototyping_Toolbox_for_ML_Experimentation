""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: project.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The model for a project
-----------------------------------------------------------------------------
"""
import os
from typing import Self
from data_preparation.core.network import Network
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER, SERVICE_NAME
from data_preparation.core.utils import load_json, save_json
from data_preparation.core.node import Modules


class Project:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self.network = None
        self.__project_path = os.path.join(DATA_PREPARATION_PROJECTS_FOLDER, name)
        self.__path = os.path.join(self.__project_path, SERVICE_NAME)
        self.__network_file = os.path.join(self.__path, 'network1.json')
        self.__data_cache_folder = os.path.join(self.__path, 'data_cache')
        self.__user_scripts_folder = os.path.join(self.__path, 'scripts')
        if self.exists():
            if os.path.exists(self.__network_file):
                network_json = load_json(self.__network_file)
                self.network = Network.load_network(
                    self.name,
                    network_json.get('network')
                )

    @classmethod
    def create_project(cls, project_name:str, replace: bool=False) -> Self:
        new_project = cls(project_name)
        if new_project.exists() and not replace:
            raise FileExistsError(
                f"A project with the name of {project_name} already exists, I'll do nothing!")
        new_project.setup_project()
        new_project.network = Network(project_name, DATA_PREPARATION_PROJECTS_FOLDER)
        new_project.save()
        return new_project

    def setup_project(self):
        if not self.exists():
            if not os.path.exists(self.__project_path):
                os.mkdir(self.__project_path)
            os.mkdir(self.__path)
            os.mkdir(self.__data_cache_folder)
            os.mkdir(self.__user_scripts_folder)

    def exists(self):
        return os.path.exists(self.__path)
    
    def add_module(self, module_name: Modules) -> dict:
        """
        Adds a module to the project's network
        """
        if not self.exists():
            raise FileNotFoundError("The Project doesn't exist. Make sure to cretae the project first!")
        try:
            new_module = self.network.add_module(
                                        module_name,
                                    )
            self.save()
            return new_module
        except ValueError as e:
            raise ValueError from e
    
    def save(self) -> None:
        """
        Saves the project to the filesystem
        """
        if self.network is None:
            raise FileNotFoundError("The Project doesn't exist. Make sure to cretae the project first!")
        network_as_dict = self.network.as_dict()

        save_json(
            self.__network_file,
            {
                "name": self.name,
                "network": network_as_dict,
            }
        )
