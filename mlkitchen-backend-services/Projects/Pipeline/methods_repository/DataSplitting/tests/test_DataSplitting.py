""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_DataSplitting.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The tests for the DataSplitting modules
-----------------------------------------------------------------------------
"""
import pytest
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize("algorithm", ["StratifiedGroupKFold", "GroupShuffleSplit"])
def test_splitting_algorithms_grouped(example_data_set_timeseries,
                              algorithm):
    parameters = {
        "StratifiedGroupKFold": {
            "n_splits": 5,
            "group": "subject_id",
            "target_col": "hospital_expire_flag",
            "test_size": 0.2,
        },
        "GroupShuffleSplit": {
            "group": "subject_id",
            "validation_size": 0.15,
            "test_size": 0.15,
        },
    }
    
    expected_number_groups = len(example_data_set_timeseries[parameters[algorithm]['group']].unique())
    expected_result_size = {
        "StratifiedGroupKFold": {
            "folds": parameters["StratifiedGroupKFold"]["n_splits"],
            "TEST": int(len(example_data_set_timeseries) *
                        parameters["StratifiedGroupKFold"]["test_size"]),
            "TRAINING": int(len(example_data_set_timeseries) *
                            (1 - parameters["StratifiedGroupKFold"]["test_size"]) /
                            parameters["StratifiedGroupKFold"]["n_splits"] *
                            (parameters["StratifiedGroupKFold"]["n_splits"] - 1)),
            "VALIDATION": int(len(example_data_set_timeseries) *
                              (1 - parameters["StratifiedGroupKFold"]["test_size"]) /
                              parameters["StratifiedGroupKFold"]["n_splits"]),
            },
        "GroupShuffleSplit": {
            "folds": 1,
            "TEST": int(len(example_data_set_timeseries) *
                        parameters["GroupShuffleSplit"]["test_size"]),
            "TRAINING": int(len(example_data_set_timeseries) *
                            (1 - parameters['GroupShuffleSplit']["test_size"] - parameters['GroupShuffleSplit']["validation_size"])),
            "VALIDATION": int(len(example_data_set_timeseries) *
                              parameters["GroupShuffleSplit"]["validation_size"]),
        },
    }
    splitter = ModuleFinder.use_method("DataSplitting", algorithm,
                                       **parameters[algorithm])
    result = splitter.split(example_data_set_timeseries)
    sum_groups=[]
    for i, res in enumerate(result):
        example_data_set_timeseries['set'] = res
        unique_groups = example_data_set_timeseries.groupby('set')[parameters[algorithm]['group']].unique()
        sum_groups.append(sum_number_groups(unique_groups))
        assert sum_groups[i] == expected_number_groups
    
    assert len(result) == expected_result_size[algorithm]["folds"]
    
    for r in result:
        for split in ("TRAINING", "VALIDATION", "TEST"):
            print(split )
            assert len(example_data_set_timeseries[r.values == split])/len(example_data_set_timeseries) == pytest.approx((expected_result_size[algorithm][split])/len(example_data_set_timeseries), 0.3)

@pytest.mark.parametrize("algorithm", ["KFold",  "LeaveOneOut",
                                       "ShuffleSplit"])
def test_splitting_algorithms(example_data_set,
                              algorithm):
    parameters = {
        "KFold": {
            "n_splits": 5,
            "test_size": 0.2
        },
        "LeaveOneOut": {
            "test_size": 0.2
        },
        "ShuffleSplit": {
            "validation_size": 0.15,
            "test_size": 0.15
        }
    }
    expected_result_size = {
        "KFold": {
            "folds": parameters["KFold"]["n_splits"],
            "TEST": int(len(example_data_set) *
                        parameters["KFold"]["test_size"]),
            "TRAINING": int(len(example_data_set) *
                            (1 - parameters["KFold"]["test_size"]) /
                            parameters["KFold"]["n_splits"] *
                            (parameters["KFold"]["n_splits"] - 1)),
            "VALIDATION": int(len(example_data_set) *
                              (1 - parameters["KFold"]["test_size"]) /
                              parameters["KFold"]["n_splits"]),
            },
        "LeaveOneOut": {
            "folds": int(len(example_data_set) *
                         (1 - parameters["LeaveOneOut"]["test_size"])),
            "TEST": int(len(example_data_set) *
                        parameters["LeaveOneOut"]["test_size"]),
            "TRAINING": int(len(example_data_set) *
                            (1 - parameters["LeaveOneOut"]["test_size"]) - 1),
            "VALIDATION": 1
        },
        "ShuffleSplit": {
            "folds": 1,
            "TEST": int(len(example_data_set) *
                        parameters["ShuffleSplit"]["test_size"]),
            "TRAINING": int(len(example_data_set) *
                            (1 - parameters["ShuffleSplit"]["test_size"] - parameters["ShuffleSplit"]["validation_size"])),
            "VALIDATION": int(len(example_data_set) *
                              parameters["ShuffleSplit"]["validation_size"]),
        },
    }
    splitter = ModuleFinder.use_method("DataSplitting", algorithm,
                                       **parameters[algorithm])
    result = splitter.split(example_data_set)
    assert len(result) == expected_result_size[algorithm]["folds"]

    for r in result:
        for split in ("TRAINING", "VALIDATION", "TEST"):
            assert expected_result_size[algorithm][split] - 1 <= \
              len(example_data_set[r.values == split]) <= \
              expected_result_size[algorithm][split] + 1


@pytest.mark.parametrize("algorithm", ["LeavePOut"])
def test_splitting_expensive_algorithms(example_small_data_set,
                                        algorithm):
    parameters = {
        "LeavePOut": {
            "test_size": 0.2,
            "p": 2,
        }
    }

    expected_result_size = {
        "LeavePOut": {
            "folds": ncr(int(len(example_small_data_set) *
                         (1 - parameters["LeavePOut"]["test_size"])),
                         parameters[algorithm]["p"]),
            "TEST": int(len(example_small_data_set) *
                        parameters["LeavePOut"]["test_size"]),
            "TRAINING": int(len(example_small_data_set) *
                            (1 - parameters["LeavePOut"]["test_size"]) - 1),
            "VALIDATION": 1
        },
    }

    splitter = ModuleFinder.use_method("DataSplitting", algorithm,
                                       **parameters[algorithm])
    result = splitter.split(example_small_data_set)
    assert len(result) == expected_result_size[algorithm]["folds"]
    for r in result:
        for split in ("TRAINING", "VALIDATION", "TEST"):
            assert expected_result_size[algorithm][split] - 1 <= \
              len(example_small_data_set[r.values == split]) <= \
              expected_result_size[algorithm][split] + 1


def ncr(n, r):
    def mul(vec):
        res = 1
        for v in vec:
            res *= v
        return res

    r = min(r, n-r)
    numerator = mul(list(range(n-r+1, n+1)))
    denominator = mul(list(range(1, r+1)))
    return numerator // denominator


def sum_number_groups(unique_groups):
    s = 0
    for group in unique_groups:
        s = s + len(group)
    return s
