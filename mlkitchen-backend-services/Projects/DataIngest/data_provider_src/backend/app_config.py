""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: app_config.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: The needed input variables of the app. If not defined as
             environment variable, the default value is used.
-----------------------------------------------------------------------------
"""

import os
import logging
import yaml


_logger = logging.getLogger(__name__)


def _get_variable(name):
    return os.environ.get(name) or \
           _config.get(name)


def _get_path_variable(name, default):
    """
    :name: the name of the variable
    :default: the default value, if the name is not found in the environment
     variables or in the config
    :return: the absolute path for a given path variable
    1. if the variable is defined as environment variable, the relative path is
    considered with respect to this project. For example, "." means the root
    of this project or next to the serve.py file.
    2. If the variable is defined in a config file, the relative paths are
    defined with respect to the config file.
    For example "./input_metadata.yaml" means that the file should be next to
    the config file.
    3. If the variable is not defined in either of environment variables or the
    config file, it will role back to the default values and same as the first
    case, the relative paths are w.r.t. the project's root folder.
    """
    if name in os.environ:
        return os.path.abspath(os.environ[name])
    if name in _config:
        _config_folder = os.path.dirname(DATAINGEST_CONFIG_FILE)
        if not os.path.isabs(_config[name]):
            return os.path.abspath(os.path.join(_config_folder, _config[name]))
        return _config[name]
    return os.path.abspath(default)


if "DATAINGEST_CONFIG_FILE" in os.environ:
    DATAINGEST_CONFIG_FILE = os.environ["DATAINGEST_CONFIG_FILE"]
else:
    DATAINGEST_CONFIG_FILE = os.path.join('.', 'configuration', 'config.yaml')
DATAINGEST_CONFIG_FILE = os.path.abspath(DATAINGEST_CONFIG_FILE)
_logger.info("The configuration is going to be loaded from %s",
             DATAINGEST_CONFIG_FILE)

with open(DATAINGEST_CONFIG_FILE, 'rt', encoding='utf8') as config_file:
    _config = yaml.safe_load(config_file)

AISANDBOX_PROJECTS_FOLDER = _get_path_variable("AISANDBOX_PROJECTS_FOLDER",
                                               "./projects")
_logger.info("Projects are going to be saved under %s",
             AISANDBOX_PROJECTS_FOLDER)

Data_INGEST_HOST = _get_variable("Data_INGEST_HOST") or "0.0.0.0"
Data_INGEST_PORT = int(_get_variable("Data_INGEST_PORT")) or 8000
_logger.info("DATA-PROVIDER is served on %d port", Data_INGEST_PORT)

ROOT_PATH = str(_get_variable("ROOT_PATH")) or ""
_logger.info("AI-SANDBOX is submounted below %s path", ROOT_PATH)