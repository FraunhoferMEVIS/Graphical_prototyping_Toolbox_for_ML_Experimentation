""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_MissingValueHandling.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The tests for HandlingMissingValues' modules
-----------------------------------------------------------------------------
"""

import pytest
from pandas.testing import assert_frame_equal
from methods_repository.abstraction import ModuleFinder

@pytest.mark.parametrize("algorithm", ["Median", "PreviousAndNextValue","MeanGrouped","MedianGrouped", "Median",
                                       "DropColumnsWithMissingRatio",
                                       "DropSubjectWithMissingRatio",
                                       "NormalValue"])
def test_imputation_algorithms(example_train_patient, example_test_patient,
                               example_test_patient_imputed, algorithm):
    if algorithm == "NormalValue":
        obj = ModuleFinder.use_method("HandlingMissingValues",
                                      algorithm, columns=['avg_sbp',
                                                          'avg_heartrate'],
                                      fill_value=90)
    elif algorithm == "MeanGrouped" or algorithm == "MedianGrouped"or algorithm == "DropSubjectWithMissingRatio":
        obj = ModuleFinder.use_method("HandlingMissingValues", algorithm, grouping_ids=['subject_id','hadm_id'],
                                         columns=['avg_sbp', 'avg_heartrate'], )
    elif algorithm == "PreviousAndNextValue":
        obj = ModuleFinder.use_method("HandlingMissingValues", algorithm, grouping_ids=['subject_id','hadm_id'], time_column=['period'], 
                                          columns=['avg_sbp','avg_heartrate'],)
    else:
        obj = ModuleFinder.use_method("HandlingMissingValues", algorithm,
                                      columns=['avg_sbp', 'avg_heartrate'])
    obj.fit(example_train_patient)

    imputed_test = obj.transform(example_test_patient)
    print('by hand \n',example_test_patient_imputed[algorithm])
    print('algorithm \n', imputed_test)
    assert_frame_equal(imputed_test, example_test_patient_imputed[algorithm],
                       check_dtype=False, check_like=True)


# test Multivariate imputation algorithms
@pytest.mark.parametrize("algorithm", ["Iterative_Imputer", "KNNImputer"])
def test_multivariate_imputation_algorithms(example_train_patient,
                                            example_test_patient,
                                            algorithm):
    obj = ModuleFinder.use_method("HandlingMissingValues", algorithm,
                                  columns=['avg_sbp', 'avg_heartrate'])
    obj.fit(example_train_patient)
    obj.transform(example_test_patient)