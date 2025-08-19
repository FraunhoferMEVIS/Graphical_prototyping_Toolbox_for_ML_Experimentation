""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: exceptions.py
author: Lucas Rebscher
date: 12/2023
description: The exceptions
-----------------------------------------------------------------------------
"""


class DataPreparationError(Exception):
    """Base exception of this application."""


class ModuleExistsError(DataPreparationError):
    """A module with the same id already exists in the network."""


class ProjectNotFound(DataPreparationError):
    """The project does not exist."""


class ModuleNotExistsError(DataPreparationError):
    """The module does not exist."""


class NetworkNotFoundError(DataPreparationError):
    """Network does not exist yet."""


class ResultNotFound(DataPreparationError):
    """Result does not exist yet."""


class InternalError(DataPreparationError):
    """An internal error occurred."""


class ConnectionNotExistsError(DataPreparationError):
    """The connection does not exist."""


class NotVisualizationModule(DataPreparationError):
    """
    The input module is not a visualization module
    """


class ModuleWithoutOutputTable(DataPreparationError):
    """
    This module doesn't have any output as a table
    """