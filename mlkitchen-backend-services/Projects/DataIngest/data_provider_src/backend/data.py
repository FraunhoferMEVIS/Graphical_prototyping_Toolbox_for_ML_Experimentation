""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: data.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 03/2023
description: The model to split data, load data and required configuration.
-----------------------------------------------------------------------------
"""
import os
from glob import glob
from pandas import read_parquet, read_pickle, Series
from methods_repository.config_models import RecipeConfig
from methods_repository.abstraction import ModuleFinder
from data_provider_src.backend.app_config import AISANDBOX_PROJECTS_FOLDER


def load(project_id: str):
    """
    Loads the parquet data stored in the project folder and returns it.
    """
    data_location = os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                 'mlkitchen', 'data', 'data.parquet')
    if os.path.exists(data_location):
        return read_parquet(data_location)
    raise IOError("The data file does not exist for the given project.")


def split(project_id: str, config: RecipeConfig):
    """
    Splits the data of a given project based on the input SplitConfig.
    The results is saved as pickle files for use when running of the recipes.
    """
    _clean_up_old_splits(project_id)
    split_conf = config.split
    if not (parameters := split_conf.parameters):
        parameters = {}

    if config.task == 'classification':
        parameters['target_col'] = config.target_col

    if not split_conf.name:
        if config.task == 'classification':
            split_conf.name = "StratifiedShuffleSplit"
        else:
            split_conf.name = "ShuffleSplit"
        if split_conf.ratio:
            parameters['test_size'] = split_conf.ratio[2]
            parameters['validation_size'] = split_conf.ratio[1]
    try:
        splitter = ModuleFinder.use_method("DataSplitting", split_conf.name,
                                           split_conf.language or "python",
                                           **parameters)
    except (ValueError, NameError) as e:
        return 0, e

    project_data_path = os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                     'mlkitchen', 'data')
    data_path = os.path.join(project_data_path, 'data.parquet')
    if os.path.exists(data_path):
        input_data = read_parquet(data_path)
    else:
        return 0, f"No data file (data.parquet) was found for {project_id}"
    try:
        results = splitter.split(input_data)
        for i, result in enumerate(results):
            result.to_pickle(os.path.join(project_data_path, f'split_{i}'))
    except (IOError, ValueError) as e:
        return 0, e
    return len(results), "Split Indices saved!"


def get_split_indices(project_id: str, split_num: int = 0) -> Series:
    """
    returns the split indices of a specific split of a project.
    If the input split_num is larger than number of existing splits,
    It will raise an error, otherwise the indices are returned as
    Pandas Series.
    :project_id: is the name of the project.
    :split_num: in case more than one folds or splits are saved for the
    project, for example in case of 5-fold split, with this number the
    specific split can be request. The default value is 0
    """
    indices_path = os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                'mlkitchen', 'data', f'split_{split_num}')
    if not os.path.exists(indices_path):
        raise ValueError(
            f"The '{project_id}' contains only {split_num} or fewer splits."
            )
    indices = read_pickle(indices_path)
    return indices


def split_data_exists(project_id: str) -> bool:
    return len(glob(os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                 'mlkitchen', 'data', f'split_*'))) > 0


def _clean_up_old_splits(project_id: str) -> None:
    split_indices = glob(os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                      'mlkitchen', 'data', 'split_*'))
    for file in split_indices:
        os.remove(file)


def get_num_splits(project_id: str):
    """
    Returns the number of splits saved in the project data space.
    """
    return len(glob(os.path.join(AISANDBOX_PROJECTS_FOLDER, project_id,
                                 'mlkitchen', 'data', 'split_*')))