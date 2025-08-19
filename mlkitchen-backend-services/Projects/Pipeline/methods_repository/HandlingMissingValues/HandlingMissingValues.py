""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: HandlingMissingValues.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The available modules for data imputation
-----------------------------------------------------------------------------
"""

from copy import deepcopy
import logging
import inspect
from typing import Any
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn import impute
from sklearn.base import BaseEstimator, TransformerMixin
from methods_repository.config_models import ProgrammingLanguages


_logger = logging.getLogger(__name__)


_IMPORT_THIS = "methods_repository.HandlingMissingValues.HandlingMissingValues"
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "Median": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByMedian",
        },
        "MedianGrouped": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByMedianGrouped",
        },

        "Mean": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByMean",
        },

        "MeanGrouped": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByMeanGrouped",
        },

        "MostFrequent": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByMostFrequent",
        },
        "PreviousAndNextValue": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByPreviousAndNextValue",
        },
        "DropColumnsWithMissingRatio": {
            "import": _IMPORT_THIS,
            "name": "DropColumnsWithMissingRatio",
        },
        "DropSubjectWithMissingRatio": {
            "import": _IMPORT_THIS,
            "name": "DropSubjectWithMissingRatio",
        },
        "NormalValue": {
            "import": _IMPORT_THIS,
            "name": "ReplaceByNormalValue",
        },
        "Iterative_Imputer": {
            "import": _IMPORT_THIS,
            "name": "Iterative_Imputer",
        },
        "KNNImputer": {
            "import": _IMPORT_THIS,
            "name": "KNNImputer",
        },
    },
    ProgrammingLanguages.R: {},
}


class BaseMissingValueHandling(BaseEstimator, TransformerMixin):

    def __init__(self, columns = None, passthrough=True) -> None:
        super().__init__()
        self._columns = columns
        self._columns_out = None
        self._imputer = None
        self._passthrough = passthrough

    def fit(self, X: pd.DataFrame, y=None, **kwargs):
        """
        Preparing the class based on the input training dataset
        """
        if self._columns:
            if callable(self._columns):
                self._columns = self._columns(X)
            self._imputer = self._imputer.fit(X[self._columns])
            self._columns_out = list(self._imputer.get_feature_names_out())
            if self._passthrough:
                self._columns_out += list(X.columns.difference(self._columns))
        else:
            self._imputer =  self._imputer.fit(X)
            self._columns_out = list(self._imputer.get_feature_names_out())
        return self

    def transform(self, X: pd.DataFrame):
        """
        Applying the method on input data
        """
        if self._columns:
            transformed_data = pd.DataFrame(self._imputer.transform(X[self._columns]),
                                            columns=self._imputer.get_feature_names_out())
            if self._passthrough:
                passing_features = X.columns.difference(self._columns)
                transformed_data[passing_features] = X[passing_features]
        else:
            transformed_data = self._imputer.transform(X)
        return transformed_data

    def get_params(self, deep=True):
        params = {
            "columns": self._columns,
            "passthrough": self._passthrough
        }
        return params

    def get_column_names(self, data):
        return self._columns if self._columns else data.columns
    
    def get_feature_names_out(self, *args, **params):
        return self._columns_out


class ReplaceByMedian(BaseMissingValueHandling):
    """
    Using this method, all the missing values for given or all parameters \
    are replaced with the median of the training dataset.
    For example, if the value of heart_beat_rate was measured every one hour \
    except at 2:00. The missing value then will be replaced by the median of \
    all measured values for the given patient.
    """
    def __init__(self, columns: list[str] | None = None, **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        kwargs['strategy'] = 'median'
        self._imputer = impute.SimpleImputer(**kwargs)
        _logger.info('\nCreated object of ReplaceWithMedian')


class ReplaceByMean(BaseMissingValueHandling):
    """
    Using this method, all the missing values for given or all parameters \
    are replaced with the mean of the training dataset.
    For example, if the value of heart_beat_rate was measured every one hour \
    except at 2:00. The missing value then will be replaced by the mean of \
    all measured values for the given patient.
    """
    def __init__(self, columns: list[str] | None = None, **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        kwargs['strategy'] = 'mean'
        self._imputer = impute.SimpleImputer(**kwargs)
        _logger.info('\nCreated object of ReplaceWithMean')


class ReplaceByMostFrequent(BaseMissingValueHandling):
    """
    Using this method, all the missing values for given or all parameters \
    are replaced with the most common value in the training dataset.
    For example, if the value of admission_type was not mentioned for a
    patient In the ICU. The missing value then will be replaced by \
    the most common value in the database.
    """
    def __init__(self, columns: list[str] | None = None, **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        kwargs['strategy'] = 'most_frequent'
        self._imputer = impute.SimpleImputer(**kwargs)
        _logger.info('\nCreated object of ReplaceWithMostFrequent')


class ReplaceByMeanGrouped(BaseMissingValueHandling):
    """  
    Using this method, all the missing values for given or all columns (except grouping_ids)
    are replaced with the mean of the group of the training dataset.
    For example, if the value of heart_beat_rate was measured every one hour
    except at 2:00. The missing value then will be replaced by the mean of
    all measured values of the patient.
    """
    def __init__(self, grouping_ids: list[str] | str, columns = None,
                 **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        self._groupby = grouping_ids
        if isinstance(self._groupby, str):
            self._groupby = [self._groupby]
        _logger.info('\nCreated object of %s', self.__class__.__name__)

    def fit(self, X: pd.DataFrame, y=None, **_):
        if self._columns:
            if callable(self._columns):
                self._columns = self._columns(X)
        else:
            self._columns = self.get_column_names(X)
        self._columns_out = X.columns
        return self

    def get_column_names(self, data):
        if self._columns:
            return [x for x in self._columns if x not in self._groupby]
        return data.columns.difference(self._groupby).tolist()

    def transform(self, X: pd.DataFrame):
        # the copy leaves the original dataframe intact
        data = deepcopy(X)
        data[self._columns] = \
                data[self._columns].fillna(data.groupby(self._groupby)[self._columns].transform('mean'))
        return data

    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        params['grouping_ids'] = self._groupby
        return params
    

class ReplaceByMedianGrouped(ReplaceByMeanGrouped):
    """  
    Using this method, all the missing values for given or all columns (except grouping_ids)\
    are replaced with the median of the group of the training dataset.
    For example, if the value of heart_beat_rate was measured every one hour \
    except at 2:00. The missing value then will be replaced by the median of \
    all measured values of the patient.
    """
    def transform(self, X: pd.DataFrame):
        # the copy leaves the original dataframe intact
        data = deepcopy(X)
        data[self._columns] = \
                data[self._columns].fillna(data.groupby(self._groupby)[self._columns].transform('median'))
        return data


class ReplaceByPreviousAndNextValue(BaseMissingValueHandling):
    """
    Using this method, all the missing values for given or all parameters
    are replaced with the previous or next value in the data events of the
    patient.
    For example, if the value of heart_beat_rate was measured every one hour
    except at 2:00. The missing value then will be replaced by the value
    measured at 1:00.
    Note: If both variables "replaceByPrevious" and "replaceByNext",
    are set to True it priors the previous value
    """
    def __init__(self, grouping_ids: list[str] | str,
                 time_column: str,  columns: list[str] | None = None,
                 replaceByPrevious: bool = True,
                 replaceByNext: bool = True, **kwargs):
        super().__init__(columns=columns, **kwargs)
        self._groupby = grouping_ids
        self._time_column = time_column
        self._replace_by_previous = replaceByPrevious
        self._replace_by_next = replaceByNext
        _logger.info('\nCreated object of ReplaceWithPreviousAndNextValue')

    def get_column_names(self, data):
        return self._columns if self._columns else data.columns.difference(self._groupby).tolist()

    def fit(self, X: pd.DataFrame, y=None, **_):
        _logger.info("This Algorithm treats train and test data equally.")
        if callable(self._columns):
            self._columns = self._columns(X)
        self._columns_out = X.columns
        return self

    def transform(self, X: pd.DataFrame):
        _logger.info('Note: If both variables "replaceByPrevious" and %s %s',
                     '"replaceByNext"',
                     'are set to True it priors the previous value')
        data = deepcopy(X)
        data = data.sort_values(self._time_column)
        features = self.get_column_names(data)

        if self._replace_by_previous:
            data[features] = data[features].fillna(
                data.groupby(self._groupby)[features].ffill())
        if self._replace_by_next:
            data[features] = data[features].fillna(
                data.groupby(self._groupby)[features].bfill())
        return data.sort_index()

    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        params['grouping_ids'] = self._groupby
        params['time_column'] = self._time_column
        params['replaceByPrevious'] = self._replace_by_previous
        params['replaceByNext'] = self._replace_by_next
        return params

class DropColumnsWithMissingRatio(BaseMissingValueHandling):
    """
    Using this method, the entire columns with the missing values more than a
    given ratio are removed from the database.
    """
    def __init__(self, columns: list[str] | None = None,
                 ratio: float = 0.2, **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        self._columns_to_drop = []
        self._ratio = ratio
        _logger.info('\nCreated object of DropColumnsWithMissingRatio')

    def fit(self, X: pd.DataFrame, y=None, **_):
        if callable(self._columns):
            self._columns = self._columns(X)
        features = self.get_column_names(X)
        ratio_dict = dict(X[features].isna().sum()/len(X))
        self._columns_to_drop = self._get_columns_to_drop(ratio_dict,
                                                          self._ratio)
        self._columns_out = X.columns.difference(self._columns_to_drop)
        return self

    def transform(self, X: pd.DataFrame):
        return X.drop(columns=self._columns_to_drop)

    def _get_columns_to_drop(self, ratio_dict, ratio):
        columns_to_drop = []
        for column in ratio_dict:
            if ratio_dict[column] > ratio:
                columns_to_drop.append(column)
        return columns_to_drop

    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        params['ratio'] = self._ratio
        return params


class DropSubjectWithMissingRatio(BaseMissingValueHandling):
    """
    Using this method, a subject with missing data for more than a given ratio
    are removed from the dataset.
    """
    def __init__(self,
                 grouping_ids: list[str] | str,
                 columns: list[str] | None = None,
                 ratio: float = 0.5, **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        self._groupby = grouping_ids
        self._ratio = ratio
        _logger.info('\nCreated object of DropSubjectWithMissingRatio')

    def fit(self, X: pd.DataFrame, y=None, **_):
        if callable(self._columns):
            self._columns = self._columns(X)
        _logger.warning("This Algorithm treats train and test data equally.")
        self._columns_out = X.columns
        return self
    
    def get_column_names(self, data):
        if self._columns:
            return [x for x in self._columns if x not in self._groupby]
        return data.columns.difference(self._groupby).tolist()

    def _get_patients_to_keep(self, data: pd.DataFrame):
        features = self.get_column_names(data)
        groups = data.groupby(self._groupby)[features]
        df_ratio = (groups.count().sum(axis=1)) / (len(features) *
                                                   groups.size())
        return df_ratio[df_ratio > self._ratio].reset_index()[self._groupby]

    def transform(self, X: pd.DataFrame):
        patients_to_keep = self._get_patients_to_keep(X)
        return pd.merge(patients_to_keep, X, on=self._groupby)

    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        params['ratio'] = self._ratio
        params['grouping_ids'] = self._groupby
        return params


class ReplaceByNormalValue(BaseMissingValueHandling):
    """
    Using this method, all the missing values for given 'columns'
    are replaced with the given 'values'.
    """
    def __init__(self, columns: list[str] | None = None,
                 fill_value: Any | None = None,
                 **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns, **kwargs)
        kwargs['strategy'] = 'constant'
        kwargs['fill_value'] = fill_value
        self._imputer = impute.SimpleImputer(**kwargs)
        _logger.info('\nCreated object of ReplaceWithMostFrequent')


class Iterative_Imputer(BaseMissingValueHandling):
    """
    Wrapper fo the Iterative Imputer method
    """
    # The wrapper should have the same signature as the original method to
    # avoid any issues in the frontend.
    __doc__ = inspect.getdoc(impute.IterativeImputer)
    __signature__ = inspect.signature(impute.IterativeImputer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default="None",
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(impute.IterativeImputer).parameters.values())
        )

    def __init__(self, columns: list[str] | None = None,
                 **kwargs):
        """
        Iterative Imputer method
        """
        super().__init__(columns=columns)
        self._imputer = impute.IterativeImputer(**kwargs)
        _logger.info('\nCreated object of Iterative_Imputer')
        # https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html


class KNNImputer(BaseMissingValueHandling):
    """
    Wrapper fo the KNNImputer method
    """

    # The wrapper should have the same signature as the original method to
    # avoid any issues in the frontend
    __doc__ = inspect.getdoc(impute.KNNImputer)
    __signature__ = inspect.signature(impute.KNNImputer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default="None",
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(impute.KNNImputer).parameters.values())
        )

    def __init__(self, columns: list[str] | None = None,
                 **kwargs):
        """
        Initializing the class
        """
        super().__init__(columns=columns)
        self._imputer = impute.KNNImputer(**kwargs)
        _logger.info('\nCreated object of KNNImputer')
        # https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html
