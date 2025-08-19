""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: data_catalog.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: defining the structure of the input data.
-----------------------------------------------------------------------------
"""

import logging
from typing import Any
from src.backend.utilities import handle_requests
from methods_repository.config_models import DataTypes
from src.models.recipe import TargetConfig


_logger = logging.getLogger(__name__)


class DataAccess():
    """
    defined Data model. This is a temporary class and will be replaced soon.
    """
    __ddu: str
    __project_id: str
    __features: dict
    __keys: list[str]

    def __init__(self, data_descriptor_url: str,
                 project_id: str, **data: Any) -> None:
        super().__init__(**data)
        self.__ddu = data_descriptor_url
        self.__project_id = project_id
        resp = handle_requests(
                    url=f"{self.__ddu}/features/{self.__project_id}/list",
                    method="GET")
        if "features" in resp:
            _logger.info("Successfully connected to data descriptor.")
            self.__features = {feature["name"]: feature["type"]
                               for feature in resp["features"]}
        else:
            _logger.error("""Could not connect to data descriptor. \
                             Please make sure that the service is \
                             running and a correct url is provided.""")
        if "keys" in resp:
            self.__keys = list(resp["keys"])

    def get_attributes_list(self) -> list[str]:
        """
        returns the list of data columns/features
        """
        return list(self.__features.keys())

    def get_data_keys(self) -> list[str]:
        return self.__keys

    def data_type(self, key: str) -> DataTypes:
        """
        returns the Type of a given feature/column in the data model
        """
        if not self.__features:
            resp = handle_requests(
                    url=f"{self.__ddu}/features/{self.__project_id}/list",
                    method="GET")
            if "features" in resp:
                self.__features = resp.json()["features"]
                return [feature["name"] for feature in self.__features]
        if key in self.__features:
            return self.__features[key]
        raise ValueError(f"The {key} is not defined in the data model.")

    def get_target_col(self) -> TargetConfig:
        resp = handle_requests(
                    url=f"{self.__ddu}/features/{self.__project_id}/get_target_column",
                    method="GET")
        if resp and 'name' in resp and 'type' in resp:
            if resp["name"] and resp["type"]:
                return TargetConfig(
                    name=resp["name"],
                    type=resp["type"]
                )
            raise ValueError(f"The target column is not defined for the project {self.__project_id}")
        raise ValueError("Problem with getting the target column from metadata. Please make sure that data is exported from the data descriptor.")
