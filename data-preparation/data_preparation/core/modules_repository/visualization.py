""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: visualization.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 06/2024
description: The module for generating plots of a table
-----------------------------------------------------------------------------
"""

import logging
from numpy import reshape
import matplotlib.pyplot as plt
import seaborn as sns
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes


__all__ = ["ScatterPlot", "BarPlot", "HistogramPlot", "LinePlot", "JointPlot"]
_logger = logging.getLogger(__name__)


class ScatterPlot(Node):
    """
    Generate scatter plot(s) from the input data columns.
    """
    NAME = "scatter-plot"
    DESCRIPTION = """Generates scatter plot(s) from the input data columns. \
        based on the inputs from the user, it could generate one or \
        multiple scatter plots."""
    OUT_SOCKETS = []
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be used for visualization",
            "required": True,
        },
    ]
    PARAMETERS = {
        "x_columns": {
            "id": "x_columns",
            "name": "x_columns",
            "description": """The columns to be used for the X axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "y_columns": {
            "id": "y_columns",
            "name": "y_columns",
            "description": """The columns to be used for the Y axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "marker": {
            "id": "marker",
            "name": "marker",
            "description": "The shape of the marker, if not given circle is used by default.",
            "type": "string",
            "required": False,
            "value": 'o',
            "multipleValues": False,
            "allowedValues": [
                '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', 
                '*', 'h', 'H', 'D', 'd', 'P', 'X', '+'
            ]
        },
        "marker_color": {
            "id": "marker_color",
            "name": "marker_color",
            "description": """The color of the markers, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the markers, can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of marker_color and color_from are given, the value
                of 'color_from is used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_x": {
            "id": "size_x",
            "name": "size_x",
            "description": """The size of subplots in x direction (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_y": {
            "id": "size_y",
            "name": "size_y",
            "description": """The size of subplots in y direction (default: 4).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font scale in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_map": {
            "id": "color_map",
            "name": "color_map",
            "description": """The colormap to show the hue from the 'color_from' parameter, if it is a numerical column (default: inferno).""",
            "type": "string",
            "required": False,
            "value": 'inferno',
            "multipleValues": False,
            "allowedValues": {'viridis', 'plasma', 'inferno', 'magma',
                              'cividis', 'Greys', 'Purples', 'Blues',
                              'Greens', 'Oranges', 'Reds', 'GnBu',
                              'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                              'binary', 'gist_gray', 'gray', 'bone', 'PiYG',
                              'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'coolwarm',
                              'bwr', 'seismic', 'twilight', 'CMRmap', 'gist_earth',
                              'terrain'}
        }
    }

    def __init__(self,
                 module_id: str = "",
                 label: str = None,
                 inputs: list[Socket] = None,
                 config: dict[str, ModuleConfigParameter] = None,
                 valid_results: bool = False,
                 position: dict = None,
                 parent_project: str = None,
                 result_repo: ResultsRepository = FileResultsRepository(),
                ):
        super().__init__(
                 module_id=module_id,
                 label=label,
                 inputs=inputs,
                 config=config,
                 valid_results=valid_results,
                 position=position,
                 parent_project=parent_project,
                 result_repo=result_repo,
                 )
    
    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        """
        The module doesn't have any output.
        """
        return {}

    def _get_all_columns(self, data_type: str | list[str] = None):
        """
        returns all columns of the data with specified data_type, based on the input metadata.
        The default value for data_type is ['numerical', 'categorical'],
            for all numerical and categorical columns.
        """
        if data_type is None:
            data_type = {'numerical', 'categorical'}
        if isinstance(data_type, str):
            data_type = {data_type}
        else:
            data_type = set(data_type)
        if self.inputs and self.inputs[0].name:
            input_metadata = self.get_input_metadata()[self.inputs[0].name]
            all_columns = [feature["name"] for feature in input_metadata["features"] 
                           if feature["type"] in data_type]
        else:
            raise TypeError("Please check that the inputs are connected and the results are ready!")
        return all_columns

    def _get_remaining_cols(self, excluded_columnns):
        if excluded_columnns:
            return [col for col in self._get_all_columns() if col not in excluded_columnns]
        
        return self._get_all_columns()
    
    def _get_x_y_cols(self):

        list_of_cols = []
        if 'x_columns' in self.parameters:
            if x_columns := self.parameters["x_columns"].value:
                list_of_cols.extend(x_columns)
        else:
            x_columns = None
        if 'y_columns' in self.parameters:
            if y_columns := self.parameters["y_columns"].value:
                list_of_cols.extend(y_columns)
        else:
            y_columns = None
        if 'color_from' in self.parameters:
            if color_from := self.parameters['color_from'].value:
                list_of_cols.append(color_from)
        else:
            color_from = None

        rest_of_cols = self._get_remaining_cols(list_of_cols)
        
        if not x_columns:
            x_columns = rest_of_cols
        
        if not y_columns:
            y_columns = rest_of_cols
        
        return x_columns, y_columns
    
    def _initialize_figure(self, num_x, num_y, fig=None):

        size_x = self.parameters["size_x"].value or 8
        size_y = self.parameters["size_y"].value or 4
        font_scale = self.parameters["font_scale"].value or 1.0
        if isinstance(font_scale, str):
            font_scale = float(font_scale)

        sns.set_theme(font_scale=font_scale)

        if isinstance(size_x, str):
            size_x = int(size_x)
        if isinstance(size_y, str):
            size_y = int(size_y)
        if fig is None: 
            fig, _ = plt.subplots(num_x, num_y, frameon=False, figsize=(num_y*size_x, num_x*size_y))
        
        axes = fig.get_axes()
        axes = reshape(axes, (num_x, num_y))
        
        return fig, axes


    def run_for_page(self, page, **kwargs):
        """
        Implement the scatter plotting for an input chunk of data.
        """

        marker = self.parameters["marker"].value or 'round'
        marker_color = self.parameters["marker_color"].value or 'blue'
        color_from = self.parameters["color_from"].value
        
        x_columns, y_columns = self._get_x_y_cols()

        fig, axes = self._initialize_figure(num_x=len(x_columns),
                                            num_y=len(y_columns),
                                            fig=kwargs.get("figure", None))

        categorical_columns = self._get_all_columns(data_type=["categorical"])
        for j, y in enumerate(y_columns):
            for i, x in enumerate(x_columns):
                if x == y:
                    continue

                if color_from and color_from not in categorical_columns:
                    cmap_name = self.parameters["color_map"].value or "inferno"
                    norm = plt.Normalize(page[color_from].min(), page[color_from].max())
                    sns.scatterplot(x=x, y=y, data=page, ax=axes[i][j], marker=marker,
                                color=marker_color, hue=color_from,
                                palette=cmap_name,
                                legend=False,
                                hue_norm=norm)
                    sm = plt.cm.ScalarMappable(cmap=cmap_name, norm=norm)
                    sm.set_array([])
                    axes[i][j].figure.colorbar(sm, ax=axes[i][j])
                else:
                    sns.scatterplot(x=x, y=y, data=page, ax=axes[i][j], marker=marker,
                                    color=marker_color, hue=color_from,
                                    legend=True)
        return fig

    def write_output(self, result: plt.axes, append=False) -> bool:
        """
        writes the resulting plot to the output file.

        :param: result (axes): The result of the module.
        :returns: True if the result is written successfully and False otherwise.
        """
        if result is None:
            return False
        try:
            self._results_repo.add(project_name=self.parent_project,
                                   module_id=self.id,
                                   results=result,
                                   data_type=ResultTypes.IMAGE,
                                   append=append)
        except IOError as e:
            self.error_message = f"Failed to write the result of module {self.NAME} to the results repository: {e}"
            _logger.error(self.error_message)
            return False
        return True
    
    def run(self) -> None:
        """
          Implement the logic to run the module based on the input configuration.
        """
        super().run()

        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        try:
            # Read the input file
            fig = None
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                fig = self.run_for_page(chunk, figure=fig)
            
            if not self.write_output(fig):
                raise IOError(f"Failed to write output for module {self.NAME}")                
            self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to run module: %s", e)
            raise Exception(f"Failed to run module ({self.NAME}): {e}") from e

    def _get_in_keys(self, input_metadata=None) -> list[str]:
        """
        Get the input keys or indices of the table, based on user's input.
        """
        if (keys := self.parameters["keys"].value) is None:
            if input_metadata is None:
                input_metadata=self.get_input_metadata()
            if self.inputs and self.inputs[0].name:
                input_metadata = input_metadata[self.inputs[0].name]
            keys = input_metadata["keys"]
        if isinstance(keys, str):
            keys = [keys]
        return keys
    
    def get_output(self, **kwargs):
        """
        If the outout is valid, it will return the saved plot.
        """
        if self.valid_results:
            return self._results_repo.get(project_name=self.parent_project, module_id=self.id,
                                   data_type=ResultTypes.IMAGE)
        raise ValueError("The output is not valid, please make sure to run the module, first!")
    
    def is_visualization_module(self):
        return True


