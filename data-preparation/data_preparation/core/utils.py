""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: utils.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The utility functions
-----------------------------------------------------------------------------
"""
import os
import json
import logging
from filelock import FileLock


def load_json(path: str) -> dict:
    """
    Loads a json file to a dictionary and returns it.
    :path: path to the 'json' file.
    """
    if not os.path.exists(path):
        return None
    lock_path = path + ".lock"
    lock = FileLock(lock_path)
    with lock:
        with open(path, 'rt', encoding="utf-8") as file:
            content = json.load(file)
            logging.info("Loading %s file.", path)
            logging.debug("Json file content %s", content)
            return content


def save_json(path: str, data: dict) -> None:
    """
    Saves the input data to a json file.
    It rewrites the existing file.
    """
    lock_path = path + ".lock"
    lock = FileLock(lock_path)

    try:
        with lock:
            with open(path, 'wt', encoding="utf-8") as file:
                json.dump(data, file)
                logging.info("Saved %s file.", path)
    except IOError as e:
        logging.error("Error in saving %s file. %s", path, e)
        raise e
