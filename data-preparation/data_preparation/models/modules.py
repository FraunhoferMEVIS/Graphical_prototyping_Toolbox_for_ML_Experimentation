""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: modules.py
author: Lucas Rebscher
date: 12/2023
description: pydantic models
-----------------------------------------------------------------------------
"""
from enum import Enum
from pydantic import BaseModel


class ModuleCategory(str, Enum):
    TABLE = "Table"
    TABLE_MERGE = "Table-Merge"
    FILTER = "Filter"
    PREPROCESS = "Preprocess"
    VISUALIZE = "Visualize"
    AGGREGATE_AND_TRANSFORM = "Aggregate and Transform"


class ModuleBlueprint(BaseModel):
    id: str
    # category of blueprint
    category: ModuleCategory
    title: str
    subtitle: str = ""
    description: str = ""
