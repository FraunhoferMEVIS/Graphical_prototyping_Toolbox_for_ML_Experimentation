""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: config_model.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: Requiered configurations and inputs defining different steps
             of the project
-----------------------------------------------------------------------------
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel


class TaskTypes(str, Enum):
    classification = "classification"
    regression = "regression"
    clustering = "clustering"
    timeseries_regression = "timeseries_regression"
    timeseries_classification = "timeseries_classification"
    anomaly_detection = "anomaly_detection"
    data_transformation = "data_transformation"


class SamplingTypes(str, Enum):
    oversampling = "oversampling"
    undersampling = "undersampling"
    over_undersampling = "over_undersampling"


class FeatureSelectionTypes(str, Enum):
    estimator_based = "estimator_based"
    statistical_based = "statistical_based"


class MetricTypes(str, Enum):
    score_for_regression = "score_for_regression"
    score_for_clustering = "score_for_clustering"
    score_for_classification = "score_for_classification"


class VisualizationTypes(str, Enum):
    plot = "plot"
    grid = "grid"


class ProgrammingLanguages(str, Enum):
    Python = "python"
    R = "r"


class DataTypes(str, Enum):
    """
    different types of data columns.
    """
    numerical = 'numerical'
    categorical = 'categorical'


class AlgorithmConfig(BaseModel):
    name: str
    library: (str | None) = None
    language: ProgrammingLanguages | None = None
    parameters: dict[str, Any] | None = None

    def to_yaml_dict(self):
        yaml_format = {}
        if self.name:
            yaml_format['name'] = self.name
        if self.library:
            yaml_format['library'] = self.library
        if self.language:
            yaml_format['language'] = self.language.value
        if self.parameters:
            yaml_format['parameters'] = self.parameters
        return yaml_format


class MetricsConfig(AlgorithmConfig):
    threshold: float | None = None
    greater_is_better: bool | None = None

    def to_yaml_dict(self):
        yaml_format = super().to_yaml_dict()
        if self.threshold:
            yaml_format['threshold'] = self.threshold
        if self.greater_is_better:
            yaml_format['greater_is_better'] = self.greater_is_better
        return yaml_format


class ColumnTransformerConfig(AlgorithmConfig):
    """
    if column name is given, the method will be applied only to the specified
    column name. Otherwise, if "all_numerical" is equal to True, the method
    will be applied to all numerical columns, and/or if "all_categorical" is
    equal to True, the method will be applie to all categorical columns of
    the dataset. If none of these inputs are set, the method is applied to
    all columns, except for Identifier columns, e.g. subject_id.
    """
    column_name: (list[str] | None) = None
    all_numerical: (bool | None) = None
    all_categorical: (bool | None) = None

    def to_yaml_dict(self):
        yaml_format = super().to_yaml_dict()
        if self.column_name:
            yaml_format['ratio'] = self.column_name
        if self.all_numerical:
            yaml_format['all_numerical'] = self.all_numerical
        if self.all_categorical:
            yaml_format['all_categorical'] = self.all_categorical
        return yaml_format


class SplitConfig(AlgorithmConfig):
    ratio: list[float] = [0.7, 0.2, 0.1]
    name: str | None = None

    def to_yaml_dict(self):
        yaml_format = super().to_yaml_dict()
        if self.ratio:
            yaml_format['ratio'] = self.ratio
        return yaml_format


class SamplingConfig(AlgorithmConfig):
    """
    configuration for resampling
    The resampling is applied, only if the ration of minority
    class is smaller than the value stored in 
    'resampling_minority_percentage'
    """
    #Currently, we only use the method implemented in mlflow
    name: str | None = None
    resampling_minority_percentage: float = 0.00001

    def to_yaml_dict(self):
        yaml_format = super().to_yaml_dict()
        yaml_format['resampling_minority_percentage'] = \
                            self.resampling_minority_percentage
        return yaml_format


class NewFeatureConfig(AlgorithmConfig):
    column_name: str

    def to_yaml_dict(self):
        yaml_format = super().to_yaml_dict()
        if self.column_name:
            yaml_format['column_name'] = self.column_name
        return yaml_format