class BarPlot(ScatterPlot):
    """
    Generate bar plot(s) from the input data columns.
    """
    NAME = "bar-plot"
    DESCRIPTION = """Generates bar plot(s) from the input data columns. \
        based on the inputs from the user, it could generate one or \
        multiple bar plots."""
    PARAMETERS = {
        "x_columns": {
            "id": "x_columns",
            "name": "x_columns",
            "description": """The columns to be used for the X axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "y_columns": {
            "id": "y_columns",
            "name": "y_columns",
            "description": """The columns to be used for the Y axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "estimator": {
            "id": "estimator",
            "name": "estimator",
            "description": """The estimator for plotting the bars, the default value is mean.""",
            "type": "string",
            "required": False,
            "value": 'mean',
            "multipleValues": False
        },
        "errorbar": {
            "id": "error_bar",
            "name": "error_bar",
            "description": """The function for computing the error bar. \
                possible values are 'sd' for standards deviation, 'ci' for confidence interval, \
                'pi' for percentile interval, and 'se' for standard error (sd devided by the root of sample size), \
                or 'None' to not show error bars.
                The default value is sd (standard deviation).""",
            "type": "string",
            "required": False,
            "value": 'sd',
            "allowedValues": {"sd", "ci", "pi", "se"},
            "multipleValues": False
        },
        "errorbar_parameter": {
            "id": "error_bar_parameter",
            "name": "error_bar_parameter",
            "description": """The parameter of the error_bar function. \
                For 'sd' and 'se' it is a scale parameter (default: 1), \
                for 'ci' it is a percentile of a confidence interval (default: 95), and \
                for 'pi' the range of percentile (default: 95).""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "bar_color": {
            "id": "bar_color",
            "name": "bar_color",
            "description": """The color of the bars, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string", 
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the bars, can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of bar_color and color_from are given, the value
                of 'color_from is used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_x": {
            "id": "size_x",
            "name": "size_x",
            "description": """The size of subplots in x direction (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_y": {
            "id": "size_y",
            "name": "size_y",
            "description": """The size of subplots in y direction (default: 4).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font size in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        }
    }

    def run_for_page(self, page, **kwargs):
        """
        Implement bar plot for an input chunk of data.
        """
        bar_color = self.parameters["bar_color"].value or 'blue'
        color_from = self.parameters["color_from"].value

        if (errorbar := self.parameters['errorbar'].value or 'sd') == 'None':
            errorbar = None
        if (errorbar_parameter := self.parameters["errorbar_parameter"].value) is None:
            if errorbar in {'sd', 'se'}:
                errorbar_parameter = 1
            elif errorbar in {'ci', 'pi'}:
                errorbar_parameter = 95
        
        x_columns, y_columns = self._get_x_y_cols()

        if fig := kwargs.get("figure", None):
            _logger.Warning("The data is too big, only an approximated result is shown.")
            return fig

        fig, axes = self._initialize_figure(num_x=len(x_columns),
                                            num_y=len(y_columns),
                                            fig=fig)

        for j, y in enumerate(y_columns):
            for i, x in enumerate(x_columns):
                if x == y:
                    continue
                sns.barplot(x=x, y=y, data=page, ax=axes[i][j],
                            color=bar_color, hue=color_from,
                            errorbar=(errorbar, errorbar_parameter) if errorbar else None)
        
        return fig


class HistogramPlot(ScatterPlot):
    """
    Generate histogram plot(s) from the input data columns.
    """
    NAME = "histogram-plot"
    DESCRIPTION = """Generates histogram plot(s) from the input data columns. \
        based on the inputs from the user, it could generate one or \
        multiple histogram plots."""
    PARAMETERS = {
        "x_columns": {
            "id": "x_columns",
            "name": "x_columns",
            "description": """The columns to be used for the X axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "number_of_bins": {
            "id": "number_of_bins",
            "name": "number_of_bins",
            "description": """The number of bins of the histogram, if not given, \
                the 'bins_estimator' will be used to compute the bins of histogram.""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "bins_estimator": {
            "id": "bins_estimator",
            "name": "bins_estimator",
            "description": """An estimator for calculating the bins of the histogram (default: 'auto').
                If 'number_of_bins' is set, the value of this parameter is ignored.""",
            "type": "string",
            "required": False,
            "value": 'auto',
            "allowedValues": {'auto', 'freedman diaconis', 'scott', 'rice', 'sturges', 'doane', 'sqrt'},
            "multipleValues": False
        },
        "plot_kde": {
            "id": "plot_kde",
            "name": "plot_kde",
            "description": """Whether plot the kde or not (default: False).""",
            "type": "boolean",
            "required": False,
            "value": False,
            "multipleValues": False
        },
        "bar_color": {
            "id": "bar_color",
            "name": "bar_color",
            "description": """The color of the bars, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the bars, can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of bar_color and color_from are given, the value
                of 'color_from is used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_x": {
            "id": "size_x",
            "name": "size_x",
            "description": """The size of subplots in x direction (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_y": {
            "id": "size_y",
            "name": "size_y",
            "description": """The size of subplots in y direction (default: 4).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font size in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        }
    }

    def run_for_page(self, page, **kwargs):
        """
        Implement plotting histogram for input chunk of data.
        """
        bar_color = self.parameters["bar_color"].value or 'blue'
        color_from = self.parameters["color_from"].value
        plot_kde = self.parameters["plot_kde"].value or False

        if (number_of_bins := self.parameters['number_of_bins'].value) is None:
            bins_estimator = self.parameters['number_of_bins'].value or 'auto'
            if bins_estimator == 'freedman diaconis':
                bins_estimator = 'fd'
            bins = bins_estimator
        else:
            bins = number_of_bins

        x_columns, _ = self._get_x_y_cols()

        if fig := kwargs.get("figure", None):
            _logger.Warning("The data is too big, only an approximated result is shown.")
            return fig

        fig, axes = self._initialize_figure(num_x=len(x_columns),
                                            num_y=1,
                                            fig=fig)

        for i, x in enumerate(x_columns):
            sns.histplot(x=x, data=page, ax=axes[i][0],
                        color=bar_color, hue=color_from,
                        bins=bins,
                        kde=plot_kde,
                        multiple='dodge')
        return fig


class LinePlot(ScatterPlot):
    """
    Generate line plot(s) from the input data columns.
    """
    NAME = "line-plot"
    DESCRIPTION = """Generates line plot(s) from the input data columns. \
        based on the inputs from the user, it could generate one or \
        multiple line plots."""
    PARAMETERS = {
        "x_columns": {
            "id": "x_columns",
            "name": "x_columns",
            "description": """The columns to be used for the X axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "y_columns": {
            "id": "y_columns",
            "name": "y_columns",
            "description": """The columns to be used for the Y axis, if not given \
                all combination of columns are used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "sort": {
            "id": "sort",
            "name": "sort",
            "description": "Wether sort the data of x and y axes or not (default: True).",
            "type": "boolean",
            "required": False,
            "value": True,
            "multipleValues": False,
        },
        "line_color": {
            "id": "line_color",
            "name": "line_color",
            "description": """The color of the lines, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the lines, can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of marker_color and color_from are given, the value
                of 'color_from is used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_x": {
            "id": "size_x",
            "name": "size_x",
            "description": """The size of subplots in x direction (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size_y": {
            "id": "size_y",
            "name": "size_y",
            "description": """The size of subplots in y direction (default: 4).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font scale in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        }
    }

    def run_for_page(self, page, **kwargs):
        """
        Implement the line plot for an input chunk of data.
        """
        if (sort := self.parameters["sort"].value) is None:
            sort = True
        line_color = self.parameters["line_color"].value or 'blue'
        color_from = self.parameters["color_from"].value
        
        x_columns, y_columns = self._get_x_y_cols()

        fig, axes = self._initialize_figure(num_x=len(x_columns),
                                            num_y=len(y_columns),
                                            fig=kwargs.get("figure", None))

        for j, y in enumerate(y_columns):
            for i, x in enumerate(x_columns):
                if x == y:
                    continue
                sns.lineplot(x=x, y=y, data=page, ax=axes[i][j], sort=sort,
                            color=line_color, hue=color_from, legend=True)
        return fig


class JointPlot(ScatterPlot):
    """
    Generate joint plot(s) from the input data columns.
    """
    NAME = "joint-plot"
    DESCRIPTION = """Generates joint plot(s) from the input data columns."""
    PARAMETERS = {
        "x_column": {
            "id": "x_column",
            "name": "x_column",
            "description": """The column to be used for the X axis. \
                The column should contain either a numeric or datetime values.""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "y_column": {
            "id": "y_column",
            "name": "y_column",
            "description": """The column to be used for the Y axis. \
                The column should contain either a numeric or datetime values.""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": False
        },
        "kind": {
            "id": "kind",
            "name": "kind",
            "description": "The kind of joint plot (default: scatter).",
            "type": "string",
            "required": False,
            "value": 'scatter',
            "allowedValues": {'scatter', 'kde', 'hist', 'hex', 'reg', 'resid'},
            "multipleValues": False,
        },
        "color": {
            "id": "color",
            "name": "color",
            "description": """The color of the plot, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the plot can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of marker_color and color_from are given, the value
                of 'color_from is used. \
                This feature is not supported with the plot 'kind's of 'hex', 'reg', and 'resid'.
                If 'kind' is one of above values, the value of 'color_from' will be ignored.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size": {
            "id": "size",
            "name": "size",
            "description": """The size of the plot, it will be a square (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font scale in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        }
    }

    def run_for_page(self, page, **kwargs):
        """
        Implement the line plot for an input chunk of data.
        """

        if fig := kwargs.get("figure", None):
            _logger.Warning("The data is too big, only an approximated result is shown.")
            return fig

        x_column = self.parameters["x_column"].value
        y_column = self.parameters["y_column"].value
        kind = self.parameters["kind"].value or 'scatter'
        color = self.parameters["color"].value or 'blue'
        if kind not in {'hex', 'reg', 'resid'}:
            color_from = self.parameters["color_from"].value
        else:
            color_from = None
        size = self.parameters["size"].value or 8
        font_scale = self.parameters["font_scale"].value or 1.0
        if isinstance(font_scale, str):
            font_scale = float(font_scale)

        sns.set_theme(font_scale=font_scale)
        fig = sns.jointplot(x=x_column, y=y_column, data=page, kind=kind,
                        color=color, hue=color_from, height=size)
        return fig


class PairPlot(ScatterPlot):
    """
    Generate pair plot(s) from the input data columns.
    """
    NAME = "pair-plot"
    DESCRIPTION = """Generates pair plot(s) from the input data columns."""
    PARAMETERS = {
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": """The columns to be used for the plot. \
                If not given, all columns are used for the plotting""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "kind": {
            "id": "kind",
            "name": "kind",
            "description": "The kind of plots to make (default: scatter).",
            "type": "string",
            "required": False,
            "value": 'scatter',
            "allowedValues": {'scatter', 'kde', 'hist', 'reg'},
            "multipleValues": False,
        },
        "diag_kind": {
            "id": "diag_kind",
            "name": "diag_kind",
            "description": """The kind of diagonal plots, if 'None' is selected, the value is the same as 'kind'.
              (default: 'auto').""",
            "type": "string",
            "required": False,
            "value": 'auto',
            "allowedValues": {'auto', 'hist', 'kde', 'None'},
            "multipleValues": False,
        },
        "color_from": {
            "id": "color_from",
            "name": "color_from",
            "description": """The color of the plot can be different, based on \
                another column. This could be a categorical or a numerical column.
                If both of marker_color and color_from are given, the value
                of 'color_from is used. \
                This feature is not supported with the plot 'kind's of 'hex', 'reg', and 'resid'.
                If 'kind' is one of above values, the value of 'color_from' will be ignored.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "marker": {
            "id": "marker",
            "name": "marker",
            "description": "The shape of the marker, if not given circle is used by default.",
            "type": "string",
            "required": False,
            "value": 'o',
            "multipleValues": False,
            "allowedValues": [
                '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', 
                '*', 'h', 'H', 'D', 'd', 'P', 'X', '+'
            ]
        },
        "color": {
            "id": "color",
            "name": "color",
            "description": """The color of the plot, default value is blue. \
                input could be a hex number (example: '#ff7f0e') or one of 'red',
                'green', 'blue', 'black', 'yellow'""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "size": {
            "id": "size",
            "name": "size",
            "description": """The size of the plot, it will be a square (default: 8).""",
            "type": "integer",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "font_scale": {
            "id": "font_scale",
            "name": "font_scale",
            "description": """The font scale in the plots (default: 1).""",
            "type": "float",
            "required": False,
            "value": None,
            "multipleValues": False
        }
    }

    def run_for_page(self, page, **kwargs):
        """
        Implement the line plot for an input chunk of data.
        """

        if fig := kwargs.get("figure", None):
            _logger.Warning("The data is too big, only an approximated result is shown.")
            return fig

        kind = self.parameters["kind"].value or 'scatter'
        color_from = self.parameters["color_from"].value
        if kind in {'kde', 'reg'} or color_from is not None:
            data_type = ['numerical']
        else:
            data_type = None
        columns = self.parameters["columns"].value or self._get_all_columns(data_type=data_type)
        if (diag_kind := self.parameters["diag_kind"].value or 'auto') == 'None':
            diag_kind = None
        color = self.parameters["color"].value or 'blue'
        marker = self.parameters["marker"].value or 'o'
        size = self.parameters["size"].value or 8
        font_scale = self.parameters["font_scale"].value or 1.0
        if isinstance(font_scale, str):
            font_scale = float(font_scale)

        sns.set_theme(font_scale=font_scale)
        if kind == 'scatter':
            plot_kws={"marker": marker,
                      "color": color,
                    }
        elif kind == 'kde':
            plot_kws={"marker": marker,
                      "color": None if color_from else color,
                      "multiple": 'stack'}
        elif kind == 'hist':
            plot_kws={"color": None if color_from else color,
                      "multiple": 'dodge',
                      "shrink": .8}
        else: # it's 'reg'
            plot_kws={"marker": marker,
                      "color": None if color_from else color,
                    }
        
        if diag_kind == 'hist':
            diag_kws = {"color": None if color_from else color,
                        "multiple": 'dodge',
                        "shrink": .8}
        elif diag_kind =='kde' or (diag_kind == 'auto' and color_from):
            diag_kws = {"color": None if color_from else color,
                        "multiple": 'stack'}
        else:
            diag_kws = {"color": None if color_from else color,
                        "shrink": .8}
        fig = sns.pairplot(data=page, vars=columns, kind=kind,
                           diag_kind=diag_kind,
                           plot_kws=plot_kws,
                           diag_kws=diag_kws,
                           hue=color_from,
                           height=size)
        return fig