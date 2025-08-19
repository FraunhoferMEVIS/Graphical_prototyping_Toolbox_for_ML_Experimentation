""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: FeatureSeletion.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: List of feature selection algorithms.
-----------------------------------------------------------------------------
"""
import importlib
import logging
from pandas import DataFrame
from methods_repository.config_models import ProgrammingLanguages, \
                                             FeatureSelectionTypes, TaskTypes


_logger = logging.getLogger(__name__)


List_of_Algorithms = {
    ProgrammingLanguages.Python: {

        "SequentialFeatureSelector": {
            "import": "sklearn.feature_selection",
            "name": "SequentialFeatureSelector",
            "flags": [FeatureSelectionTypes.estimator_based,
                      TaskTypes.classification, TaskTypes.regression]
        },

        "GenericUnivariateSelect": {
            "import": "sklearn.feature_selection",
            "name": "GenericUnivariateSelect",
            "flags": [FeatureSelectionTypes.statistical_based,
                      TaskTypes.classification, TaskTypes.regression]

        },
        "SelectPercentile": {
            "import": "sklearn.feature_selection",
            "name": "SelectPercentile",
            "flags": [FeatureSelectionTypes.statistical_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "SelectKBest": {
            "import": "sklearn.feature_selection",
            "name": "SelectKBest",
            "flags": [FeatureSelectionTypes.statistical_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "SelectFromModel": {
            "import": "sklearn.feature_selection",
            "name": "SelectFromModel",
            "flags": [FeatureSelectionTypes.estimator_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "SelectFwe": {
            "import": "sklearn.feature_selection",
            "name": "SelectFwe",
            "flags": [FeatureSelectionTypes.statistical_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "RFE": {
            "import": "sklearn.feature_selection",
            "name": "RFE",
            "flags": [FeatureSelectionTypes.estimator_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "RFECV": {
            "import": "sklearn.feature_selection",
            "name": "RFECV",
            "flags": [FeatureSelectionTypes.estimator_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "VarianceThreshold": {
            "import": "sklearn.feature_selection",
            "name": "VarianceThreshold",
            "flags": [FeatureSelectionTypes.statistical_based,
                      TaskTypes.classification, TaskTypes.regression]
        },
        "SelectByName": {
            "import": "methods_repository.FeatureSelection.FeatureSelection",
            "name": "SelectByName",
            "flags": []
        },
    }
}


class SelectByName():
    """
    A Feature Selection Transformer, based on the user's input.
    A user can pass the list of features to select and decide to
    only keep these features (default), or remove them from the
    feature set.

    Parameters
    ----------
    feature_names : [str], default=None
        The list of features that should be kept or removed.

    keep : bool, default=True
        If set to True the list of features will be kept and all
        the others will be removed. If set to False, all the features
        in the list of feature_names will be removed an the rest of
        the features will be kept.

    Attributes
    ----------
    n_features_in_ : int
        Number of features seen during :term:`fit`.

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Defined only when `X` has
        feature names that are all strings.

    """

    def __init__(
        self,
        feature_names: list[str] = None,
        keep: bool = True
    ):
        self._feature_names = feature_names
        self._keep = keep

    def fit(self, X: DataFrame, y=None):
        """Fit transformer by checking X.

        Parameters
        ----------
        X : DataFrame or any data type that supports "columns" method and
            can be indexed by name.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            FunctionTransformer class instance.
        """
        if self._keep:
            self._feature_names_out = self._feature_names
        else:
            self._feature_names_out = [col for col in X.columns
                                       if col not in self._feature_names]
        return self

    def transform(self, X):
        """Transform X using the forward function.

        Parameters
        ----------
        X : DataFrame or any data type that supports "columns" and drop method.

        Returns
        -------
        X_out : Transformed input.
        """
        return X[self._feature_names_out]

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        return self._feature_names_out



def get_parameter_type_and_options(algorithm_name: str, parameter: str):
    """
    Gets the type and options of the parameter for the given algorithm.
    """

    def get_estimators_with_specific_task_type(task_types: list[str]):
        step_module = importlib.import_module(
            "methods_repository.Estimator.Estimator")

        list_of_estimators = []
        for algorithm in step_module.List_of_Algorithms.get(language, {}):
            for task_type in task_types:
                if task_type in step_module.List_of_Algorithms[language][algorithm]['flags']:
                    list_of_estimators.append(algorithm)
        return list_of_estimators

    def extract_required_task_type(algorithm_name: str):
        task_types = []
        for tt in List_of_Algorithms[language][algorithm_name]['flags']:
            if tt in TaskTypes:
                task_types.append(tt)
        return task_types

    language = ProgrammingLanguages.Python
    param_type, param_options = None, None

    if parameter in {'estimator', 'final_estimator'}:
        param_type = 'Estimator'
        param_options = get_estimators_with_specific_task_type(task_types=extract_required_task_type(algorithm_name))
    elif parameter == 'estimators':
        param_type = 'list[Estimator]'
        param_options = get_estimators_with_specific_task_type(task_types=extract_required_task_type(algorithm_name))

    return param_type, param_options
