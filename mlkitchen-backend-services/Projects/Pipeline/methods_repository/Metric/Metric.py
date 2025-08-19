""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Metric.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The available Metrics in the repository
-----------------------------------------------------------------------------
"""
import inspect
from enum import Enum
from sklearn.metrics import (precision_recall_curve, auc)
from keras import metrics as keras_metrics
from methods_repository.config_models import ProgrammingLanguages, \
                                             MetricTypes, MetricsConfig


INDICES_OF_DATA_INPUT = [0, 1]
_IMPORT_THIS = "methods_repository.Metric.Metric"
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        # ############ Classification scores  #############
        "accuracy_score": {
            "import": "sklearn.metrics",
            "name": "accuracy_score",
            "flags": [MetricTypes.score_for_classification]
        },

        "balanced_accuracy_score": {
            "import": "sklearn.metrics",
            "name": "balanced_accuracy_score",
            "flags": [MetricTypes.score_for_classification]
        },

        "top_k_accuracy_score": {
            "import": "sklearn.metrics",
            "name": "top_k_accuracy_score",
            "flags": [MetricTypes.score_for_classification]
        },

        "average_precision_score": {
            "import": "sklearn.metrics",
            "name": "average_precision_score",
            "flags": [MetricTypes.score_for_classification]
        },

        "roc_auc_score": {
            "import": "sklearn.metrics",
            "name": "roc_auc_score",
            "flags": [MetricTypes.score_for_classification]
        },

        "f1_score": {
            "import": "sklearn.metrics",
            "name": "f1_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "fbeta_score": {
            "import": "sklearn.metrics",
            "name": "fbeta_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "precision_score": {
            "import": "sklearn.metrics",
            "name": "precision_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "recall_score": {
            "import": "sklearn.metrics",
            "name": "recall_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "jaccard_score": {
            "import": "sklearn.metrics",
            "name": "jaccard_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "cohen_kappa_score": {
            "import": "sklearn.metrics",
            "name": "cohen_kappa_score",
            "flags": [MetricTypes.score_for_classification]
        },
        "AUPRC": {
            "import": _IMPORT_THIS,
            "name": "area_under_precision_recall_curve",
            "flags": [MetricTypes.score_for_classification]
        },
        # ############ Classification loss #############
        "log_loss": {
            "import": "sklearn.metrics",
            "name": "log_loss",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_classification]
        },
        "brier_score_loss": {
            "import": "sklearn.metrics",
            "name": "brier_score_loss",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_classification]
        },
        "hamming_loss": {
            "import": "sklearn.metrics",
            "name": "hamming_loss",
            "flags": [MetricTypes.score_for_classification]
        },

        # ############ Regression score #############
        "explained_variance_score": {
            "import": "sklearn.metrics",
            "name": "explained_variance_score",
            "flags": [MetricTypes.score_for_regression],
        },
        "r2_score": {
            "import": "sklearn.metrics",
            "name": "r2_score",
            "greater_is_better": True,
            "flags": [MetricTypes.score_for_regression],
         },
        "mean_gamma_deviance": {
            "import": "sklearn.metrics",
            "name": "mean_gamma_deviance",
            "flags": [MetricTypes.score_for_regression],
         },
        "mean_absolute_percentage_error": {
            "import": "sklearn.metrics",
            "name": "mean_absolute_percentage_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "d2_absolute_error_score": {
            "import": "sklearn.metrics",
            "name": "d2_absolute_error_score",
            "flags": [MetricTypes.score_for_regression],
         },
        "d2_pinball_score": {
            "import": "sklearn.metrics",
            "name": "d2_pinball_score",
            "flags": [MetricTypes.score_for_regression],
         },
        "d2_tweedie_score": {
            "import": "sklearn.metrics",
            "name": "d2_tweedie_score",
            "flags": [MetricTypes.score_for_regression],
         },
        "max_error": {
            "import": "sklearn.metrics",
            "name": "max_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "mean_absolute_error": {
            "import": "sklearn.metrics",
            "name": "mean_absolute_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "mae": {
            "import": "sklearn.metrics",
            "name": "mean_absolute_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "mean_squared_error": {
            "import": "sklearn.metrics",
            "name": "mean_squared_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "mse": {
            "import": "sklearn.metrics",
            "name": "mean_squared_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "rmse": {
            "import": "sklearn.metrics",
            "name": "root_mean_squared_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression]
        },
        "root_mean_squared_error": {
            "import": "sklearn.metrics",
            "name": "root_mean_squared_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression]
        },
        "mean_squared_log_error": {
            "import": "sklearn.metrics",
            "name": "mean_squared_log_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "median_absolute_error": {
            "import": "sklearn.metrics",
            "name": "median_absolute_error",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },
        "mean_poisson_deviance": {
            "import": "sklearn.metrics",
            "name": "mean_poisson_deviance",
            "greater_is_better": False,
            "flags": [MetricTypes.score_for_regression],
         },

        # ############ Classification Metric reports and matrices #############
        # no tests for reports and metric
        # prints metrics (preciscion, recall, f1-score, support) for micro,
        # macro,weighted average as well as for each class
        "classification_report": {
            "import": "sklearn.metrics",
            "name": "classification_report",
            "type": MetricTypes.score_for_classification,
        },
        "confusion_matrix": {
            "import": "sklearn.metrics",
            "name": "confusion_matrix",
            "type": MetricTypes.score_for_classification,
        },
    }
}


def get_greater_is_better(metric: MetricsConfig):
    """
    gets the "greater_is_better" value for the given metric config.
    If it is defined in the input config, the value will be returned.
    If it is not defined, finds the value from the repo.
    :metric: the input metric configuration
    If the metric
    :raises ValueError if it is not defined in the repository
    or is not given as input.
    """
    if not (language := metric.language):
        language = ProgrammingLanguages.Python
    if metric.greater_is_better:
        return metric.greater_is_better
    if language in List_of_Algorithms and \
            metric.name in List_of_Algorithms[language] and \
            "greater_is_better" in List_of_Algorithms[language][metric.name]:
        return List_of_Algorithms[language][metric.name]["greater_is_better"]
    return True
    # raise ValueError(f"greater_is_better is not defined for {metric.name}")


def area_under_precision_recall_curve(y_true: list[float],
                                      y_score: list[float]) -> float:
    """
    Computes the Area Under the Precision-Recall Curve (AUPRC),
    based on the ground truth and the prediction scores.
    Current implementation is for binary classification.
    """
    precision, recall, _ = precision_recall_curve(y_true,
                                                  y_score)
    auc_precision_recall = auc(recall, precision)
    return auc_precision_recall


class AveragingOptions(str, Enum):
    micro = "micro"
    macro = "macro"
    weighted = "weighted"
    samples = "samples"


class ExtendedAveragingOptions(str, Enum):
    binary = "binary"
    micro = "micro"
    macro = "macro"
    weighted = "weighted"
    samples = "samples"


class MultiClassOptions(str, Enum):
    raise_ = "raise"
    ovr = "ovr"
    ovo = "ovo"


def get_parameter_type_and_options(algorithm_name: str, parameter: str):
    """
    Gets the type and options of the parameter for the given algorithm.
    """
    parameter_type_options = {
        'y_true': ("list[float]", None),
        'y_pred': ("list[float]", None),
        'y_score': ("list[float]", None),
        'normalize': ("bool", None),
        'beta': ("float", None),
        'pos_label': ("int", None),
        'sample_weight': (None, None),
        'zero_division': (None, None),
        'labels': (None, None)
    }
    if algorithm_name in {'average_precision_score', 'roc_auc_score'}:
        parameter_type_options['average'] = ("Enum", list(AveragingOptions))
    elif algorithm_name in {'f1_score', 'fbeta_score'}:
        parameter_type_options['average'] = ("Enum", list(ExtendedAveragingOptions))
    else:
        parameter_type_options['average'] = (None, None)
    
    return parameter_type_options.get(parameter, (None, None))
    
        

def generate_metrics_dic_keras():
    list_ = inspect.getmembers(keras_metrics)
    metric_dic = {}
    for name, _ in list_:
        metric_dic[name] = {
            "import": "keras.metrics",
            "name": name,
            "flag": "keras",
        }
    return metric_dic


List_of_KerasMetrics = {
    ProgrammingLanguages.Python: generate_metrics_dic_keras()
}
