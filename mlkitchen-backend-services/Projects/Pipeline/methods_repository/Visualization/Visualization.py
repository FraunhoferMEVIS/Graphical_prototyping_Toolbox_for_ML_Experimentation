""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Visualization.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: List of algorithms for visualization module.
-----------------------------------------------------------------------------
"""

import logging
from methods_repository.config_models import ProgrammingLanguages, \
                                             VisualizationTypes

_logger = logging.getLogger(__name__)


INDICES_OF_DATA_INPUT = [0]
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "relplot": {
            "import": "seaborn",
            "name": "relplot",
            "flags": [VisualizationTypes.plot],
        },
        "scatterplot": {
            "import": "seaborn",
            "name": "scatterplot",
            "flags": [VisualizationTypes.plot],
        },
        "lineplot": {
            "import": "seaborn",
            "name": "lineplot",
            "flags": [VisualizationTypes.plot],
        },
        "displot": {
            "import": "seaborn",
            "name": "displot",
            "flags": [VisualizationTypes.plot],
        },
        "histplot": {
            "import": "seaborn",
            "name": "histplot",
            "flags": [VisualizationTypes.plot],
        },
        "kdeplot": {
            "import": "seaborn",
            "name": "kdeplot",
            "flags": [VisualizationTypes.plot],
        },
        "ecdfplot": {
            "import": "seaborn",
            "name": "ecdfplot",
            "flags": [VisualizationTypes.plot],
        },
        "rugplot": {
            "import": "seaborn",
            "name": "rugplot",
            "flags": [VisualizationTypes.plot],
        },
        "catplot": {
            "import": "seaborn",
            "name": "catplot",
            "flags": [VisualizationTypes.plot],
        },
        "stripplot": {
            "import": "seaborn",
            "name": "stripplot",
            "flags": [VisualizationTypes.plot],
        },
        "swarmplot": {
            "import": "seaborn",
            "name": "swarmplot",
            "flags": [VisualizationTypes.plot],
        },
        "violinplot": {
            "import": "seaborn",
            "name": "violinplot",
            "flags": [VisualizationTypes.plot],
        },
        "boxplot": {
            "import": "seaborn",
            "name": "boxplot",
            "flags": [VisualizationTypes.plot],
        },
        "boxenplot": {
            "import": "seaborn",
            "name": "boxenplot",
            "flags": [VisualizationTypes.plot],
        },
        "pointplot": {
            "import": "seaborn",
            "name": "pointplot",
            "flags": [VisualizationTypes.plot],
        },
        "barplot": {
            "import": "seaborn",
            "name": "barplot",
            "flags": [VisualizationTypes.plot],
        },
        "countplot": {
            "import": "seaborn",
            "name": "countplot",
            "flags": [VisualizationTypes.plot],
        },
        "lmplot": {
            "import": "seaborn",
            "name": "lmplot",
            "flags": [VisualizationTypes.plot],
        },
        "regplot": {
            "import": "seaborn",
            "name": "regplot",
            "flags": [VisualizationTypes.plot],
        },
        "residplot": {
            "import": "seaborn",
            "name": "residplot",
            "flags": [VisualizationTypes.plot],
        },
        "heatmap": {
            "import": "seaborn",
            "name": "heatmap",
            "flags": [VisualizationTypes.plot],
        },
        "clustermap": {
            "import": "seaborn",
            "name": "clustermap",
            "flags": [VisualizationTypes.plot],
        },
        "pairplot": {
            "import": "seaborn",
            "name": "pairplot",
            "flags": [VisualizationTypes.plot],
        },
        "jointplot": {
            "import": "seaborn",
            "name": "jointplot",
            "flags": [VisualizationTypes.plot],
        },
        "FacetGrid": {
            "import": "seaborn",
            "name": "FacetGrid",
            "flags": [VisualizationTypes.grid],
        },
        "PairGrid": {
            "import": "seaborn",
            "name": "PairGrid",
            "flags": [VisualizationTypes.grid],
        },
        "JointGrid": {
            "import": "seaborn",
            "name": "JointGrid",
            "flags": [VisualizationTypes.grid],
        },
    }
}




def get_parameter_type_and_options(algorithm_name: str, parameter: str):
    """
    Gets the type and options of the parameter for the given algorithm.
    """
    language = ProgrammingLanguages.Python

    param_type, param_options = None, None

    if algorithm_name in List_of_Algorithms[language]:
        algorithm_info = List_of_Algorithms[language][algorithm_name]
        if algorithm_info["import"] == "seaborn":
            if parameter in {"x", "y"}:
                param_type = "list[str]"
            elif parameter in {"hue"}:
                param_type = "str"
            elif parameter in {"palette"}:
                param_type = "str"
                param_options = [
                    "deep", "muted", "pastel", "bright", "dark", "colorblind",
                    "tab10", "tab20", "tab20b", "tab20c", "vlag", "rocket",
                    "mako", "flare", "husl"
                ]
    else:
        return param_type, param_options

    return param_type, param_options
