""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: dummy.py
author: Lucas Rebscher
date: 12/2023
description: The dummy data
-----------------------------------------------------------------------------
This module contains dummy data used for ongoing development.

It can be removed in a later stage.
"""
import uuid
from data_preparation.models.modules import ModuleBlueprint, ModuleCategory
from data_preparation.models.network import (
                Connection, Module, ModuleConfig,
                Network as NetworkModel, Position)


def create_module_blueprints() -> list[ModuleBlueprint]:
    return [
        ModuleBlueprint(
            id="sqlTable",
            category=ModuleCategory.TABLE,
            title="SQL Table",
        ),
        ModuleBlueprint(
            id="load-csv-file",
            category=ModuleCategory.TABLE,
            title="Load CSV",
        ),
        ModuleBlueprint(
            id="filter-by-value",
            category=ModuleCategory.FILTER,
            title="Filter By Values",
        ),
        ModuleBlueprint(
            id="table-merge",
            category=ModuleCategory.TABLE_MERGE,
            title="Table Merge",
        ),
        ModuleBlueprint(
            id="new-column",
            category=ModuleCategory.AGGREGATE_AND_TRANSFORM,
            title="New Column",
        ),
        ModuleBlueprint(
            id="aggregateAndTransform",
            category=ModuleCategory.AGGREGATE_AND_TRANSFORM,
            title="Aggregate and Transform",
        ),
        ModuleBlueprint(
            id="convert-unit",
            category=ModuleCategory.PREPROCESS,
            title="Unit Conversion",
        ),
        ModuleBlueprint(
            id="comorbidity",
            category=ModuleCategory.AGGREGATE_AND_TRANSFORM,
            title="Comorbidity",
        ),
        ModuleBlueprint(
            id="aggregate-and-transform-multi-columns",
            category=ModuleCategory.AGGREGATE_AND_TRANSFORM,
            title="Aggregate and Transform Multi Columns",
        ),
        ModuleBlueprint(
            id="filter-by-condition",
            category=ModuleCategory.FILTER,
            title="Filter by Condition"
        ),
        ModuleBlueprint(
            id="assign-timewindow",
            category=ModuleCategory.PREPROCESS,
            title="Assign Timewindow",
        ),

        ModuleBlueprint(
            id="sample-timeevents",
            category=ModuleCategory.PREPROCESS,
            title="Sample Events to Timewindow",
        ),

        ModuleBlueprint(
            id="scatter-plot",
            category=ModuleCategory.VISUALIZE,
            title="Scatter Plot",
        ),
        ModuleBlueprint(
            id="bar-plot",
            category=ModuleCategory.VISUALIZE,
            title="Bar Plot",
        ),
        ModuleBlueprint(
            id="histogram-plot",
            category=ModuleCategory.VISUALIZE,
            title="Histogram Plot",
        ),
        ModuleBlueprint(
            id="line-plot",
            category=ModuleCategory.VISUALIZE,
            title="Line Plot",
        ),
        ModuleBlueprint(
            id="joint-plot",
            category=ModuleCategory.VISUALIZE,
            title="Joint Plot",
        ),
        ModuleBlueprint(
            id="pair-plot",
            category=ModuleCategory.VISUALIZE,
            title="Pair Plot",
        ),
        ModuleBlueprint(
            id="flag-by-condition",
            category=ModuleCategory.PREPROCESS,
            title="Flag by Condition",
        ),
        ModuleBlueprint(
            id="select-event",
            category=ModuleCategory.FILTER,
            title="Select Event",
        ),
        ModuleBlueprint(
            id="delete-column",
            category=ModuleCategory.PREPROCESS,
            title="Delete Column",
        ),
        ModuleBlueprint(
            id="export",
            category=ModuleCategory.TABLE,
            title="Export Data",
        ),
        ModuleBlueprint(
            id="edit-column-name",
            category=ModuleCategory.PREPROCESS,
            title="Edit Column Name",
        ),
        ModuleBlueprint(
            id="edit-data-type",
            category=ModuleCategory.PREPROCESS,
            title="Edit Data Type",
        ),
    ]


def create_network() -> NetworkModel:
    modules = [
        Module(
            id=str(uuid.uuid4()),
            label="My input table",
            config=ModuleConfig(),
            position=Position(x=100, y=100),
            blueprint="table",
            input_sockets=[],
            output_sockets=[],
        ),
        Module(
            id=str(uuid.uuid4()),
            label="My filter",
            config=ModuleConfig(),
            position=Position(x=500, y=150),
            blueprint="filter",
            input_sockets=[],
            output_sockets=[],
        ),
        Module(
            id=str(uuid.uuid4()),
            label="My Visualization",
            config=ModuleConfig(),
            position=Position(x=900, y=150),
            blueprint="visualize",
            input_sockets=[],
            output_sockets=[],
        ),
    ]
    return NetworkModel(
        modules=modules,
        connections=[
            Connection(
                id=str(uuid.uuid4()),
                sourceNode=modules[0].id,
                sourceSocket="SOCKET",
                targetNode=modules[1].id,
                targetSocket="SOCKET",
            ),
            Connection(
                id=str(uuid.uuid4()),
                sourceNode=modules[1].id,
                sourceSocket="SOCKET",
                targetNode=modules[2].id,
                targetSocket="SOCKET",
            ),
        ],
    )
