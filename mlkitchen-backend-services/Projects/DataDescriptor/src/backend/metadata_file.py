""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: metadata_file.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 08/2024
description: The backend for working with metadata file
-----------------------------------------------------------------------------
"""
import os
import shutil
import yaml
from src.models.features import MetadataModel
from src.backend.app_config import DATADESCRIPTOR_PROJECTS_FOLDER, \
                                   DATADESCRIPTOR_INPUT_DATA_CONFIG


def get_project_config_path(project_id: str) -> str:
    project_folder = os.path.join(DATADESCRIPTOR_PROJECTS_FOLDER,
                        project_id)
    if not os.path.exists(project_folder):
        raise ValueError(f"The given project {project_id} doesn't exist.")
    return os.path.join(project_folder, 'mlkitchen', 'metadata.yaml')


def get_project_metadata(project_id: str):
    """
    Opens and returns the metadata file.
    """
    metadata_file = get_project_config_path(project_id) if project_id \
        else DATADESCRIPTOR_INPUT_DATA_CONFIG
    if not os.path.exists(metadata_file):
        raise ValueError("No metada is defined for the given project.")
    with open(metadata_file, 'rt', encoding='utf8') as file_id:
        content = yaml.safe_load(file_id)
    return content


def setup_project_if_not_exist(project_id: str) -> None:
    if not os.path.exists(os.path.join(DATADESCRIPTOR_PROJECTS_FOLDER,
                                       project_id, 'mlkitchen')):
        os.makedirs(os.path.join(DATADESCRIPTOR_PROJECTS_FOLDER, project_id,
                                 'mlkitchen'))
    if not os.path.exists(get_project_config_path(project_id)):
        _set_default_project_features(project_id)


def save_project_metadata(project_id: str, metadata: MetadataModel) -> None:
    """
    saves the inpit metadata to the project
    """
    if not os.path.exists(os.path.join(DATADESCRIPTOR_PROJECTS_FOLDER,
                                       project_id, 'mlkitchen')):
        os.makedirs(os.path.join(DATADESCRIPTOR_PROJECTS_FOLDER, project_id,
                                 'mlkitchen'))
    config_path = get_project_config_path(project_id)
    metadata_dict = metadata.to_yaml_dict()
    with open(config_path, 'wt', encoding='utf8') as file_id:
        yaml.safe_dump(metadata_dict, file_id)
    return metadata_dict


def _set_default_project_features(project_id: str):
    shutil.copyfile(os.path.join(DATADESCRIPTOR_INPUT_DATA_CONFIG),
                    get_project_config_path(project_id))

