""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: DataSplitting.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The available methods for DataSplitting
-----------------------------------------------------------------------------
"""

from abc import ABC, abstractmethod
import logging
from pandas import DataFrame, Series
from sklearn import model_selection
from methods_repository.config_models import ProgrammingLanguages
_logger = logging.getLogger(__name__)


_IMPORT_THIS = "methods_repository.DataSplitting.DataSplitting"

List_of_Algorithms = {
    ProgrammingLanguages.Python: {

        "KFold": {
            "import": _IMPORT_THIS,
            "name": "KFold"
        },

        "LeaveOneOut": {
            "import": _IMPORT_THIS,
            "name": "LeaveOneOut"
        },
        "LeavePOut": {
            "import": _IMPORT_THIS,
            "name": "LeavePOut"
        },
        "ShuffleSplit": {
            "import": _IMPORT_THIS,
            "name": "ShuffleSplit"
        },

        "StratifiedShuffleSplit": {
            "import": _IMPORT_THIS,
            "name": "StratifiedShuffleSplit"
        },
        "StratifiedGroupKFold": {
            "import": _IMPORT_THIS,
            "name": "StratifiedGroupKFold"
        },
        "GroupShuffleSplit": {
            "import": _IMPORT_THIS,
            "name": "GroupShuffleSplit"
        },
    },
    ProgrammingLanguages.R: {}
}


class BaseDataSplitting(ABC):
    def __init__(self, n_splits: int = None,
                 target_col: str = None) -> None:
        super().__init__()
        self._n_splits = n_splits
        self._target_col = target_col

    @abstractmethod
    def split(self, data: DataFrame):
        raise NotImplementedError()


class KFold(BaseDataSplitting):
    """
        Uses the KFold class of sklearn.model_selection to split the data.
        In the first step, the test data is randomly selected from the dataset,
        using StratifiedShuffleSplit or ShuffleSplit, depending on if the
        target_col is given or not. Then the rest of the data is split to Train
        and validation in "k" folds. The output is a list of size "k".
        Each member of the list contains the "TRAINING", "VALIDATION",
        and "TEST" indices of the given fold.

        @data: The input data that should be split.

        @k: Number of folds. Default value is 5.

        @target_col: is a string, the name of the column in data that contains
        the target data. If the target_col is given, StratifiedShuffleSplit is
        used to select the "TEST" data. Otherwise, ShuffleSplit is used.

        @test_size: The ratio of samples (as a float number between 0 and 1) that should be
        selected at random for "TEST". The default value is 1/(k+1).

        :output: A list of Pandas.Series with a length of "k".
        Each of Series contain the indices of "TRAINING",
        "VALIDATION" and "TEST" indices of the given fold.
        Hint: The "TEST" indices would be the same for all folds.
    """
    def __init__(self, n_splits: int = 5, target_col: str = None,
                 test_size: float = None) -> None:
        super().__init__(n_splits, target_col)
        self._test_size = test_size

    def split(self, data: DataFrame) -> list[Series]:
        if not self._test_size:
            test_size = 1 / (self._n_splits+1)
        else:
            test_size = self._test_size

        if self._target_col:
            X = data.drop(columns=self._target_col)
            y = data[self._target_col]
            splitter_test = model_selection.StratifiedShuffleSplit(
                                    n_splits=1,
                                    test_size=test_size).split(X, y)
        else:
            splitter_test = model_selection.ShuffleSplit(n_splits=1,
                                                         test_size=test_size
                                                         ).split(data)
        result = []
        for train, test_ind in splitter_test:
            splitter_train = model_selection.KFold(n_splits=self._n_splits)
            for _, validation_ind in \
                    splitter_train.split(train):
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result


class LeavePOut(BaseDataSplitting):
    """
    Uses the LeaveOneOut class of sklearn.model_selection to split the
    data. In the first step, the test data is randomly selected from the
    dataset, using StratifiedShuffleSplit or ShuffleSplit, depending on if
    the target_col is given or not. Then the rest of the data is split to
    train and validation in leave one out manner. The output is a list
    with a length of data minus number of test samples. Each member of the
    list contains the "TRAINING", "VALIDATION", and "TEST" indices of the
    given fold.

    This cross-validation method can be computationally, very expensive.
    For large datasets, consider using other methods such as k_fold,
    stratified_k_fold or shuffle_split.

    @data: The input data that should be split.

    @p: number of samples that should be left out at each fold. Default = 2

    @target_col: is a string, the name of the column in data that contains
    the target data. If the target_col is given, StratifiedShuffleSplit is
    used to select the "TEST" data. Otherwise, ShuffleSplit is used.

    @test_size: The ratio of samples (as a float number between 0 and 1) that should be
    selected at random for "TEST". The default value is 0.1.

    :output: A list of Pandas.Series.Each of these Series contain the
    indices of "TRAINING", "VALIDATION" and "TEST" indices of the given
    fold.

    Hint: The "TEST" indices would be the same for all folds.
    """
    def __init__(self, p: int = 2, n_splits: int = None,
                 target_col: str = None,
                 test_size: float = 0.1) -> None:
        super().__init__(n_splits, target_col)
        self._p = p
        self._test_size = test_size

    def split(self, data: DataFrame) -> list[Series]:
        if self._target_col:
            X = data.drop(columns=self._target_col)
            y = data[self._target_col]
            splitter_test = model_selection.StratifiedShuffleSplit(
                                    n_splits=1,
                                    test_size=self._test_size).split(X, y)
        else:
            splitter_test = model_selection.ShuffleSplit(
                                                n_splits=1,
                                                test_size=self._test_size
                                                         ).split(data)
        result = []
        for train, test_ind in splitter_test:
            splitter_train = model_selection.LeavePOut(p=self._p)
            for n, (_, validation_ind) in \
                    enumerate(splitter_train.split(train)):
                if self._n_splits and n >= self._n_splits:
                    break
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result


class LeaveOneOut(LeavePOut):
    """
    Uses the LeaveOneOut class of sklearn.model_selection to split the
    data. In the first step, the test data is randomly selected from the
    dataset,
    using StratifiedShuffleSplit or ShuffleSplit, depending on if the
    target_col is given or not. Then the rest of the data is split to train
    and validation in leave one out manner. The output is a list with a
    length of data minus number of test samples. Each member of the list
    contains the "TRAINING", "VALIDATION", and "TEST" indices of the given
    split.

    This cross-validation method can be computationally, very expensive.
    For large datasets, consider using other methods such as k_fold,
    stratified_k_fold or shuffle_split.

    @data: The input data that should be split.

    @target_col: is a string, the name of the column in data that contains
    the target data. If the target_col is given, StratifiedShuffleSplit is
    used to select the "TEST" data. Otherwise, ShuffleSplit is used.

    @test_size: The ratio of samples (as a float number between 0 and 1) that should be
    selected at random for "TEST". The default value is 0.1.

    :output: A list of Pandas.Series with a length of len(10) - test_size.
    Each of Series contain the indices of "TRAINING",
    "VALIDATION" and "TEST" indices of the given fold.
    Hint: LeaveOneOut would have the same result as LeavePOut, when p=1.
    Hint: The "TEST" indices would be the same for all folds.
    """
    def __init__(self, n_splits: int = None,
                 target_col: str = None, test_size: float = 0.1) -> None:
        super().__init__(p=1, n_splits=n_splits,
                         target_col=target_col, test_size=test_size)


class ShuffleSplit(BaseDataSplitting):
    """
    Uses the ShuffleSplit class of sklearn.model_selection to split the
    data. The output is a pandas.Series containing the "TRAINING",
    "VALIDATION", and "TEST" indices of the split.

    @data: The input data that should be split.

    @validation_size: The ratio of validation size, Default value is 0.2
    
    @test_size: The ratio of test size, Default value is 0.2

    @n_splits: how many times the spliting should be repeated. Default=1

    :output: A list of Pandas.Series containing the indices of "TRAINING",
    "VALIDATION" and "TEST" indices of the given fold. The length of the
    list is equal to n_splits.

    Hint: The "TEST" indices would be the same for all folds.
    """
    def __init__(self, n_splits: int = 1,
                 validation_size: float = 0.2,
                 test_size: float = 0.2) -> None:
        super().__init__(n_splits)
        if validation_size > 1 or test_size > 1:
            train_size = 100 - validation_size - test_size
        else:
            train_size = 1 - validation_size - test_size
        self._ratio = [train_size, validation_size, test_size]

    def split(self, data: DataFrame) -> list[Series]:
        sum_ratio = sum(self._ratio)
        ratio = [r/sum_ratio for r in self._ratio]
        ratio[0] /= (ratio[0] + ratio[1])
        ratio[1] = 1 - ratio[0]
        splitter_test = model_selection.ShuffleSplit(n_splits=1,
                                                     test_size=ratio[2])
        result = []
        for train, test_ind in splitter_test.split(data):
            splitter_train = model_selection.ShuffleSplit(
                                    n_splits=self._n_splits,
                                    test_size=ratio[1])
            for _, validation_ind in \
                    splitter_train.split(train):
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result


class StratifiedShuffleSplit(ShuffleSplit):
    """
    Uses the StratifiedShuffleSplit class of sklearn.model_selection to
    split the data. The output is a pandas.Series containing the
    "TRAINING", "VALIDATION", and "TEST" indices of the split.

    @validation_size: The ratio of validation size, Default value is 0.2
    @test_size: The ratio of test size, Default value is 0.2

    @n_splits: how many times the spliting should be repeated. Default=1

    :output: A list of Pandas.Series containing the indices of "TRAINING",
    "VALIDATION" and "TEST" indices of the given fold. The length of the
    list is equal to n_splits.

    Hint: The "TEST" indices would be the same for all folds.
    """
    def __init__(self, target_col: str, n_splits: int = 1,
                 validation_size: float = 0.2,
                 test_size: float = 0.2) -> None:
        super().__init__(n_splits, validation_size=validation_size, test_size=test_size)
        self._target_col = target_col

    def split(self, data: DataFrame) -> list[Series]:
        sum_ratio = sum(self._ratio)
        ratio = [r/sum_ratio for r in self._ratio]
        ratio[0] /= (ratio[0] + ratio[1])
        ratio[1] = 1 - ratio[0]
        splitter_test = model_selection.StratifiedShuffleSplit(
                                            n_splits=1,
                                            test_size=ratio[2])
        result = []
        y = data[self._target_col]
        X = data.drop(columns=self._target_col)

        for train, test_ind in splitter_test.split(X, y,):
            splitter_train = model_selection.StratifiedShuffleSplit(
                                    n_splits=self._n_splits,
                                    test_size=ratio[1])
            for _, validation_ind in \
                    splitter_train.split(
                        X.iloc[train],
                        y.iloc[train]):
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result
    

class StratifiedGroupKFold(BaseDataSplitting):
    """
    Stratified Group K-Folds cross-validator.
    Provides train/validation/test indices to split data.
    It is a variation of GroupKFold, which returns stratified folds, based on the given target column and group column.
    The folds are made by preserving the percentage of samples for each class.
    The output is a pandas.Series containing the "TRAINING", "VALIDATION", and "TEST" indices of the split.
    
    @n_splits: Number of folds. Default value is 5.
    @group: The column name of the groups in the data.
    @target_col: The column name of the target variable in the data.
    @test_size: The ratio of samples (as a float number between 0 and 1) that should be selected at random for "TEST". The default value is 1/(k+1).
    """
    def __init__(self, group: str, n_splits: int = 5, 
                 target_col: str = None,
                 test_size: float = None) -> None:
        super().__init__(n_splits, target_col)
        self._test_size = test_size
        self._group = group      # method can also be applied without groupping

    def split(self, data: DataFrame) -> list[Series]:
        """
        Actual splitting of the data into TRAINING, VALIDATION and TEST sets.
        """
        if not self._test_size:
            test_size = 1 / (self._n_splits+1)
        else:
            test_size = self._test_size
        if self._target_col:
            y = data[self._target_col]
            X = data.drop(columns=self._target_col)
            splitter_test = model_selection.GroupShuffleSplit(n_splits=1, test_size = test_size).split(X, y,  groups = data[self._group])
        else:
            splitter_test = []
        result = []
        for train, test_ind in splitter_test:
            splitter_train = model_selection.StratifiedGroupKFold(n_splits=self._n_splits)
            for _, validation_ind in \
                    splitter_train.split(
                        X.iloc[train],
                        y.iloc[train], groups = data[self._group].iloc[train]):
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result


class GroupShuffleSplit(ShuffleSplit):
    def __init__(self, group: str, n_splits: int = 1,
                 validation_size: float = 0.2,
                 test_size: float = 0.2) -> None:
        """
        Uses the ShuffleSplit class of sklearn.model_selection to split the
        data. The output is a pandas.Series containing the "TRAINING",
        "VALIDATION", and "TEST" indices of the split.

        @data: The input data that should be split.

        @ratio: The split ratio for ["TRAINING", "VALIDATION", and "TEST"].
        Default value is [0.6, 0.2, 0.2]

        @n_splits: how many times the spliting should be repeated. Default=1

        :output: A list of Pandas.Series containing the indices of "TRAINING",
        "VALIDATION" and "TEST" indices of the given fold. The length of the
        list is equal to n_splits.

        Hint: The "TEST" indices would be the same for all folds.
        """
        super().__init__(n_splits, validation_size=validation_size, test_size=test_size)
        self._group = group

    def get_ratio(self):
        sum_ratio = sum(self._ratio)
        ratio = [r/sum_ratio for r in self._ratio]
        ratio[0] /= (ratio[0] + ratio[1])
        ratio[1] = 1 - ratio[0]
        return ratio

    def split(self, data: DataFrame) -> list[Series]:
        ratio = self.get_ratio()
        splitter_test = model_selection.GroupShuffleSplit(n_splits=1,
                                                     test_size=ratio[2])
        result = []
        for train, test_ind in splitter_test.split(data, groups= data[self._group]):
            splitter_train = model_selection.GroupShuffleSplit(
                                    n_splits=self._n_splits,
                                    test_size=ratio[1])
            for _, validation_ind in \
                    splitter_train.split(train,groups= data[self._group].iloc[train]):
                indices = Series("TRAINING", index=range(len(data)))
                indices[train[validation_ind]] = "VALIDATION"
                indices[test_ind] = "TEST"
                result.append(indices)
            break
        return result