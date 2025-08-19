""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_metric.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The test functions for testing Metric functions
-----------------------------------------------------------------------------
"""

import pytest
from methods_repository.abstraction import ModuleFinder
from methods_repository.Estimator.tests.test_estimators import get_splitting


def get_sample_classification_parameters():
    """
    return sample classification parameters
    """
    return {
        "n_estimators": 900,
        "random_state": 0,
        "criterion": "gini",
    }


@pytest.mark.parametrize("algorithm", [("accuracy_score", 1),
                                       ("balanced_accuracy_score", 1),
                                       ("f1_score", 1), ("fbeta_score", 1),
                                       ("precision_score", 1),
                                       ("recall_score", 1),
                                       ("jaccard_score", 1),
                                       ("average_precision_score", 1),
                                       ("top_k_accuracy_score", 1)])
def test_metric_classification_algorithms(breast_cancer, algorithm):
    parameters_classification = get_sample_classification_parameters()
    # Data
    X = breast_cancer.data
    y = breast_cancer.target
    X_train, X_test, y_train, y_test = get_splitting(X, y)
    X_train, X_test = get_preprocessed_X(X_train, X_test)
    X_train, X_test = get_standardized_X(X_train, X_test)

    # Train
    model = ModuleFinder.use_method("Estimator", "AdaBoostClassifier",
                                    **parameters_classification)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Predict
    parameters_metric = {
        "y_true": y_test,
        "y_pred": y_pred,
        "y_score": y_pred,
        "normalize": True,
        'average': 'macro',
        "beta": 0.7,
    }
    metric = ModuleFinder.use_method("Metric", algorithm[0],
                                     **parameters_metric)
    assert metric == pytest.approx(algorithm[1], abs=0.5)


@pytest.mark.parametrize("algorithm", [("log_loss", 0),
                                       ("brier_score_loss", 0),
                                       ("roc_auc_score", 1),
                                       ("AUPRC", 1),])
def test_metric_classification_probability_algorithms(breast_cancer,
                                                      algorithm):
    parameters_classification = get_sample_classification_parameters()
    # Data
    X = breast_cancer.data
    y = breast_cancer.target
    X_train, X_test, y_train, y_test = get_splitting(X, y)
    X_train, X_test = get_preprocessed_X(X_train, X_test)
    X_train, X_test = get_standardized_X(X_train, X_test)

    # Train
    model = ModuleFinder.use_method("Estimator", "RandomForestClassifier",
                                    **parameters_classification)
    model.fit(X_train, y_train)
    y_pred_prob = model.predict_proba(X_test)
    print(y_pred_prob[:, 1])
    # Predict
    parameters_metric = {
        "y_true": y_test,
        "y_pred": y_pred_prob,
        "y_prob": y_pred_prob[:, 1],
        "y_score": y_pred_prob[:, 1],
        "normalize": True,
        'average': 'macro',
        "beta": 0.7,
    }
    metric = ModuleFinder.use_method("Metric", algorithm[0],
                                     **parameters_metric)
    assert metric == pytest.approx(algorithm[1], abs=0.5)


# Not scaled errors:
    # "mean_absolute_percentage_error" can be arbitrary high if y_true is zero
    # (because of division by epsilon)
    # "max_error" calculates the maximum residual error
    # "mean_poisson_deviance" Tweedie deviance with the power
    # parameter power=1.
@pytest.mark.parametrize("algorithm", [("mean_squared_error", 0),
                                       ("mean_squared_log_error", 0),
                                       ("median_absolute_error", 0),
                                       ("mean_absolute_error", 0),
                                       ("explained_variance_score", 1),
                                       ("r2_score", 1),
                                       ("d2_tweedie_score", 1),
                                       ("d2_absolute_error_score", 1),
                                       ("d2_pinball_score", 1)])
def test_metric_regression_algorithms(iris_dataset, algorithm):
    parameters_regression = {
        "n_estimators": 900,
        "criterion": 'poisson',
        "random_state": 0,
    }
    # Data
    X = iris_dataset.data
    y = iris_dataset.target
    X_train, X_test, y_train, y_test = get_splitting(X, y)
    X_train, X_test = get_preprocessed_X(X_train, X_test)
    X_train, X_test = get_standardized_X(X_train, X_test)

    # Train
    model = ModuleFinder.use_method("Estimator", "RandomForestRegressor",
                                    **parameters_regression)

    # Train
    model.fit(X_train, y_train)
    # Predict
    y_pred = model.predict(X_test)

    # Predict
    parameters_metric = {
        "y_true": y_test,
        "y_pred": y_pred,
        "y_score": y_pred,
        "normalize": True,
        'average': 'macro',
        "beta": 0.7,
    }
    metric = ModuleFinder.use_method("Metric", algorithm[0],
                                     **parameters_metric)
    assert metric == pytest.approx(algorithm[1], abs=0.5)


@pytest.mark.parametrize("algorithm", ["classification_report",
                                       "confusion_matrix"])
def test_reports_classification_algorithms(breast_cancer, algorithm):
    parameters_classification = get_sample_classification_parameters()

    # Data
    X = breast_cancer.data
    y = breast_cancer.target
    X_train, X_test, y_train, y_test = get_splitting(X, y)
    X_train, X_test = get_preprocessed_X(X_train, X_test)
    X_train, X_test = get_standardized_X(X_train, X_test)

    # Train and predict
    model = ModuleFinder.use_method("Estimator", "RandomForestClassifier",
                                    **parameters_classification)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Metric
    parameters_metric = {
        "y_true": y_test,
        "y_pred": y_pred,
        "y_score": y_pred,
        'average': 'macro',
    }
    report = ModuleFinder.use_method("Metric", algorithm, **parameters_metric)
    print('\nreprot\n', report)


def get_preprocessed_X(X_train, X_test):
    imputer = ModuleFinder.use_method("HandlingMissingValues", "Mean")
    imputer.fit(X_train)
    return imputer.transform(X_train), imputer.transform(X_test)


def get_standardized_X(X_train, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    return (X_train - mean) / std, (X_test - mean) / std
