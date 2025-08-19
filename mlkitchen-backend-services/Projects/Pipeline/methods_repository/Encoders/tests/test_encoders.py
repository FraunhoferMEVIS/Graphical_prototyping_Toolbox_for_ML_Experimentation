""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_estimators.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: The tests for the Encoders
-----------------------------------------------------------------------------
"""

import pytest
from pandas.testing import assert_frame_equal
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize('method', [
    'OneHotEncoder', 'OrdinalEncoder'])
def test_encoding_categorical_data(categorical_data,
                                   target_categorical,
                                   method):
    parameters = {'dtype': 'numpy.float32', 'drop': 'if_binary', 'sparse_output': False}
    encoder = ModuleFinder.use_method('Encoders', method, **parameters)
    encoder.fit(categorical_data, target_categorical['target'])
    encoder.transform(categorical_data)


@pytest.mark.parametrize('method', [
    'StandardScaler', 'Binarizer', 'MaxAbsScaler', 
    'MinMaxScaler', 'Normalizer', 'PolynomialFeatures', 'PowerTransformer',
    'QuantileTransformer', 'RobustScaler', 'SplineTransformer'])
def test_encoding_numerical_data(numerical_data, method):
    for encoding in ('onehot', 'onehot-dense'):
        parameters = {
            'encode': encoding,
            'columns': None
        }
        preprocessor = ModuleFinder.use_method('Encoders', method, **parameters)

        preprocessor = preprocessor.fit(numerical_data.data)
        preprocessor.transform(numerical_data.data)
        

@pytest.mark.parametrize('method', ['GroupedStandardScaler'])
def test_encoding_grouped_StandardScaler(grouped_numerical_data, method):
    for encoding in ('onehot', 'onehot-dense'):
        target_data=grouped_numerical_data.copy()
        parameters = {
            'encode': encoding,
            'columns': ['value1', 'value2'],
            'group_key':['ID']
        }
        preprocessor = ModuleFinder.use_method('Encoders', method, **parameters)
        preprocessor = preprocessor.fit(grouped_numerical_data)
        transformed_data=preprocessor.transform(grouped_numerical_data)
        print('\npreprocessor:\n', transformed_data)
        target_data['value1']=[-0.11624764, 0.46499055, 1.62746694, -1.27872403,
                               -0.69748583, -0.76249285, -0.15249857, -0.76249285, 1.67748427]
        target_data['value2']=[-0.98473193, -0.98473193, -0.36927447, 0.86164044,
                               1.47709789, -1.34164079, -0.4472136, 0.4472136, 1.34164079]
        print('\ntarget_data\n', target_data)
        assert_frame_equal(transformed_data, target_data, check_dtype=False)


@pytest.mark.parametrize('method', ['GroupedStandardScaler', 'GroupedMaxAbsScaler', 'GroupedMinMaxScaler',
        'GroupedNormalizer', 'GroupedPowerTransformer', 'GroupedQuantileTransformer' ,
        'GroupedRobustScaler'])
def test_encoding_grouped_data(grouped_numerical_data, method):
    for encoding in ('onehot', 'onehot-dense'):
        parameters = {
            'encode': encoding,
            'columns': ['value1', 'value2'],
            'group_key':['ID']
        }
        preprocessor = ModuleFinder.use_method('Encoders', method, **parameters)
        preprocessor = preprocessor.fit(grouped_numerical_data)
        preprocessor.transform(grouped_numerical_data)
        