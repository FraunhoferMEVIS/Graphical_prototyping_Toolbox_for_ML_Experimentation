""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Distributions.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: List of statisitcal functions.
-----------------------------------------------------------------------------
"""

from methods_repository.config_models import ProgrammingLanguages


List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "uniform": {
            "import": "scipy.stats",
            "name": "uniform",
            "flags": []
        },
        "loguniform": {
            "import": "scipy.stats",
            "name": "loguniform",
            "flags": []
        },
        "randint": {
            "import": "scipy.stats",
            "name": "randint",
            "flags": []
        }
    }
}
