""" Copyright (c) Fraunhofer MEVIS,
Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Encoders.py
authors: Elham Taghizadeh,
Melissa Finster,
Johannes Bunk
date: 10/2023
description: The available Encoders in the repository
-----------------------------------------------------------------------------
"""
import logging
import inspect
from collections.abc import Callable
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import (
            OneHotEncoder, StandardScaler, Binarizer,
            MaxAbsScaler, 
            MinMaxScaler, Normalizer, OrdinalEncoder,
            PolynomialFeatures, PowerTransformer,
            QuantileTransformer, RobustScaler, SplineTransformer,
            TargetEncoder
        )
from methods_repository.config_models import DataTypes, ProgrammingLanguages


_logger = logging.getLogger(__name__)


_IMPORT_THIS = "methods_repository.Encoders.Encoders"
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        'OneHotEncoder': {
            'import': _IMPORT_THIS,
            'name': 'OneHotEncoder_mlkitchen',
            'flags': [DataTypes.categorical]
        },
       'OrdinalEncoder': {
            'import': _IMPORT_THIS,
            'name': 'OrdinalEncoder_mlkitchen',
            'flags': [DataTypes.categorical]
        },
        'StandardScaler': {
            'import': _IMPORT_THIS,
            'name': 'StandardScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'Binarizer': {
            'import': _IMPORT_THIS,
            'name': 'Binarizer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'MaxAbsScaler': {
            'import': _IMPORT_THIS,
            'name': 'MaxAbsScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'MinMaxScaler': {
            'import': _IMPORT_THIS,
            'name': 'MinMaxScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'Normalizer': {
            'import': _IMPORT_THIS,
            'name': 'Normalizer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'PolynomialFeatures': {
            'import': _IMPORT_THIS,
            'name': 'PolynomialFeatures_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'PowerTransformer': {
            'import': _IMPORT_THIS,
            'name': 'PowerTransformer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'QuantileTransformer': {
            'import': _IMPORT_THIS,
            'name': 'QuantileTransformer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'RobustScaler': {
            'import': _IMPORT_THIS,
            'name': 'RobustScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'SplineTransformer': {
            'import': _IMPORT_THIS,
            'name': 'SplineTransformer_mlkitchen',
            'flags': [DataTypes.numerical]
        },

        'GroupedStandardScaler': {
            'import': _IMPORT_THIS,
            'name': 'GroupedStandardScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedMaxAbsScaler': {
            'import': _IMPORT_THIS,
            'name': 'GroupedMaxAbsScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedMinMaxScaler': {
            'import': _IMPORT_THIS,
            'name': 'GroupedMinMaxScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedNormalizer': {
            'import': _IMPORT_THIS,
            'name': 'GroupedNormalizer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedPowerTransformer': {
            'import': _IMPORT_THIS,
            'name': 'GroupedPowerTransformer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedQuantileTransformer': {
            'import': _IMPORT_THIS,
            'name': 'GroupedQuantileTransformer_mlkitchen',
            'flags': [DataTypes.numerical]
        },
        'GroupedRobustScaler': {
            'import': _IMPORT_THIS,
            'name': 'GroupedRobustScaler_mlkitchen',
            'flags': [DataTypes.numerical]
        }
    },
    ProgrammingLanguages.R: {
    }
}


class BaseWrapper(BaseEstimator, TransformerMixin):
    _encoder_type = TransformerMixin

    def __init__(self, columns=None, **kwargs):
        self.columns = columns
        self._encoder = self._encoder_type(**kwargs)
        self._encoder.set_output(transform='pandas')

    def fit(self, X, y=None, **kwargs):
        if self.columns:
            if callable(self.columns):
                self.columns = self.columns(X)
            else:
                self.columns = [column for column in self.columns if column in X.columns]
                
            self._encoder = self._encoder.fit(X[self.columns], y, **kwargs)
            self._features_not_changed = X.columns.difference(self.columns)
            self._features_out = list(self._encoder.get_feature_names_out()) + list(self._features_not_changed)
        else:
            self._encoder = self._encoder.fit(X, y, **kwargs)
            self._features_not_changed = []
            self._features_out = self._encoder.get_feature_names_out()
        return self

    def transform(self, X, **kwargs):
        if self.columns:
            Xs = self._encoder.transform(X[self.columns], **kwargs)
            Xs[self._features_not_changed] = X[self._features_not_changed]
        else:
            Xs = self._encoder.transform(X, **kwargs)
        return Xs

    def get_feature_names_out(self, input_features=None):
        return self._features_out

    def get_params(self, deep=True):
        out = self._encoder.get_params(deep=deep)
        out['columns'] = self.columns
        return out


class OneHotEncoder_mlkitchen(BaseWrapper):
    """Encode categorical features as a one-hot numeric array.

The features are encoded using a one-hot (aka 'one-of-K' or 'dummy')
encoding scheme. This creates a binary column for each category and
returns an array.

By default, the encoder derives the categories based on the unique values
in each feature. Alternatively, you can also specify the `categories`
manually.

This encoding is needed for feeding categorical data to many scikit-learn
estimators, notably linear models and SVMs with the standard kernels.

Read more in the :ref:`User Guide <preprocessing_categorical_features>`.
For a comparison of different encoders, refer to:
:ref:`sphx_glr_auto_examples_preprocessing_plot_target_encoder.py`.

Parameters
----------

drop : {'first', 'if_binary'},
    default=None
    Specifies a methodology to use to drop one of the categories per
    feature. This is useful in situations where perfectly collinear
    features cause problems, such as when feeding the resulting data
    into an unregularized linear regression model.

    However, dropping one category breaks the symmetry of the original
    representation and can therefore induce a bias in downstream models,
    for instance for penalized linear classification or regression models.

    - None : retain all features (the default).
    - 'first' : drop the first category in each feature. If only one
      category is present, the feature will be dropped entirely.
    - 'if_binary' : drop the first category in each feature with two
      categories. Features with 1 or more than 2 categories are
      left intact.

    When `max_categories` or `min_frequency` is configured to group
    infrequent categories, the dropping behavior is handled after the
    grouping.


handle_unknown : {'error', 'ignore', 'infrequent_if_exist'},
    default='error'
    Specifies the way unknown categories are handled during :meth:`transform`.

    - 'error' : Raise an error if an unknown category is present during transform.
    - 'ignore' : When an unknown category is encountered during
      transform, the resulting one-hot encoded columns for this feature
      will be all zeros. In the inverse transform, an unknown category
      will be denoted as None.
    - 'infrequent_if_exist' : When an unknown category is encountered
      during transform, the resulting one-hot encoded columns for this
      feature will map to the infrequent category if it exists. The
      infrequent category will be mapped to the last position in the
      encoding. During inverse transform, an unknown category will be
      mapped to the category denoted `'infrequent'` if it exists. If the
      `'infrequent'` category does not exist, then :meth:`transform` and
      :meth:`inverse_transform` will handle an unknown category as with
      `handle_unknown='ignore'`. Infrequent categories exist based on
      `min_frequency` and `max_categories`. Read more in the
      :ref:`User Guide <encoder_infrequent_categories>`.


min_frequency : int or float, default=None
    Specifies the minimum frequency below which a category will be
    considered infrequent.

    - If `int`, categories with a smaller cardinality will be considered
      infrequent.

    - If `float`, categories with a smaller cardinality than
      `min_frequency * n_samples`  will be considered infrequent.


max_categories: int, default=None
    Specifies an upper limit to the number of output features for each input
    feature when considering infrequent categories. If there are infrequent
    categories, `max_categories` includes the category representing the
    infrequent categories along with the frequent categories. If `None`,
    there is no limit to the number of output features.


feature_name_combiner : "concat" or callable, default="concat"
    Callable with signature `def callable(input_feature, category)` that returns a
    string. This is used to create feature names to be returned by
    :meth:`get_feature_names_out`.

    `"concat"` concatenates encoded feature name and category with
    `feature + "_" + str(category)`.E.g. feature X with values 1, 6, 7 create
    feature names `X_1, X_6, X_7`.


See Also
--------
OrdinalEncoder : Performs an ordinal (integer)
  encoding of the categorical features.
TargetEncoder : Encodes categorical features using the target.
sklearn.feature_extraction.DictVectorizer : Performs a one-hot encoding of
  dictionary items (also handles string-valued features).
sklearn.feature_extraction.FeatureHasher : Performs an approximate one-hot
  encoding of dictionary items or strings.
LabelBinarizer : Binarizes labels in a one-vs-all
  fashion.
MultiLabelBinarizer : Transforms between iterable of
  iterables and a multilabel format, e.g. a (samples x classes) binary
  matrix indicating the presence of a class label.
    """
    __signature__ = inspect.signature(OneHotEncoder).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   [param for param in inspect.signature(OneHotEncoder).parameters.values()
                                if param.name not in {'sparse', 'sparse_output', 'categories'}]
                )
    _encoder_type = OneHotEncoder
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        kwargs['sparse_output'] = False
        kwargs['categories'] = 'auto'
        super().__init__(columns, **kwargs)


class StandardScaler_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(StandardScaler)
    __signature__ = inspect.signature(StandardScaler).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(StandardScaler).parameters.values())
        )
    _encoder_type = StandardScaler
    _parameter_constraints = _encoder_type._parameter_constraints


