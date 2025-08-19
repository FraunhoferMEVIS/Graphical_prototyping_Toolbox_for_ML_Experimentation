""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: StatisticalFunctions.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: List of statistical functions.
-----------------------------------------------------------------------------
"""

from methods_repository.config_models import ProgrammingLanguages, TaskTypes


List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "chi2": {
            "import": "sklearn.feature_selection",
            "name": "chi2",
            "flags": [TaskTypes.classification]
        },
        "f_classif": {
            "import": "sklearn.feature_selection",
            "name": "f_classif",
            "flags": [TaskTypes.classification]
        },
        "mutual_info_classif": {
            "import": "sklearn.feature_selection",
            "name": "mutual_info_classif",
            "flags": [TaskTypes.classification]
        },
        "f_regression": {
            "import": "sklearn.feature_selection",
            "name": "f_regression",
            "flags": [TaskTypes.regression]
        },
        "mutual_info_regression": {
            "import": "sklearn.feature_selection",
            "name": "mutual_info_regression",
            "flags": [TaskTypes.regression]
        }
    }
}
