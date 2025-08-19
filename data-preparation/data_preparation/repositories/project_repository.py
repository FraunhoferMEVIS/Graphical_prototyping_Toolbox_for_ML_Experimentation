""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: project_repository.py
author: Lucas Rebscher, Elham Taghizadeh
date: 12/2023
description: The project repositry
-----------------------------------------------------------------------------
"""
import os
from abc import ABC, abstractmethod
from shutil import rmtree
from data_preparation.core.app_config import DATA_PREPARATION_PROJECTS_FOLDER, \
                                             SERVICE_NAME
from data_preparation.exceptions import ProjectNotFound


class ProjectRepository(ABC):
    @abstractmethod
    def add(self, project_name: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, project_name: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_name: str):
        raise NotImplementedError

    @abstractmethod
    def deleteAll(self):
        raise NotImplementedError


class InMemoryProjectRepository(ProjectRepository):
    """
    A simple in-memory implementation of the ProjectRepository.

    Can be used during unit testing & in ongoing development.
    """
    def __init__(self):
        self._projects = {}

    def add(self, project_name: str):
        self._projects[project_name] = project_name

    def get(self, project_name: str) -> str | None:
        if project_name in self._projects:
            return self._projects[project_name]
        raise ProjectNotFound

    def delete(self, project_name: str):
        if project_name in self._projects:
            del self._projects[project_name]

    def deleteAll(self):
        self._projects = {}


class FileProjectRepository(ProjectRepository):
    def __init__(self) -> None:
        self._storage_path = DATA_PREPARATION_PROJECTS_FOLDER
        if not os.path.exists(self._storage_path):
            os.makedirs(self._storage_path)

    def add(self, project_name: str):
        project_path = os.path.join(self._storage_path,
                                    project_name)
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        project_path = os.path.join(project_path, SERVICE_NAME)
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        if not os.path.exists(os.path.join(project_path, "scripts")):
            os.mkdir(os.path.join(project_path, "scripts"))
        if not os.path.exists(os.path.join(project_path, "results")):
            os.mkdir(os.path.join(project_path, "results"))

    def get(self, project_name: str) -> str:
        project_path = os.path.join(self._storage_path,
                                    project_name,
                                    SERVICE_NAME)
        if not os.path.exists(project_path):
            raise ProjectNotFound
        return project_name

    def delete(self, project_name: str, force=False):
        project_path = os.path.join(self._storage_path,
                                    project_name)
        if not os.path.exists(project_path):
            return
        if os.listdir(project_path) and not force:
            raise IOError(
                """The project directory is not empty.
                Use force=True to delete it anyway.""")
        rmtree(project_path)

    def deleteAll(self):
        for project in os.listdir(self._storage_path):
            rmtree(os.path.join(self._storage_path, project))