class Binarizer_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(Binarizer)
    __signature__ = inspect.signature(Binarizer).replace(
        parameters=[inspect.Parameter('keys',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(Binarizer).parameters.values())
        )
    _encoder_type = Binarizer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)

class MaxAbsScaler_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(MaxAbsScaler)
    __signature__ = inspect.signature(MaxAbsScaler).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(MaxAbsScaler).parameters.values())
        )
    _encoder_type = MaxAbsScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class MinMaxScaler_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(MinMaxScaler)
    __signature__ = inspect.signature(MinMaxScaler).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(MinMaxScaler).parameters.values())
        )
    _encoder_type = MinMaxScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class Normalizer_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(Normalizer)
    __signature__ = inspect.signature(Normalizer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(Normalizer).parameters.values())
        )
    _encoder_type = Normalizer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class OrdinalEncoder_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(OrdinalEncoder)
    __signature__ = inspect.signature(OrdinalEncoder).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(OrdinalEncoder).parameters.values())
        )
    _encoder_type = OrdinalEncoder
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class PolynomialFeatures_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(PolynomialFeatures)
    __signature__ = inspect.signature(PolynomialFeatures).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(PolynomialFeatures).parameters.values())
        )
    _encoder_type = PolynomialFeatures
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class PowerTransformer_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(PowerTransformer)
    __signature__ = inspect.signature(PowerTransformer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(PowerTransformer).parameters.values())
        )
    _encoder_type = PowerTransformer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class QuantileTransformer_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(QuantileTransformer)
    __signature__ = inspect.signature(QuantileTransformer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(QuantileTransformer).parameters.values())
        )
    _encoder_type = QuantileTransformer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class RobustScaler_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(RobustScaler)
    __signature__ = inspect.signature(RobustScaler).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(RobustScaler).parameters.values())
        )
    _encoder_type = RobustScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class SplineTransformer_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(SplineTransformer)
    __signature__ = inspect.signature(SplineTransformer).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(SplineTransformer).parameters.values())
        )
    _encoder_type = SplineTransformer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class TargetEncoder_mlkitchen(BaseWrapper):
    __doc__ = inspect.getdoc(TargetEncoder)
    __signature__ = inspect.signature(TargetEncoder).replace(
        parameters=[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(TargetEncoder).parameters.values())
        )
    _encoder_type = TargetEncoder
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(columns=columns, **kwargs)


