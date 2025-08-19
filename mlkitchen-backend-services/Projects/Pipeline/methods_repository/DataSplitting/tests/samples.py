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


data_set = pd.read_csv(os.path.join("methods_repository",
                                    "DataSplitting", "tests",
                                    "sample_patients.txt"), sep=" ")
data_set.set_index(['subject_id', 'hadm_id', 'period'], inplace=True)




data_set_ts = pd.read_csv(os.path.join("methods_repository",
                                    "DataSplitting", "tests",
                                    "sample_patients_ts.txt"), sep=" ")