class RecipeConfig(BaseModel):
    """
    The configuration structure of the recipe that should be
    defined as the input.
    """
    username: str
    description: (str | None) = None
    task: TaskTypes
    target_col: str
    positive_class: (int | bool | str | None) = None
    split: SplitConfig
    imputation: (list[ColumnTransformerConfig] | None) = None
    encoders: (list[ColumnTransformerConfig] | None) = None
    feature_selection: (AlgorithmConfig | None) = None
    metrics: list[MetricsConfig]
    primaryMetric: (str | list[str])
    estimator: (AlgorithmConfig | list[AlgorithmConfig] | None) = None
    sampling: SamplingConfig | None = None
    new_feature: (list[NewFeatureConfig] | None) = None

    def to_yaml_dict(self):
        yaml_format = {}
        if self.username:
            yaml_format['username'] = self.username
        if self.description:
            yaml_format['description'] = self.description
        if self.task:
            yaml_format['task'] = self.task.value
        if self.target_col:
            yaml_format['target_col'] = self.target_col
        if self.positive_class:
            yaml_format["positive_class"] = self.positive_class
        if self.split:
            yaml_format['split'] = self.split.to_yaml_dict()
        if self.imputation is not None:
            yaml_format['imputation'] = [imputation.to_yaml_dict()
                                         for imputation in self.imputation]
        if self.encoders is not None:
            yaml_format['encoders'] = [encoders.to_yaml_dict()
                                       for encoders in self.encoders]
        if self.feature_selection:
            yaml_format['feature_selection'] = \
                    self.feature_selection.to_yaml_dict()

        if self.metrics:
            yaml_format['metrics'] = [metric.to_yaml_dict()
                                      for metric in self.metrics]
        if self.primaryMetric:
            yaml_format['primaryMetric'] = self.primaryMetric
        if self.estimator is not None:
            if isinstance(self.estimator, list):
                yaml_format['estimator'] = [estimator.to_yaml_dict()
                                            for estimator in self.estimator]
            else:
                yaml_format['estimator'] = self.estimator.to_yaml_dict()
        if self.sampling:
            yaml_format["sampling"] = self.sampling.to_yaml_dict()
        if self.new_feature is not None:
            yaml_format['new_feature'] = [new_feature.to_yaml_dict()
                                          for new_feature in self.new_feature]
        return yaml_format

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "J.Doe",
                    "description":
                        "Predicting in-hospital expiration based on SAPSS-II",
                    "task": "classification",
                    "target_col": "hospital_expire_flag",
                    "sampling": {
                        "resampling_minority_percentage": 0.3,
                    },
                    "positive_class": 1,
                    "split": {"ratio": [0.75, 0.15, 0.1]},
                    "imputation": [{"name": "Median", "all_numerical": True}],
                    "encoders": [
                        {
                            "all_categorical": True,
                            "name": "OneHotEncoder",
                            "parameters": {
                                "handle_unknown": "ignore",
                                "drop": "if_binary",
                                "sparse_output": False
                            }
                        },
                        {
                            "name": "StandardScaler",
                            "all_numerical": True
                        }
                    ],
                    "feature_selection": {
                        "name": "SelectKBest",
                        "parameters": {
                            "score_func": "mutual_info_regression",
                            "k": 25}},
                    "metrics": [{"name": "balanced_accuracy_score",
                                 "threshold": 0.5},
                                {"name": "f1_score",
                                    "threshold": 0.5}],
                    "primaryMetric": ["f1_score"],
                    "estimator": [
                        {"name": "RandomForestClassifier",
                            "library": "sklearn",
                            "language": "python",
                            "parameters": {
                                "hyper_parameter_tuning":
                                    "RandomizedSearchCV",
                                "search_space": {
                                    "n_estimators": {
                                        "values": [50, 100, 200,
                                                   400, 800]
                                    },
                                    "max_depth": {
                                        "function": "randint",
                                        "parameters": {
                                            "low": 5,
                                            "high": 15
                                        }}
                                }
                            }},
                        {"name": "LogisticRegression",
                            "library": "sklearn",
                            "language": "python"}
                        ]
                },
                {
                    "username": "J.Doe",
                    "description":
                        "Predicting Number of Days at ICU based on SAPSS-II",
                    "task": "regression",
                    "target_col": "stay_duration",
                    "split": {"ratio": [0.75, 0.15, 0.1]},
                    "imputation": [{"name": "Median", "all_numerical": True}],
                    "feature_selection": {
                        "name": "SelectKBest",
                        "parameters": {
                            "score_func": "mutual_info_regression",
                            "k": 25}},
                    "metrics": [{"name": "rmse",
                                 "threshold": 5},
                                {"name": "r2_score",
                                 "threshold": 0.5}],
                    "primaryMetric": ["r2_score"],
                    "new_feature": [

                    ]
                }
            ]
        }
    }