class BaseWrapperGrouped(BaseEstimator, TransformerMixin):
    _encoder_type = None  #initated by child class

    def __init__(self, group_key:list[str], columns=None, **kwargs):
        self.columns = columns
        self.group_key = group_key
        self.kwargs = kwargs
        self._encoder = {}

    def group_data(self, X):
        if not self.group_key:
            raise ValueError('group_key is none')
        if len(self.group_key) == 1:
            return X.groupby(self.group_key[0])
        return X.groupby(self.group_key)
    
    def set_columns(self, X):
        if self.columns:
            if callable(self.columns):
                return self.columns(X)
            return [column for column in self.columns if column in X.columns]
        return self.columns
    
    def get_features_not_changed(self, X):
        if self.columns:
            return list(X.columns.difference(self.columns))
    
    def get_encoder(self, **kwargs):
        if self._encoder_type is None:
            raise NotImplementedError("Encoder type has not been specified in the subclass")
        encoder = self._encoder_type(**kwargs)
        return encoder

    def fit(self, X, y=None, **kwargs):
        self.columns = self.set_columns(X)
        grouped = self.group_data(X)

        for name, group in grouped:
            encoder = self.get_encoder(**self.kwargs)
            if self.columns:
                self._encoder[name] = encoder.fit(group[self.columns], y)
            else:
                self._encoder[name] = encoder.fit(group, y)
        return self

    def transform(self, X):
        X_transformed = X.copy()
        grouped_data = self.group_data(X)
        for name, group in grouped_data:
            encoder = self._encoder.get(name)
            if encoder and self.columns:
                X_transformed.loc[group.index, self.columns] = encoder.transform(group[self.columns])
            elif encoder:
                X_transformed.loc[group.index, :] = encoder.transform(group)
        return X_transformed
    
    def get_params(self, deep=True):
        params = super().get_params(deep=deep)
        params['group_key'] = self.group_key
        params['columns'] = self.columns
        params.update(self.kwargs)
        return params


