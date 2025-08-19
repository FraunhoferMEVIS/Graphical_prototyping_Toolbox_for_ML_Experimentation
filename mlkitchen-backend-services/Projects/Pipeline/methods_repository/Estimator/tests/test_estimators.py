""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_estimators.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The tests for the Estimators
-----------------------------------------------------------------------------
"""
import pytest
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler 
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize("algorithm", ["SequentialModel"])
def test_keras_model(example_data_set_timeseries, algorithm):

    target_col_ = 'hospital_expire_flag'
    parameters = {  "target_col": target_col_,
                    "identifier": 'subject_id',
                    "sequence_column": 'time_window',
                    "optimizer": 'adam',
                    "loss":'binary_crossentropy',
                    "metrics": ['accuracy'],
                    "batch_size":128,
                    "verbose":0,
                    "epochs":100,
                    "layers" : [{
                                    "name": "LSTM", 
                                    "parameters": {
                                        "units":27, "activation": 'sigmoid', "return_sequences": True}
                                },
                                {
                                    "name": "Flatten", 
                                    "parameters": {}
                                },
                                {
                                    "name": "Dense", 
                                    "parameters": {"units":1, "activation": 'sigmoid'}
                                },                                       
                            ]
                }

    normal_dist_features = ['age']
    other_dist_features = ['avg_gcseyes']
    ts_features = ['avg_gcseyes']

    model = ModuleFinder.use_method("Estimator", algorithm, **parameters)
    
    y = example_data_set_timeseries[target_col_]
    X = example_data_set_timeseries.drop(columns=target_col_)

    X_train, X_test, y_train, y_test = get_grouped_splitting(X, y)

    # preprocessing
    # impute previous or next value of a patient  (assuming, value did not change if it was not measured again)
    imputer = ModuleFinder.use_method("HandlingMissingValues",
                                      "PreviousAndNextValue",
                                      columns= ts_features,
                                      time_column='time_window',
                                      grouping_ids='subject_id')
    imputer.fit(X_train)
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)

    # if no value at all exists for a patient, fill with mean
    imputer = ModuleFinder.use_method("HandlingMissingValues", "Mean")
    imputer.fit(X_train)
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)
    
    if not isinstance(X_train, pd.DataFrame):
        output_feature_names = imputer.get_feature_names_out()
        X_train = pd.DataFrame(X_train, columns=output_feature_names)
        X_test = pd.DataFrame(X_test, columns=output_feature_names)

    ##standardize
    X_train[other_dist_features], X_test[other_dist_features] = normalize(
                            X_train[other_dist_features],
                            X_test[other_dist_features])
    X_train[normal_dist_features], X_test[normal_dist_features] = standardize(
                            X_train[normal_dist_features],
                            X_test[normal_dist_features])
    model.fit(X_train, y_train)
    res = model.predict(X_test)

    err = abs(res.reset_index(drop=True) - y_test.reset_index(drop=True)).mean()
    assert err <= 1.5

@pytest.mark.parametrize("algorithm", [
    "RandomForestRegressor", "Lasso", "LinearRegression", "SVR",
    "MLPRegressor", "BayesianRidge", "VotingRegressor", "RANSACRegressor",
    "PassiveAggressiveRegressor", "KNeighborsRegressor"])
def test_regression_algorithms(house_prices, algorithm):
    parameters = {
        "n_estimators": 200,
        "criterion": 'poisson',
        "random_state": 0,
        "estimators": [{"name": "RandomForestRegressor"},
                       {"name": "LinearRegression"},
                       {"name": "KNeighborsRegressor"},
                       {"name": "MLPRegressor"}, ],
        "kernel": [{"name": "Sum",
                    "parameters": {
                            "kernel": [{
                                "name": "RBF",
                                "length_scale": 1.0},
                                {"name": "Matern"}
                                ]}
                    }],
        "min_samples": 0.1
    }
    model = ModuleFinder.use_method("Estimator", algorithm, **parameters)

    X = house_prices.data
    y = house_prices.target

    X_train, X_test, y_train, y_test = get_splitting(X, y)

    # preprocessing
    imputer = ModuleFinder.use_method("HandlingMissingValues", "Mean")
    imputer.fit(X_train)
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)

    # Standardize
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    # Train
    model.fit(X_train, y_train)

    # Predict
    res = model.predict(X_test)
    err = abs(res - y_test).mean()
    assert err <= 1.5


# ####-------------- Test Kernels --------------------####
def test_SVR_Kernels(house_prices):
    algorithm = "SVR"
    X = house_prices.data
    y = house_prices.target

    X_train, X_test, y_train, y_test = get_splitting(X, y)

    # preprocessing
    imputer = ModuleFinder.use_method("HandlingMissingValues", "Mean")
    imputer.fit(X_train)
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)

    # Standardize
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    # Test SUM
    parameters = {
        "kernel": [{"name": "Sum",
                    "parameters": {
                            "kernel": [{
                                "name": "RBF",
                                "parameters": {
                                    "length_scale": 1.0
                                    }
                                },
                                {"name": "Matern"}
                                ]}
                    }],
                }
    model = ModuleFinder.use_method("Estimator", algorithm, **parameters)
    model.fit(X_train, y_train)
    res = model.predict(X_test)
    err = abs(res - y_test).mean()
    assert err <= 1.5

    # Test RBF
    parameters = {
        "kernel": [{
                    "name": "RBF",
                    "parameters": {
                        "length_scale": 1.0
                        }
                    }]
            }

    model = ModuleFinder.use_method("Estimator", algorithm, **parameters)
    model.fit(X_train, y_train)
    res = model.predict(X_test)
    err = abs(res - y_test).mean()
    assert err <= 1.5

@pytest.mark.parametrize("algorithm", [
    "AdaBoostClassifier", "ExtraTreesClassifier", "LinearDiscriminantAnalysis",
    "LogisticRegressionCV", "Perceptron", "RandomForestClassifier",
    "VotingClassifier", "KNeighborsClassifier", "MLPClassifier", "SVC"])
def test_classification_algorithms(iris_dataset, algorithm):
    parameters = {
        "n_estimators": 900,
        "random_state": 0,
        "criterion": "gini",
        "estimators": [{"name": "RandomForestClassifier"},
                       {"name": "LogisticRegression"}, {"name": "GaussianNB"},
                       {"name": "Perceptron"},
                       {"name": "LinearDiscriminantAnalysis"}],
    }
    model = ModuleFinder.use_method("Estimator", algorithm, **parameters)
    X = iris_dataset.data
    y = iris_dataset.target

    X_train, X_test, y_train, y_test = get_splitting(X, y)

    # Standardize
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    # Train
    model.fit(X_train, y_train)

    # Predict
    res = model.predict(X_test)
    assert sum(res == y_test) / len(y_test) >= 0.5

def get_splitting(X, y):
    splitter = ModuleFinder.use_method("DataSplitting",
                                       "ShuffleSplit",
                                       parameters={"ratio": [0.7, 0.15, 0.15]})
    splittings = splitter.split(X)
    X_train = X[splittings[0].values == "TRAINING"]
    y_train = y[splittings[0].values == "TRAINING"]

    X_validation = X[splittings[0].values == "VALIDATION"]
    y_validation = y[splittings[0].values == "VALIDATION"]
    return X_train, X_validation, y_train, y_validation


def get_grouped_splitting(X,y):
    splitting_parameters= {
            "group": "subject_id",
            "ratio": [0.7, 0.15, 0.15]
        }
    splitter = ModuleFinder.use_method("DataSplitting", "GroupShuffleSplit",
                                       **splitting_parameters)
    splittings= splitter.split(X)
    splitter.split(X)
    splittings = splitter.split(X)
    X_train = X[splittings[0].values == "TRAINING"]
    y_train = y[splittings[0].values == "TRAINING"]

    X_validation = X[splittings[0].values == "VALIDATION"]
    y_validation = y[splittings[0].values == "VALIDATION"]
    return X_train, X_validation, y_train, y_validation


def normalize(train,test):
    norm=MinMaxScaler().fit(train)
    return norm.transform (train), norm.transform(test)

def standardize(train,test):
    stnd=StandardScaler().fit(train)
    return stnd.transform (train), stnd.transform(test)