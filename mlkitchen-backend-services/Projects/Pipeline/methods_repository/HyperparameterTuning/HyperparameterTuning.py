""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: HyperparameterTuning.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: ThList of Hyperparamter algorihtms
-----------------------------------------------------------------------------
"""

import logging
from methods_repository.config_models import ProgrammingLanguages

_logger = logging.getLogger(__name__)


INDICES_OF_DATA_INPUT = [0, 1, 2]
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "GridSearchCV": {
            "import": "sklearn.model_selection",
            "name": "GridSearchCV",
        },
        "RandomizedSearchCV": {
            "import": "sklearn.model_selection",
            "name": "RandomizedSearchCV",
        },
    }
}
