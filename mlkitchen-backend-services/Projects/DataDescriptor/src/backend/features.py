""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: features.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: The backend for working with features
-----------------------------------------------------------------------------
"""
# from src.models.features import NewFeatureConfig
from .metadata_file import get_project_metadata#, setup_project_if_not_exist


def get_list_of_features(project_id: str = None):
    """
    get list of features for a specific project or the default data
    """
    # if project_id:
    #     setup_project_if_not_exist(project_id)
    
    meta_data = {"message": "No information is given for this dataset."}
    information = get_project_metadata(project_id)
    meta_data = {
        "keys": information.get("keys") or [],
        "features": information.get("features") or []
    }
    return meta_data


def get_feature_type(project_id: str, feature):
    """
    get type of a given feature int a specific project
    """
    features = get_list_of_features(project_id).get("features", None)
    for f in features:
        if f["name"] == feature:
            return f["type"]
    raise ValueError(f"""{feature} is not defined for this project \
                     ({project_id}).""")


def get_target(project_id: str):
    """
    Get the suggested target column in the given metadata
    """
    metadata = get_project_metadata(project_id)
    target = metadata.get("target", None)
    target_col = {
        'name': None,
        'type': None
    }
    if target:
        features = metadata.get('features') or []
        keys = metadata.get('keys') or []
        if target in keys:
            target_col["name"] = target
            target_col["type"] = "categorical" # assuming keys are always categorical
        else:
            for feature in features:
                if feature['name'] == target:
                    target_col = feature
                    break
    return target_col


# def add_new_feature_to_project(project_id: str, feature: NewFeatureConfig):
#     """
#     Adding a new feature to the project's data descriptor
#     """
#     raise NotImplementedError()


# def remove_feature(project_id: str, feature: str):
#     """
#     Removing a feature from a project's data descriptor
#     """
#     raise NotImplementedError()


# def undo_remove_feature(project_id: str, feature: str):
#     """
#     Put a removed feature backk in the data descriptor
#     """
#     raise NotImplementedError()