class GroupedStandardScaler_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(StandardScaler)
    __signature__ = inspect.signature(StandardScaler).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                    [inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(StandardScaler).parameters.values())
        )
    _encoder_type = StandardScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedMaxAbsScaler_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(MaxAbsScaler)
    __signature__ = inspect.signature(MaxAbsScaler).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                    [inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(MaxAbsScaler).parameters.values())
        )
    _encoder_type = MaxAbsScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedMinMaxScaler_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(MinMaxScaler)
    __signature__ = inspect.signature(MinMaxScaler).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                    [inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(MinMaxScaler).parameters.values())
        )
    _encoder_type = MinMaxScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedNormalizer_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(Normalizer)
    __signature__ = inspect.signature(Normalizer).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                    [inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(Normalizer).parameters.values())
        )
    _encoder_type = Normalizer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedPowerTransformer_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(PowerTransformer)
    __signature__ = inspect.signature(PowerTransformer).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
					[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(PowerTransformer).parameters.values())
        )
    _encoder_type = PowerTransformer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedQuantileTransformer_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(QuantileTransformer)
    __signature__ = inspect.signature(QuantileTransformer).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
					[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(QuantileTransformer).parameters.values())
        )
    _encoder_type = QuantileTransformer
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedRobustScaler_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(RobustScaler)
    __signature__ = inspect.signature(RobustScaler).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
					[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(RobustScaler).parameters.values())
        )
    _encoder_type = RobustScaler
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)


class GroupedTargetEncoder_mlkitchen(BaseWrapperGrouped):
    __doc__ = inspect.getdoc(TargetEncoder)
    __signature__ = inspect.signature(TargetEncoder).replace(
        parameters=[inspect.Parameter('group_key',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
					[inspect.Parameter('columns',
                                      kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      default=None,
                                      annotation=(list[str]|None))
                    ] + \
                   list(inspect.signature(TargetEncoder).parameters.values())
        )
    _encoder_type = TargetEncoder
    _parameter_constraints = _encoder_type._parameter_constraints

    def __init__(self, group_key: list[str], columns: list[str] | Callable | None = None,
                 **kwargs) -> None:
        super().__init__(group_key=group_key, columns=columns, **kwargs)
