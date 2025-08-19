
""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: __init__.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The methods repositry
-----------------------------------------------------------------------------
"""
import importlib
import pkgutil
import inspect
from data_preparation.models.network import Module, ModuleConfigParameter
from data_preparation.core.results_repository import ResultsRepository
from data_preparation.core.modules_repository.base_node import Node, Socket


def generate_module_from_state(config: Module,
                               parent_project: str,
                               result_repo: ResultsRepository,
                               valid_results: bool = False) -> Node:
    """
    Generates a node from a state dictionary
    """
    try:
        module_id = config.id
        name = config.blueprint
        inputs = None
        if config.config is not None:
            parameters = config.config.parameters
        else:
            parameters = None
        if config.input_sockets is not None:
            inputs = []
            for socket in config.input_sockets:
                if socket is None:
                    inputs.append(None)
                else:
                    inputs.append(socket)
        position = config.position
        label = config.label
    except KeyError as e:
        raise ValueError(f"Missing key {e} in the provided state dictionary") from e
    
    module = module_finder.get_module(name=name,
                                      module_id=module_id,
                                      label=label,
                                      inputs=inputs,
                                      config=parameters,
                                      position=position,
                                      valid_results=valid_results,
                                      result_repo=result_repo,
                                      parent_project=parent_project
                                    )
    return module


class ModuleFinder:
    """
    Finds the modules in the given package.
    """
    def __init__(self, package_name: str) -> None:
        self.package_name = package_name
        self._load_list_of_moduels()

    def _load_list_of_moduels(self):
        """
        Get all classes of defined in the package, with their metadata.
        """
        self.list_of_modules = {}
        module_types = self.discover_modules()
        for module_name in module_types.values():
            module = importlib.import_module(module_name)
            classes = inspect.getmembers(module, inspect.isclass)

            for class_name, class_obj in classes:
                if issubclass(class_obj, Node):
                    self.list_of_modules[class_obj.NAME] = {
                        "import": module_name,
                        "class_name": class_name,
                        "help": inspect.getdoc(class_obj)
                    }

    def get_module(self,
                   name: str,
                   module_id: str=None,
                   label: str = None,
                   inputs: list[Socket]=None,
                   config: dict[str, ModuleConfigParameter]=None,
                   valid_results: bool=False,
                   position: dict=None,
                   result_repo: ResultsRepository=None,
                   parent_project: str="default",
                ) -> object:
        """
        It finds the class with the given name
        and instantiate an object of it.
        :param: name is the name of the module.
        :param: module_id, inputs, parent_project_path are the inputs of all modules that have in common.
        extra inputs can be passed using kwargs, if necessary.
        It returns the module of interest.
        """

        if name in self.list_of_modules:
            module = importlib.import_module(self.list_of_modules[name]["import"])
            class_obj = getattr(module, self.list_of_modules[name]["class_name"])
            return class_obj(module_id=module_id,
                             label=label,
                             inputs=inputs,
                             config=config,
                             valid_results=valid_results,
                             position=position,
                             result_repo=result_repo,
                             parent_project=parent_project,
                             )
        raise ValueError(f"Module '{name}' not found or does not inherit from Node.")

    def discover_modules(self) -> dict:
        """
        Finds all python modules in the package.
        """
        modules = {}
        pkg = importlib.import_module(self.package_name)
        for _, module_name, _ in pkgutil.walk_packages(pkg.__path__):
            modules[module_name] = f"{self.package_name}.{module_name}"

        return modules


module_finder = ModuleFinder("data_preparation.core.modules_repository")