""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: recipe.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The models defined for the recipe input of the api
-----------------------------------------------------------------------------
"""
from enum import Enum
from pydantic import BaseModel
from methods_repository.config_models import AlgorithmConfig, MetricsConfig, \
                                             ColumnTransformerConfig, \
                                             SplitConfig


class StepConfig(BaseModel):
    """
    The structure of the input configuration of the step
    """
    step_name: str
    config: SplitConfig | list[ColumnTransformerConfig] | \
        list[MetricsConfig] | list[AlgorithmConfig]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "step_name": "impute",
                "config": {
                    "name": "ReplaceWithMedian",
                    "parameters": {
                        "columns": ["TSH", "T3", "T4"],
                    }
                }
            }]
        }
    }


class DataTypes(str, Enum):
    """
    Different types of input columns
    """
    numerical="numerical"
    categorical="categorical"


class TargetConfig(BaseModel):
    name: str
    type: DataTypes