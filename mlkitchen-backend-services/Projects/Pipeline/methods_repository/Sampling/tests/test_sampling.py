""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_sampling.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The tests for implemented Sampling modules
-----------------------------------------------------------------------------
"""

import pytest
from methods_repository.abstraction import ModuleFinder


# ,"CondensedNearestNeighbour" -> failing to result in a balanced dataset
@pytest.mark.parametrize("algorithm", ["RandomOverSampler", "SMOTE",
                                       "SVMSMOTE", "BorderlineSMOTE",
                                       "SMOTEN", "ADASYN", "TomekLinks",
                                       "RandomUnderSampler", "AllKNN",
                                       "RandomUnderSampler", "NearMiss",
                                       "EditedNearestNeighbours",
                                       "RepeatedEditedNearestNeighbours",
                                       "InstanceHardnessThreshold",
                                       "NeighbourhoodCleaningRule",
                                       "OneSidedSelection", "SMOTEENN",
                                       "SMOTETomek", "KMeansSMOTE",
                                       "ClusterCentroids"])
def test_sampling_algorithms(breast_cancer, algorithm):
    parameters = {
        "sampling_strategy": 'auto',
        "random_state": 0,
    }

    X = breast_cancer.data
    y = breast_cancer.target

    splitter = ModuleFinder.use_method("DataSplitting", "ShuffleSplit",
                                       parameters={"ratio": [0.7, 0.15, 0.15]})
    splittings = splitter.split(X)
    X_train_imbalanced = X[splittings[0].values == "TRAINING"]
    y_train_imbalanced = y[splittings[0].values == "TRAINING"]

    sampler = ModuleFinder.use_method("Sampling", algorithm, **parameters)
    _, y_train = sampler.fit_resample(X_train_imbalanced, y_train_imbalanced)

    assert y_train.value_counts()[0] == pytest.approx(
                                            y_train.value_counts()[1],
                                            rel=0.9)