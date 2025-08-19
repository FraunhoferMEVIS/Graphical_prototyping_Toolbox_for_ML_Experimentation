""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: signal.py
author: Elham Taghizadeh, Lucas Rebscher
date: 04/2024
description: The signal model
-----------------------------------------------------------------------------
"""
from abc import ABC, abstractmethod
from data_preparation.core.modules_repository.base_node import Node


_RUN_SIGNAL_NAME = "run"
_INVALIDATE_SIGNAL_NAME = "invalidate"


class BaseSignal(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def can_be_processed(self, module: Node) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def process(self, module: Node):
        raise NotImplementedError


class RunSignal(BaseSignal):
    def __init__(self) -> None:
        super().__init__(_RUN_SIGNAL_NAME)
    
    def can_be_processed(self, module: Node) -> bool:
        return module.ready_to_run()

    def process(self, module: Node):
        if not self.can_be_processed(module):
            raise ValueError(f"Cannot process signal {self.name} for module {module.id}")
        return module.run()
    
    def is_processed(self, module: Node) -> bool:
        return module.valid_results


class InvalidateSignal(BaseSignal):
    def __init__(self) -> None:
        super().__init__(_INVALIDATE_SIGNAL_NAME)
    
    def can_be_processed(self, module: Node=None) -> bool:
        return True
    
    def process(self, module: Node):
        return module.invalidate_output()
    
    def is_processed(self, module: Node) -> bool:
        return not module.valid_results


class Signal:
    def __init__(self, signal_name: str,
                 forward: bool = True,
                 backward: bool = True) -> None:
        if signal_name not in (_RUN_SIGNAL_NAME, _INVALIDATE_SIGNAL_NAME):
            raise ValueError("Only run and invalidate signals are supported")
        if not(forward or backward):
            raise ValueError("At least one of forward or backward must be True")
        self.direction = {
            "forward": forward,
            "backward": backward,
        }
        
        if signal_name == _RUN_SIGNAL_NAME:
            self._signal = RunSignal()
        else:
            self._signal = InvalidateSignal()

    def can_be_processed(self, module: Node) -> bool:
        return self._signal.can_be_processed(module)

    def process(self, module: Node):
        return self._signal.process(module)

    def is_processed(self, module: Node) -> bool:
        return self._signal.is_processed(module)