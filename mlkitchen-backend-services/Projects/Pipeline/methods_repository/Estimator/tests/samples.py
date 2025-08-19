""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: samples.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: Example inputs for the DataSplitting tests
-----------------------------------------------------------------------------
"""

import os
import pandas as pd

data_set_ts = pd.read_csv(os.path.join("methods_repository",
                                    "Estimator", "tests",
                                    "sample_patients_ts.txt"), sep=" ")