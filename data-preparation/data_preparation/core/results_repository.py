""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: results_repository.py
author: Elham Taghizadeh, Lucas Rebscher
date: 01/2024
description: The results repositry
-----------------------------------------------------------------------------
"""

import os
import glob
from io import BytesIO
import base64
from enum import Enum
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from data_preparation.core.app_config import SERVICE_NAME, DATA_PREPARATION_PROJECTS_FOLDER
from data_preparation.core.utils import load_json, save_json
from data_preparation.exceptions import ProjectNotFound, ResultNotFound


# The file formats that are supported. for each data type.
DATAFRAME_FILE_FORMAT = "csv"
IMAGE_FILE_FORMAT = "png"
DICT_FILE_FORMAT = "json"


class ResultTypes(str, Enum):
    """
    The ResultTypes class is an enumeration of the different
    result types that can be saved.
    """
    DATAFRAME = "dataframe"
    IMAGE = "image"
    DICT = "dict"


class DataIO(ABC):
    """
    The DataIO class is an abstract class for reading and 
    writing data to the file system.
    """
    @abstractmethod
    def read(self, path: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def write(self, path: str, data: Any, append: bool = True):
        raise NotImplementedError


class ResultsRepository(ABC):
    """
    The ResultsRepository class is an abstract class for
    reading and writing the results data from modules.
    
    :param: dataIO is an instance of the DataIO class,
    depending on the data that should be written. For example,
    this could be DataFrameIO or ....
    :param: file_format is the file format that the results should be saved in.
    The default is csv.
    """
    @abstractmethod
    def add(self, project_name: str,
            module_id: str,
            results: Any,
            data_type: ResultTypes
            ):
        raise NotImplementedError

    @abstractmethod
    def get(self, project_name: str,
            module_id: str,
            data_type: ResultTypes,
            **kwargs) -> dict | None:
        raise NotImplementedError
    
    @abstractmethod
    def result_exists(self, project_name: str,
                      module_id: str,
                      data_type: ResultTypes=ResultTypes.DATAFRAME
                    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_name: str, module_id: str):
        raise NotImplementedError


class FileResultsRepository(ResultsRepository):
    """
    The FileResultsRepository class is an implementation of the
    ResultsRepository class to the file system.
    """
    def __init__(self, storage_path: str=DATA_PREPARATION_PROJECTS_FOLDER):
        super().__init__()
        self._repo_path = storage_path
        self.RESULT_FOLDER = "results"

    def add(self,
            project_name: str,
            module_id: str,
            results: Any,
            data_type: ResultTypes,
            append: bool=True) -> None:
        """
        It adds the results of a module to the file system.
        If the file already exists, it will be overwritten.

        :param: project_name is the name of the project.
        :param: module_id is the id of the module that the
        results should be saved for.
        :param: results is the output results of the module.
        :param: dataIO is an instance of the DataIO class, depending
        on the data that should be written. For example, this could be
        DataFrameIO or ....
        :raises: ProjectNotFound if the project does not exist.
        """
        results_path = os.path.join(self._repo_path,
                                    project_name,
                                    SERVICE_NAME,
                                    self.RESULT_FOLDER)
        if not os.path.exists(results_path):
            raise ProjectNotFound(project_name)
        file_format = get_file_format(data_type)
        data_io = get_IO(data_type)
        filename = os.path.join(results_path, f"{module_id}.{file_format}")
        data_io.write(filename, results, append=append)

    def get(self,
            project_name: str,
            module_id: str,
            data_type: ResultTypes,
            **kwargs) -> Any:
        """
        It loads and returns the results of a module from the file system.

        :param: project_name is the name of the project.
        :param: module_id is the id of the module that the results should be
        loaded for.
        :param: data_type is the type of the data that should be loaded.
        """
        results_path = os.path.join(self._repo_path,
                                    project_name,
                                    SERVICE_NAME,
                                    self.RESULT_FOLDER)
        if not os.path.exists(results_path):
            raise ProjectNotFound(project_name)

        file_format = get_file_format(data_type)
        filename = os.path.join(results_path, f"{module_id}.{file_format}")
        if not os.path.exists(filename):
            raise ResultNotFound(project_name)
        data_io = get_IO(data_type)
        chunksize = kwargs.get("chunksize", None)
        return data_io.read(filename, chunksize=chunksize)
    
    def result_exists(self, project_name: str,
                      module_id: str,
                      data_type: ResultTypes=ResultTypes.DATAFRAME) -> bool:
        """
        It checks if the result file of a module exists in the results repo.

        :param: project_name is the name of the project.
        :param: module_id is the id of the module that the results should be
        checked for.
        """
        results_path = os.path.join(self._repo_path,
                                    project_name,
                                    SERVICE_NAME,
                                    self.RESULT_FOLDER)
        if not os.path.exists(results_path):
            raise ProjectNotFound(project_name)
        file_format = get_file_format(data_type)
        filename = os.path.join(results_path, f"{module_id}.{file_format}")
        return os.path.exists(filename)
    
    def delete(self, project_name: str, module_id: str) -> None:
        """
        It deletes all the result files of a module from the results repo.

        :param: project_name is the name of the project.
        :param: module_id is the id of the module that the results should be
        deleted for.
        """
        project_path = os.path.join(self._repo_path, project_name, SERVICE_NAME)
        if not os.path.exists(project_path):
            raise ProjectNotFound(project_name)
        results_path = os.path.join(project_path,
                                    self.RESULT_FOLDER)
        all_module_results = glob.glob(os.path.join(results_path,
                                                   f"{module_id}.*"))
        for result_file in all_module_results:
            os.remove(result_file)

class DataFrameIO(DataIO):
    """
    The DataFrameIO class is an implementation of the
    DataIO class for reading and writing DataFrame in 
    different file formats.
    """
    def read(self, path: str, **kwargs) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError
        if path.endswith(".csv"):
            return pd.read_csv(path, **kwargs)
        if path.endswith(".pkl"):
            return pd.read_pickle(path, **kwargs)
        if path.endswith("parquet"):
            return pd.read_parquet(path, **kwargs)
        raise NotImplementedError("File format not supported.")
    
    def write(self, path: str, data: pd.DataFrame, append: bool=True):
        if path.endswith(".csv"):
            data.reset_index()
            data.to_csv(path, index=False,
                        mode="a" if append else "w",
                        header=not (os.path.exists(path) and append))
        elif path.endswith(".pkl"):
            if append and os.path.exists(path):
                old_data = pd.read_pickle(path)
                data = pd.concat([old_data, data], ignore_index=True)
            data.to_pickle(path)
        elif path.endswith("parquet"):
            if append and os.path.exists(path):
                old_data = pd.read_parquet(path)
                data = pd.concat([old_data, data], ignore_index=True)
            data.to_parquet(path)
        else:
            raise NotImplementedError("File format not supported.")


class DictIO(DataIO):
    """
    The DictIO class is an implementation of the
    DataIO class for reading and writing dictionaries in 
    different file formats.
    """
    def read(self, path: str, **kwargs) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError
        if path.endswith(".json"):
            return load_json(path)
        raise NotImplementedError("File format not supported.")
    
    def write(self, path: str, data: dict, append=None) -> None:
        """
        Saves the results to the path.
        :path: path to save the data to
        :data: a dictionary that should be saved.
        :append: is not used! Added only for consistency!
        """
        if path.endswith(".json"):
            save_json(path, data=data)
        else:
            raise NotImplementedError("File format not supported.")


class ImageIO(DataIO):
    """
    The ImageIO class is an implementation of the
    DataIO class for reading and writing plots in 
    different file formats.
    """
    def read(self, path: str, **kwargs):
        """
        Not implemented yet, as we don't need the images for now
        """
        if not os.path.exists(path):
            raise FileNotFoundError
        if path[-4:] in {".png", ".svg", ".pdf"}:
            encoded_img = None
            image = Image.open(path)
            with BytesIO() as image_bytes:
                image.save(image_bytes,
                           format="png",
                )
                image_bytes.seek(0)
                encoded_img = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
                
            return encoded_img
        raise NotImplementedError("File format not supported.")
    
    def write(self, path: str, data: plt.figure, append=None) -> None:
        """
        Saves the results to the path.
        :path: path to save the data to
        :data: a list of matplotlib.pyplot axes to be saved.
        :append: is not used! Added only for consistency!
        """
        if path[-4:] in {".png", ".svg", ".pdf"}:
            if hasattr(data, 'get_axes'):
                axes = data.get_axes()
                for ax in axes:
                    if not ax.lines and not ax.collections and not ax.bar:
                        data.delaxes(ax)
            if hasattr(data, 'tight_layout'):
                data.tight_layout()
            data.savefig(path)
        else:
            raise NotImplementedError("File format not supported.")


def get_IO(data_type: ResultTypes) -> DataIO:
    """
    The get_IO function returns an instance of the DataIO class
    depending on the file format.

    :param: file_format is the file format of the data that should
    be read or written.
    :raises: NotImplementedError if the file format is not supported.
    """
    if data_type == ResultTypes.DATAFRAME:
        return DataFrameIO()
    if data_type == ResultTypes.IMAGE:
        return ImageIO()
    if data_type == ResultTypes.DICT:
        return DictIO()
    return None


def get_file_format(data_type: ResultTypes) -> str:
    """
    The get_file_format function returns the file format
    depending on the data type.

    :param: data_type is the type of the data that should be read or written.
    :raises: NotImplementedError if the data type is not supported.
    """
    if data_type == ResultTypes.DATAFRAME:
        return DATAFRAME_FILE_FORMAT
    if data_type == ResultTypes.IMAGE:
        return IMAGE_FILE_FORMAT
    if data_type == ResultTypes.DICT:
        return DICT_FILE_FORMAT
