""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: methods.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2024
description: Workflow steps and method metadata for structured pipelines.
-----------------------------------------------------------------------------
"""
from typing import Any
from itertools import chain
from enum import Enum
from pydantic import BaseModel
from methods_repository.config_models import ProgrammingLanguages

class MainSteps(str, Enum):
    """
    All main Steps
    """
    Visualization = "Visualization"
    DataSplitting = "DataSplitting"
    HandlingMissingValues = "HandlingMissingValues"
    Sampling = "Sampling"
    Estimator = "Estimator"
    Metric = "Metric"
    NewFeature = "NewFeature"
    FeatureSelection = "FeatureSelection"
    Encoders = "Encoders"


class SubSteps(str, Enum):
    """
    These are the sub steps that can be selected within one of main steps,
    for example the Hyperparametertuining that should be selected within
    "Estimator" selection step.
    """
    HyperparameterTuning = "HyperparameterTuning"
    Distributions = "Distributions"


class Steps(str, Enum):
    """
    list of all steps and sub_steps such as distributions and tuning algorithms
    """
    _ignore_ = 'member cls'
    cls = vars()
    for member in chain(list(MainSteps), list(SubSteps)):
        cls[member.name] = member.value


class MethodParameters(BaseModel):
    """
    The structure of the parameters of the method
    """
    name: str
    type: str
    default: Any
    help: str | None = None
    options: list[str] | None = None
    min: Any
    max: Any


class MethodMetadata(BaseModel):
    """
    The structure of the output of the method metadata
    """
    name: str
    programming_language: ProgrammingLanguages
    step: Steps
    parameters: list[MethodParameters] = []
    help: str
