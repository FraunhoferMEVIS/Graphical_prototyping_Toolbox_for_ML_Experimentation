""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_visualization_modules.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The pytest file for testing the test_visualization module
-----------------------------------------------------------------------------
"""
import os
import pytest
from data_preparation.core.modules_repository.visualization import (
                ScatterPlot, BarPlot, HistogramPlot, LinePlot,
                JointPlot, PairPlot,
            )
from data_preparation.models.network import Socket, ModuleConfigParameter


@pytest.mark.parametrize("combination", [(None, None, None, None, None, None, None, None, None), # all default
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], 's', '#f3459a', "code", None, None, 1.2, "gist_earth"),
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], '8', 'red', "test", None, 5, None, "seismic"),
                                         (None, ['systolic_blood_pressure', 'diastolic_blood_pressure'], 'D', 'black', None, None, None, '1.1', "gist_earth"),
                                         (['code'], None, 'h', None, 'test', 24, None, 1.5, None),
                                        ])
def test_run_scatterplot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_columns": combination[0],
        "y_columns": combination[1],
        "marker": combination[2],
        "marker_color": combination[3],
        "color_from": combination[4],
        "size_x": combination[5],
        "size_y": combination[6],
        "font_scale": combination[7],
        "color_map": combination[8]
    }
    module = ScatterPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_columns": ModuleConfigParameter(
                id="x_columns",
                type="string",
                value=config["x_columns"],
                name="x_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "y_columns": ModuleConfigParameter(
                id="y_columns",
                type="string",
                value=config["y_columns"],
                name="y_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "marker": ModuleConfigParameter(
                id="marker",
                type="string",
                value=config["marker"],
                name="marker",
                description="...",
                required=False,
                multipleValues=False,
                allowedValues=[
                    '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', 
                    '*', 'h', 'H', 'D', 'd', 'P', 'X'
                ]
            ),
            "marker_color": ModuleConfigParameter(
                id="marker_color",
                type="string",
                value=config["marker_color"],
                name="marker_color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_x": ModuleConfigParameter(
                id="size_x",
                type="integer",
                value=config["size_x"],
                name="size_x",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_y": ModuleConfigParameter(
                id="size_y",
                type="integer",
                value=config["size_y"],
                name="size_y",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_map": ModuleConfigParameter(
                id="color_map",
                type="string",
                value=config["color_map"],
                name="color_map",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    output_file = os.path.join(result_repo._repo_path, existing_project,
                               "maratus", "results", f"{module.id}.png")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1500
    module.invalidate_output()


@pytest.mark.parametrize("combination", [(None, None, None, None, None, None, None, None), # all default
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], '#f3459a', "code", '15', None, 1.5),
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], 'red', "test", None, None, '1'),
                                         (None, ['systolic_blood_pressure', 'diastolic_blood_pressure'], 'black', None, None, None, 1.2),
                                         (['code'], None, None, 'test_unit', 12, 8, '2'),
                                        ])
def test_run_bar_plot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_columns": combination[0],
        "y_columns": combination[1],
        "bar_color": combination[2],
        "color_from": combination[3],
        "size_x": combination[4],
        "size_y": combination[5],
        "font_scale": combination[6]
    }
    module = BarPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_columns": ModuleConfigParameter(
                id="x_columns",
                type="string",
                value=config["x_columns"],
                name="x_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "y_columns": ModuleConfigParameter(
                id="y_columns",
                type="string",
                value=config["y_columns"],
                name="y_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "bar_color": ModuleConfigParameter(
                id="bar_color",
                type="string",
                value=config["bar_color"],
                name="bar_color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_x": ModuleConfigParameter(
                id="size_x",
                type="integer",
                value=config["size_x"],
                name="int",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_y": ModuleConfigParameter(
                id="size_y",
                type="integer",
                value=config["size_y"],
                name="size_y",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    assert os.path.exists(os.path.join(result_repo._repo_path, existing_project,
                                       "maratus", "results", f"{module.id}.png"))
    module.invalidate_output()


def test_run_bar_plot_parameter_by_id(existing_project, result_repo, sample_input_table2):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_columns": ['systolic_blood_pressure'],
        "y_columns": ['diastolic_blood_pressure'],
        "error_bar": "sd",
        "bar_color":'#f3459a',
        "color_from": "code",
        "size_x": '15',
        "size_y": None,
        "font_scale": 1.5
    }
    module = BarPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_columns": ModuleConfigParameter(
                id="x_columns",
                type="string",
                value=config["x_columns"],
                name="x_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "y_columns": ModuleConfigParameter(
                id="y_columns",
                type="string",
                value=config["y_columns"],
                name="y_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            # The name was actually errorbar in the parameters, but the id is "error_bar"
            "error_bar": ModuleConfigParameter(
                id="error_bar",
                type="string",
                value=config["error_bar"],
                name="error_bar",
                description="...",
                required=False,
                multipleValues=True
            ),
            "bar_color": ModuleConfigParameter(
                id="bar_color",
                type="string",
                value=config["bar_color"],
                name="bar_color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_x": ModuleConfigParameter(
                id="size_x",
                type="integer",
                value=config["size_x"],
                name="int",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_y": ModuleConfigParameter(
                id="size_y",
                type="integer",
                value=config["size_y"],
                name="size_y",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    assert os.path.exists(os.path.join(result_repo._repo_path, existing_project,
                                       "maratus", "results", f"{module.id}.png"))
    module.invalidate_output()


@pytest.mark.parametrize("combination", [(None, None, None, None, None, None, None, None, None), # all default
                                         (['systolic_blood_pressure'], 10, None, True,'#f3459a', "code", '15', None, 1.5),
                                         (['diastolic_blood_pressure'], None, 'freedman diaconis', False, 'red', "test", None, None, '1'),
                                         (['systolic_blood_pressure', 'diastolic_blood_pressure'], 20, 'auto', True, 'black', None, None, None, 1.2),
                                         (['code'], None, 'scott', True, None, 'test_unit', 12, 8, '2'),
                                         (None, None, 'rice', False, None, 'test_unit', None, None, '1'),
                                         (None, None, 'sturges', True, None, 'test_unit', None, None, '1'),
                                         (None, None, 'doane', False, None, 'test_unit', None, None, '1'),
                                         (None, None, 'sqrt', True, None, 'test_unit', None, None, '1'),
                                        ])
def test_run_hist_plot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_columns": combination[0],
        "number_of_bins": combination[1],
        "bins_estimator": combination[2],
        "plot_kde": combination[3],
        "bar_color": combination[4],
        "color_from": combination[5],
        "size_x": combination[6],
        "size_y": combination[7],
        "font_scale": combination[8]
    }
    module = HistogramPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_columns": ModuleConfigParameter(
                id="x_columns",
                type="string",
                value=config["x_columns"],
                name="x_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "number_of_bins": ModuleConfigParameter(
                id="number_of_bins",
                type="integer",
                value=config["number_of_bins"],
                name="number_of_bins",
                description="...",
                required=False,
                multipleValues=False
            ),
            "bins_estimator": ModuleConfigParameter(
                id="bins_estimator",
                type="string",
                value=config["bins_estimator"],
                name="bins_estimator",
                description="...",
                required=False,
                multipleValues=False
            ),
            "bar_color": ModuleConfigParameter(
                id="bar_color",
                type="string",
                value=config["bar_color"],
                name="bar_color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "plot_kde": ModuleConfigParameter(
                id="plot_kde",
                type="boolean",
                value=config["plot_kde"],
                name="plot_kde",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_x": ModuleConfigParameter(
                id="size_x",
                type="integer",
                value=config["size_x"],
                name="int",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_y": ModuleConfigParameter(
                id="size_y",
                type="integer",
                value=config["size_y"],
                name="size_y",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    output_file = os.path.join(result_repo._repo_path, existing_project,
                               "maratus", "results", f"{module.id}.png")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1500
    module.invalidate_output()


@pytest.mark.parametrize("combination", [(None, None, None, None, None, None, None, None), # all default
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], True, '#f3459a', "code", None, None, 1.2),
                                         (['systolic_blood_pressure'], ['diastolic_blood_pressure'], False, 'red', "code", None, 5, None),
                                         (None, ['systolic_blood_pressure', 'diastolic_blood_pressure'], False, 'black', None, None, None, '1.1'),
                                         (['systolic_blood_pressure'], None, True, None, 'test_unit', 24, None, 1.5),
                                        ])
def test_run_lineplot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_columns": combination[0],
        "y_columns": combination[1],
        "sort": combination[2],
        "line_color": combination[3],
        "color_from": combination[4],
        "size_x": combination[5],
        "size_y": combination[6],
        "font_scale": combination[7]
    }
    module = LinePlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_columns": ModuleConfigParameter(
                id="x_columns",
                type="string",
                value=config["x_columns"],
                name="x_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "y_columns": ModuleConfigParameter(
                id="y_columns",
                type="string",
                value=config["y_columns"],
                name="y_columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "sort": ModuleConfigParameter(
                id="sort",
                type="boolean",
                value=config["sort"],
                name="sort",
                description="...",
                required=False,
                multipleValues=False,
            ),
            "line_color": ModuleConfigParameter(
                id="line_color",
                type="string",
                value=config["line_color"],
                name="line_color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_x": ModuleConfigParameter(
                id="size_x",
                type="integer",
                value=config["size_x"],
                name="size_x",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size_y": ModuleConfigParameter(
                id="size_y",
                type="integer",
                value=config["size_y"],
                name="size_y",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    output_file = os.path.join(result_repo._repo_path, existing_project,
                               "maratus", "results", f"{module.id}.png")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1500
    module.invalidate_output()


@pytest.mark.parametrize("combination", [('systolic_blood_pressure', 'diastolic_blood_pressure', None, None, None, None, None), # all default
                                         ('systolic_blood_pressure', 'diastolic_blood_pressure', 'scatter', '#f3459a', "code", None, 1.2),
                                         ('systolic_blood_pressure', 'test', 'kde', 'red', "code", 5, None),
                                         ('test', 'diastolic_blood_pressure', 'hist', 'black', None, None, '1.1'),
                                         ('diastolic_blood_pressure', 'systolic_blood_pressure', 'hex', None, 'test_unit', 10, 1.5),
                                         ('systolic_blood_pressure', 'test', 'reg', None, 'test_unit', 10, 1),
                                         ('systolic_blood_pressure', 'diastolic_blood_pressure', 'resid', None, 'test', 12, 1),
                                        ])
def test_run_jointplot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "x_column": combination[0],
        "y_column": combination[1],
        "kind": combination[2],
        "color": combination[3],
        "color_from": combination[4],
        "size": combination[5],
        "font_scale": combination[6]
    }
    module = JointPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "x_column": ModuleConfigParameter(
                id="x_column",
                type="string",
                value=config["x_column"],
                name="x_column",
                description="...",
                required=False,
                multipleValues=False
            ),
            "y_column": ModuleConfigParameter(
                id="y_column",
                type="string",
                value=config["y_column"],
                name="y_column",
                description="...",
                required=False,
                multipleValues=False
            ),
            "kind": ModuleConfigParameter(
                id="kind",
                type="string",
                value=config["kind"],
                name="kind",
                description="...",
                required=False,
                multipleValues=False,
            ),
            "color": ModuleConfigParameter(
                id="color",
                type="string",
                value=config["color"],
                name="color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size": ModuleConfigParameter(
                id="size",
                type="integer",
                value=config["size"],
                name="size",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    output_file = os.path.join(result_repo._repo_path, existing_project,
                               "maratus", "results", f"{module.id}.png")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1500
    module.invalidate_output()


@pytest.mark.parametrize("combination", [(None, None, None, None, None, None, None, None), # all default
                                         (None, 'scatter', 'auto', 'test_unit', '+', '#f3459a', 5, 1.1), # should ignore color
                                         (None, 'kde', 'hist', 'code', None, None, None, None), # kde-hist combo
                                         (['systolic_blood_pressure', 'test'], 'hist', 'kde', None, None, 'red', 5, None),
                                         (None, 'reg', 'None', 'code', 's', 'black', None, '1.1'),
                                         (None, 'reg', 'auto', 'code', 's', 'black', None, '1.1'),
                                         (None, 'reg', 'kde', 'test_unit', None, None, None, None),
                                         (None, 'scatter', 'hist', 'code', None, None, None, 1),
                                         (None, 'scatter', 'None', 'code', None, None, None, 1),
                                        ])
def test_run_pairplot(existing_project, result_repo, sample_input_table2, combination):
    """
    The test for the run method of the Get_Postgres_Table module.
    """
    config = {
        "columns": combination[0],
        "kind": combination[1],
        "diag_kind": combination[2],
        "color_from": combination[3],
        "marker": combination[4],
        "color": combination[5],
        "size": combination[6],
        "font_scale": combination[7]
    }
    module = PairPlot(
        inputs=[
            Socket(name="input1", value=sample_input_table2),
        ],
        config={
            "columns": ModuleConfigParameter(
                id="columns",
                type="string",
                value=config["columns"],
                name="columns",
                description="...",
                required=False,
                multipleValues=True
            ),
            "kind": ModuleConfigParameter(
                id="kind",
                type="string",
                value=config["kind"],
                name="kind",
                description="...",
                required=False,
                multipleValues=False,
            ),
            "diag_kind": ModuleConfigParameter(
                id="diag_kind",
                type="string",
                value=config["diag_kind"],
                name="diag_kind",
                description="...",
                required=False,
                multipleValues=False,
            ),
            "color_from": ModuleConfigParameter(
                id="color_from",
                type="string",
                value=config["color_from"],
                name="color_from",
                description="...",
                required=False,
                multipleValues=False
            ),
            "marker": ModuleConfigParameter(
                id="marker",
                type="string",
                value=config["marker"],
                name="marker",
                description="...",
                required=False,
                multipleValues=False
            ),
            "color": ModuleConfigParameter(
                id="color",
                type="string",
                value=config["color"],
                name="color",
                description="...",
                required=False,
                multipleValues=False
            ),
            "size": ModuleConfigParameter(
                id="size",
                type="integer",
                value=config["size"],
                name="size",
                description="...",
                required=False,
                multipleValues=False
            ),
            "font_scale": ModuleConfigParameter(
                id="font_scale",
                type="float",
                value=config["font_scale"],
                name="font_scale",
                description="...",
                required=False,
                multipleValues=False
            ),
        },
        parent_project=existing_project,
        result_repo=result_repo
    )
    module.run()
    assert module.valid_results
    assert module.error_message == ""
    output_file = os.path.join(result_repo._repo_path, existing_project,
                               "maratus", "results", f"{module.id}.png")
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 1500
    module.invalidate_output()
