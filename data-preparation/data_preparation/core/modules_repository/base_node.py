""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: base_node.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The model for a node
-----------------------------------------------------------------------------
"""

import uuid
from typing import Self, Any
import logging
import pandas as pd
from data_preparation.models.network import Position, Socket, \
                                            ModuleConfigParameter
from data_preparation.core.results_repository import \
                        ResultsRepository,  FileResultsRepository, ResultTypes


_logger = logging.getLogger(__name__)

def config_parameter_dump(config: ModuleConfigParameter) -> dict:
    """
    It dumps the input parameters of the module.

    :param: config (dict): The input parameters of the module.
    :returns: The dumped input parameters of the module.
    """
    return {
        "id": config.id,
        "name": config.name,
        "description": config.description,
        "type": config.type.value if config.type else None,
        "required": config.required,
        "value": config.value,
        "multipleValues": config.multipleValues,
        "allowedValues": config.allowedValues,
    }

class Node:
    """
    The base model for a node. A node is a module in the network. It can have multiple inputs and outputs.
    :param: module_id (str): The id of the module. The default value is a random uuid.
    :param: inputs (list[Socket]): The list of input sockets of the module. The default value is None.
            The inputs represent the connections to the previous modules. 
            If the input is None, it means that the module is not connected to any other module yet.
            The names in the connections should match the names of the input sockets.
    """
    NAME = "base_module"
    IN_SOCKETS = [{"name": "input_1",
                   "required": False,
                   "value": None,
                   "description": "The input file"
                }]
    PARAMETERS: dict[str, ModuleConfigParameter] = {}
    OUT_SOCKETS = [Socket(name = "output_1",
                          value = None,
                          description = "The output file")]
    _CHUNKSIZE = 250000
    id: str = ""
    inputs: list[Socket] = None
    position: Position = None
    label: str = None
    error_message: str = ""
    valid_results: bool = False
    parent_project: str = None
    
    def __init__(self,
                 module_id: str = "",
                 label: str = None,
                 inputs: list[Socket] = None,
                 config: dict[str, ModuleConfigParameter] = None,
                 valid_results: bool = False,
                 position: Position = None,
                 parent_project: str = None,
                 result_repo: ResultsRepository = FileResultsRepository(),
                 ):
        """
           Initializes a Node object.

            :param: module_id (str): The id of the module.
            :param: inputs (list[Socket]): The list of input sockets of the module.
            :param: parent_project_path (str): The parent project path.
        """
        self.NUM_INPUTS = len(self.IN_SOCKETS)
        self._results_repo = result_repo
        self.parent_project = parent_project

        self.label = label if label else self.NAME
        self.position = position if position else Position(x=0, y=0)

        self._populate_parameters(config)

        input_names = {socket["name"]: i for i, socket in enumerate(self.IN_SOCKETS)}
        if not module_id:
            self.id = f"{self.NAME}_{str(uuid.uuid4())}"
        else:
            self.id = module_id
        self.valid_results = valid_results
        if inputs and len(inputs) > self.NUM_INPUTS:
            raise ValueError(f"Too many input files for module {self.NAME}")

        self.inputs = [None] * self.NUM_INPUTS
        if inputs:
            for socket in inputs:
                # Check if the input name is valid
                if socket is None:
                    continue
                if socket.name not in input_names:
                    raise ValueError(f"Invalid input name {socket.name} for module {self.NAME}")
                input_index = input_names[socket.name]
                self.inputs[input_index] = socket
        else:
            for i, socket in enumerate(self.IN_SOCKETS):
                self.inputs[i] = Socket(name=socket["name"], value=None)
    
    def validate_input_parameters(self) -> bool:
        """
        It validates the input parameters of the module.

        :param: parameters (dict): The input parameters of the module.
        :returns: True if the input parameters are valid and False otherwise.
        """
        for param_name, ref_param in self.PARAMETERS.items():
            if ref_param.get("required", None) and (param_name not in self.parameters or \
                                       self.parameters[param_name].value is None):
                return False
            if ref_param.get("type", None) not in (Any, self.parameters[param_name].type.value):
                return False
        return True
    
    def update_parameters(self, new_parameters: dict[str, ModuleConfigParameter]) -> None:
        """
        It updates the parameters of the module.

        :param: new_parameters (dict): The new input parameters of the module.
        """
        new_parameters = _clean_config_by_reference(new_parameters, self.PARAMETERS)
        self._populate_parameters(new_parameters)
        self.validate_input_parameters()

    def disconnect_input(self, input_name: str) -> None:
        """
        Disconnects the input socket with the given input name.
        """
        socket_names = self.get_input_sockets_names()
        if input_name not in socket_names:
            raise ValueError(f"Invalid input name {input_name} for module {self.NAME}")
        input_index = socket_names.index(input_name)
        self.inputs[input_index].value = None
        self.invalidate_output()

    def _populate_parameters(self, config: dict[str, ModuleConfigParameter]) -> None:
        """
        It populates the parameters of the module.

        :param: parameters (dict): The input parameters of the module.
        """
        self.parameters = {}
        if not config:
            for param_name, ref_param in self.PARAMETERS.items():
                self.parameters[param_name] = ModuleConfigParameter(**ref_param)
            return
        config = _clean_config_by_reference(config, self.PARAMETERS)
        for param_name, ref_param in self.PARAMETERS.items():
            if (input_param := config.get(param_name, None)) is None:
                self.parameters[param_name] = ModuleConfigParameter(**ref_param)
            else:
                for attr, value in input_param.model_dump().items():
                    if value is None:
                        setattr(input_param, attr, ref_param.get(attr, None))
                if ref_param.get("type", None) and ref_param["type"] not in (Any, input_param.type.value):
                    raise ValueError(f"Invalid input type {input_param.type} for module {self.NAME}")
                if input_param.allowedValues:
                    if input_param.multipleValues and isinstance(input_param.value, list):
                        for val in input_param.value:
                            if val not in input_param.value not in input_param.allowedValues:
                                raise ValueError(f"Invalid input value {val} for module {self.NAME}")
                    elif input_param.value and input_param.value not in input_param.allowedValues:
                        raise ValueError(f"Invalid input value {input_param.value} for module {self.NAME}")
                self.parameters[param_name] = input_param

    def write_output(self, result: pd.DataFrame, append=True) -> bool:
        """
        writes the results to the output file.

        :param: result (pd.DataFrame): The result of the module.
        :returns: True if the result is written successfully and False otherwise.
        """
        try:
            self._results_repo.add(project_name=self.parent_project,
                                   module_id=self.id,
                                   results=result,
                                   data_type=ResultTypes.DATAFRAME,
                                   append=append)
        except IOError as e:
            self.error_message = f"Failed to write the result of module {self.NAME} to the results repository: {e}"
            _logger.error(self.error_message)
            return False
        return True
    
    def write_metadata(self, metadata: dict) -> bool:
        """
        Writes the extracted metadata to the storage.
        :param: metadata: a dictionary with the name of data columns and their type.
        :returns: True if the metadata is written successfully and False otherwise.
        """
        if metadata:
            try:
                self._results_repo.add(
                    project_name=self.parent_project,
                    module_id=self.id,
                    results=metadata,
                    data_type=ResultTypes.DICT,
                    append=False
                )
            except IOError as e:
                self.error_message=f"Failed to write the output metadata for module {self.NAME} to the results repository: {e}"
                return False
        return True
    
    def get_input_metadata(self) -> dict[str, dict]:
        """
        Loads the metadata from all the given inputs of the module and
        returns them as a dictionary of dictionaries.
        :return: A dict of dicts. The first level keys represent the inputs,
                 the second level keys are the name of columns.
                 The values represent the type of data for each column.
        """
        metadata = {}
        for socket in self.inputs:
            input_metadata = self._results_repo.get(
                                self.parent_project,
                                socket.value,
                                ResultTypes.DICT
                            )
            metadata[socket.name] = input_metadata
        return metadata

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        """
        It computes the output metada, based on the input and the functionality of the module.
        Each module, shoould define it's own 'define_output_metadata.
        """
        if input_metadata is None:
            input_metadata = {}
        return input_metadata

    def run(self) -> None:
        """
        Runs the module.
        The functionality of the module is implemented in this method.
        """
        self.invalidate_output()
        if not self.validate_input_parameters():
            self.error_message = f"Invalid input parameters for module {self.NAME}"
            raise ValueError(self.error_message)

        if not self.required_inputs_connected():
            self.error_message = f"Missing required input connections for module {self.NAME}"
            raise TypeError(self.error_message)
    
    def required_inputs_connected(self) -> bool:
        return not any(socket['required'] and self.inputs[i] is None
                       for (i, socket) in enumerate(self.IN_SOCKETS))

    def as_dict(self) -> dict:
        """
        Returns the state of the node as a dictionary,
        that can be saved to a network.
        """
        state = {
            'id': self.id,
            'blueprint': self.NAME,
            'input_sockets': [socket.model_dump() for socket in self.inputs],
            'output_sockets': [socket.model_dump() for socket in self.OUT_SOCKETS],
            'valid_results': self.valid_results,
            'config': {"parameters": {param_name: config_parameter_dump(parameter) \
                       for param_name, parameter in self.parameters.items() if parameter}},
            'position': self.position.model_dump(),
            'label': self.label,
        }
        return state

    def invalidate_output(self) -> None:
        """
        Invalidates the output of the module.
        """
        self.valid_results = False
        self.error_message = ""
        self._results_repo.delete(project_name=self.parent_project,
                                  module_id=self.id)
    
    def connect_input(self, target_socket_name: str, source_module: str, invalidate: bool = True) -> Self:
        """
        Connects the input socket to the given input name.
        """
        if target_socket_name not in self.get_input_sockets_names():
            raise ValueError(f"Invalid input name {target_socket_name} for module {self.NAME}")
        input_index = self.get_input_sockets_names().index(target_socket_name)
        self.inputs[input_index].value = source_module
        if invalidate:
            self.invalidate_output()
        return self

    def get_input_sockets_names(self):
        return [socket.name for socket in self.inputs]
    
    def get_output_socket_name(self):
        return [socket.name for socket in self.OUT_SOCKETS]

    def ready_to_run(self) -> bool:
        """
        Checks if the module is ready to run.
        """
        # If all inputs are connected and the input parameters are valid
        if not self.validate_input_parameters() or \
           not self.required_inputs_connected():
            return False
        # if the results of previous modules are available
        return not any(not self._results_repo.result_exists(
                                            project_name=self.parent_project,
                                            module_id=socket.value)
                       for socket in self.inputs)
    
    def get_output(self, **kwargs):
        """
        If the outout is valid, it will return the requested page number,
        with the given size of the output table.
        """
        page = kwargs.get('page', 0)
        size = kwargs.get('size', 20)
        if self.valid_results:
            n = 0
            for chunk in self._results_repo.get(self.parent_project,
                                                self.id,
                                                data_type=ResultTypes.DATAFRAME,
                                                chunksize=size):
                if n == page:
                    break
                n += 1
            else: # page larger than data size
                chunk = chunk[0:0]
            return chunk
        raise ValueError("The output is not valid, please make sure to run the module, first!")
    
    def get_output_metadata(self):
        try:
             return self._results_repo.get(
                    project_name=self.parent_project,
                    module_id=self.id,
                    data_type=ResultTypes.DICT,
                )
        except IOError as e:
            raise ValueError(f"Failed to get the output metadata for module {self.NAME}: {e}") from e

    def is_visualization_module(self):
        return False


def _clean_config_by_reference(config: dict, ref_config: dict) -> dict:
    """
    It cleans the input config dict, in case some of the config keys are actually the ids in the ref_config
    """
    cleaned_config = {}
    ref_ids = {val['id']: key for key, val in ref_config.items() if isinstance(val, dict) and 'id' in val}
    for key, val in config.items():
        if key not in ref_config and key in ref_ids:
            cleaned_config[ref_ids[key]] = val
        else:
            cleaned_config[key] = val
    return cleaned_config