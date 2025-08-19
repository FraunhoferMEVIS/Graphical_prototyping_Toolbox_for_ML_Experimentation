""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: node.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The model for a node
-----------------------------------------------------------------------------
"""
from enum import Enum
import importlib
import inspect
import pkgutil
from data_preparation.core.modules_repository import ModuleFinder


def get_all_classes(package_name, prefix=''):
    classes = []
    package = importlib.import_module(package_name)
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__, prefix=prefix):
        full_name = f"{package_name}.{name}"
        module = importlib.import_module(full_name)
        classes.extend(get_classes_in_module(module))
        if is_pkg:
            classes.extend(get_all_classes(full_name, prefix=f"{full_name}."))
    return classes


def get_classes_in_module(module):
    return [obj.NAME for _, obj in inspect.getmembers(module) \
            if inspect.isclass(obj) and obj.__module__ == module.__name__ and hasattr(obj, "NAME")]


class ModuleTypes(str, Enum):
    """
    list of all developed modules in the modules repository
    """
    _ignore_ = 'modules_set module member finder cls'
    cls = vars()
    modules_set = set()
    finder = ModuleFinder("data_preparation.core.modules_repository")
    for module in finder.discover_modules():
        modules_set.add(module)
    for member in modules_set:
        cls[member] = member


class Modules(str, Enum):
    """
    list of all developed modules in the modules repository
    """
    _ignore_ = 'modules_set module member finder cls'
    cls = vars()
    modules_set = set()
    finder = ModuleFinder("data_preparation.core.modules_repository")
    for module in finder.list_of_modules:
        modules_set.add(module)
    for member in modules_set:
        cls[member] = member
