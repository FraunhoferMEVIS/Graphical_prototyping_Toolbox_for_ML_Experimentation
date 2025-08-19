""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: utilities.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: Some utilities used in different steps.
-----------------------------------------------------------------------------
"""
import os
import logging
import json
import yaml
import requests
from fastapi import HTTPException
from src.backend.app_config import REQUESTS_TIME_OUT


_logger = logging.getLogger(__name__)


_REQUEST_PROTOCOLS = ["GET", "POST", "DELETE", "PUT", "OPTIONS", "HEAD",
                      "PATCH"]


def input_parameters_to_str(parameters: dict):
    """
    The input parameters are converted to string
    :parameters: a dictionary of different parameters
    :returns an str
    """
    if not parameters:
        return ""
    params = ""
    for key, val in parameters.items():
        if isinstance(val, str):
            params += f"{key}='{val}', "
        else:
            params += f"{key}={val}, "
    return params


def save_config_to_yaml(config: dict, path) -> None:
    """
    saving a configuration to a yaml file.
    :config: a dict as input that should be written to the file
    :path: path to a 'yaml' file.
    """
    with open(path, 'w', encoding="utf-8") as outfile:
        yaml.safe_dump(config,
                       outfile,
                       default_flow_style=False,
                       sort_keys=False
                       )
    _logger.info('configuration saved to %s', path)


def load_yaml(path: str) -> dict:
    """
    Loads a yaml file to a dictionary and returns it.
    : path: path to a 'yaml' file.
    """
    with open(path, 'rt', encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    return data


def load_json(path: str) -> dict:
    """
    Loads a json file to a dictionary and returns it.
    : path: path to the 'json' file.
    """
    if not os.path.exists(path):
        return None
    with open(path, 'rt', encoding="utf-8") as file:
        return json.load(file)


def handle_requests(url, method=str, request_json=None):
    """
    Sends HTTP requests to a specified URL and returns the response.

    Parameters:
    :url (str): The URL to send the request to
    :method (RequestProtocol): The HTTP method to use (default is 'get')
    :headers (dict): A dictionary of headers to include in the request
      (default is None)
    :params (dict): A dictionary of query string parameters to include in the
        request (default is None)
    :data (dict): A dictionary of data to include in the request body
        (default is None)

    :returns: requests.Response: The response object from the server
    :raise error when an exception raised via request
    """
    if method not in _REQUEST_PROTOCOLS:
        raise ValueError(f'''{method} is not valid. It should be one of
        {', '.join(_REQUEST_PROTOCOLS)}''')
    try:
        response = requests.request(url=url,
                                    method=method,
                                    json=request_json,
                                    timeout=REQUESTS_TIME_OUT)
        if response.status_code >= 400:
            raise HTTPException(response.status_code, response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(500, "Server could not perform upstream request") from e


def get_largest_file_number_in_path(path: str):
    """
    If files or folders are saved in a directory
    with numbers as names, this function can be
    used to get the last sequential number.
    """
    largest = -1
    if not os.path.exists(path):
        return largest
    folders = os.listdir(path)
    for f in folders:
        if f.isnumeric():
            largest = max(int(f), largest)
    return largest
