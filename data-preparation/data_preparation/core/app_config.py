""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: app_config.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description:  initializes configuration settings by loading environment 
            variables, a configuration file, default values, 
            and sets up paths, URLs, database credentials, and other service parameters
-----------------------------------------------------------------------------
"""

import os
import logging
import yaml


_logger = logging.getLogger(__name__)


def _get_variable(name):
    if name in os.environ:
        return os.environ[name]
    if name in _config:
        return _config[name]
    return None


def _get_path_variable(name, default):
    """
    :name: the name of the variable
    :default: the default value, if the name is not found in the environment
     variables or in the config
    :return: the absolute path for a given path variable
    1. if the variable is defined as environment variable, the relative path is
    considered with respect to this project. For example, "." means the root
    of this project or next to the aisandbox_server.py file.
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
        _config_folder = os.path.dirname(AISANDBOX_CONFIG_FILE)
        if not os.path.isabs(_config[name]):
            return os.path.abspath(os.path.join(_config_folder, _config[name]))
        return _config[name]
    return os.path.abspath(default)


if "AISANDBOX_CONFIG_FILE" in os.environ:
    AISANDBOX_CONFIG_FILE = os.environ["AISANDBOX_CONFIG_FILE"]
else:
    AISANDBOX_CONFIG_FILE = os.path.join('configuration', 'config.yaml')
AISANDBOX_CONFIG_FILE = os.path.abspath(AISANDBOX_CONFIG_FILE)
_logger.info("The configuration is going to be loaded from %s",
             AISANDBOX_CONFIG_FILE)

with open(AISANDBOX_CONFIG_FILE, 'rt', encoding="utf-8") as config_file:
    _config = yaml.safe_load(config_file)

SERVICE_NAME = _get_variable("SERVICE_NAME") or "maratus"

DATA_PREPARATION_PROJECTS_FOLDER = _get_path_variable("DATA_PREPARATION_PROJECTS_FOLDER",
                                                      './projects')
_logger.info("Projects are going to be saved under %s",
             DATA_PREPARATION_PROJECTS_FOLDER)

DATA_PREPROCESSING_PORT = int(_get_variable("DATA_PREPROCESSING_PORT")) or 6050
_logger.info("AI-SANDBOX is served on %d port", DATA_PREPROCESSING_PORT)

ROOT_PATH = str(_get_variable("ROOT_PATH")) or ""
_logger.info("AI-SANDBOX is submounted below %s path", ROOT_PATH)

AISANDBOX_URL = _get_variable("AISANDBOX_URL") or "http://0.0.0.0:8000"
_logger.info("AI-SANDBOX is served on %d port", AISANDBOX_URL)

DATA_DESCRIPTOR_URL = _get_variable("DATA_DESCRIPTOR_URL") or \
                     "http://0.0.0.0:8080"

DATASET_URL = _get_variable("DATASET_URL") or \
             ""

DATA_PROVIDER_URL = _get_variable("DATA_PROVIDER_URL") or \
                    "http://0.0.0.0:8088"

REQUESTS_TIME_OUT = _get_variable("REQUESTS_TIME_OUT") or 300

POSTGRES_HOST = _get_variable("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = _get_variable("POSTGRES_PORT") or 5432
POSTGRES_DB = _get_variable("POSTGRES_DB") or "mimmiciv"
POSTGRES_USER = _get_variable("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = _get_variable("POSTGRES_PASSWORD") or "postgres"

DATA_PREPARATION_CSV_REPO = _get_path_variable("DATA_PREPARATION_CSV_REPO", "./projects/csv_datasets")