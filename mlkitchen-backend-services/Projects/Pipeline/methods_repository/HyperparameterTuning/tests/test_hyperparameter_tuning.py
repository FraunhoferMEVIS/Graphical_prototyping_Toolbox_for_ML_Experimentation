""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_hyperparameter_tuning.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: Test the hyperparamter tuning modules.
-----------------------------------------------------------------------------
"""
import pytest
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize("algorithm", [
     "GridSearchCV"])  # , "RandomizedSearchCV", "BayesSearchCV"])
def test_hyperparameter_tuning_for_regression(house_prices, algorithm):
    estimator = "RandomForestRegressor"
    parameters = {
        "hyper_parameter_tuning": algorithm,
        "search_space": {
            "n_estimators": {"values": [50, 200]},
        },
        "random_state": 0,
        "min_samples": 0.1
    }
    model = ModuleFinder.use_method("Estimator", estimator, **parameters)

    X = house_prices.data
    y = house_prices.target

    # Train
    model.fit(X, y)

    # Predict
    res = model.predict(X)
    err = abs(res - y).mean()
    assert err <= 1.5
