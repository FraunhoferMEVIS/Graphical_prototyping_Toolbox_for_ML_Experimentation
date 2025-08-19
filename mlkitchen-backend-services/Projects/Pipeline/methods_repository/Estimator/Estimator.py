""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Estimator.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The available Estimators in the repository
-----------------------------------------------------------------------------
"""

import inspect
import importlib
from abc import ABC, abstractmethod
import logging
import numpy as np
import tensorflow as tf
from pandas import DataFrame, Series
from numpy import ndarray
from sklearn.utils._param_validation import StrOptions
from keras.models import Sequential
from keras import layers as keras_layers, Input
from methods_repository.config_models import TaskTypes, ProgrammingLanguages
from methods_repository.abstraction import get_kernels_list, get_algorithm_list


_logger = logging.getLogger(__name__)
_IMPORT_THIS = "methods_repository.Estimator.Estimator"

List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        # ############ Regression Algorithms #############
        "AdaBoostRegressor": {
            "import": "sklearn.ensemble",
            "name": "AdaBoostRegressor",
            "flags": [TaskTypes.regression],
        },
        "BaggingRegressor": {
            "import": "sklearn.ensemble",
            "name": "BaggingRegressor",
            "flags": [TaskTypes.regression],
        },
        "ExtraTreesRegressor": {
            "import": "sklearn.ensemble",
            "name": "ExtraTreesRegressor",
            "flags": [TaskTypes.regression],
        },
        "GaussianProcessRegressor": {
            "import": "sklearn.gaussian_process",
            "name": "GaussianProcessRegressor",
            "flags": [TaskTypes.regression],
        },
        "GradientBoostingRegressor": {
            "import": "sklearn.ensemble",
            "name": "GradientBoostingRegressor",
            "flags": [TaskTypes.regression],
        },
        "HistGradientBoostingRegressor": {
            "import": "sklearn.ensemble",
            "name": "HistGradientBoostingRegressor",
            "flags": [TaskTypes.regression],
        },
        "IsotonicRegression": {
            "import": "sklearn.isotonic",
            "name": "IsotonicRegression",
            "flags": [TaskTypes.regression],
        },
        "KernelRidge": {
            "import": "sklearn.kernel_ridge",
            "name": "KernelRidge",
            "flags": [TaskTypes.regression],
        },
        "RandomForestRegressor": {
            "import": "sklearn.ensemble",
            "name": "RandomForestRegressor",
            "flags": [TaskTypes.regression],
        },
        "StackingRegressor": {
            "import": "sklearn.ensemble",
            "name": "StackingRegressor",
            "flags": [TaskTypes.regression],
        },
        "VotingRegressor": {
            "import": "sklearn.ensemble",
            "name": "VotingRegressor",
            "flags": [TaskTypes.regression],
        },
        "LinearRegression": {
            "import": "sklearn.linear_model",
            "name": "LinearRegression",
            "flags": [TaskTypes.regression],
        },
        "Ridge": {
            "import": "sklearn.linear_model",
            "name": "Ridge",
            "flags": [TaskTypes.regression],
        },
        "RidgeCV": {
            "import": "sklearn.linear_model",
            "name": "RidgeCV",
            "flags": [TaskTypes.regression],
        },
        "SGDRegressor": {
            "import": "sklearn.linear_model",
            "name": "SGDRegressor",
            "flags": [TaskTypes.regression],
        },
        "ElasticNet": {
            "import": "sklearn.linear_model",
            "name": "ElasticNet",
            "flags": [TaskTypes.regression],
        },
        "ElasticNetCV": {
            "import": "sklearn.linear_model",
            "name": "ElasticNetCV",
            "flags": [TaskTypes.regression],
        },
        "Lars": {
            "import": "sklearn.linear_model",
            "name": "Lars",
            "flags": [TaskTypes.regression],
        },
        "LarsCV": {
            "import": "sklearn.linear_model",
            "name": "LarsCV",
            "flags": [TaskTypes.regression],
        },
        "Lasso": {
            "import": "sklearn.linear_model",
            "name": "Lasso",
            "flags": [TaskTypes.regression],
        },
        "LassoCV": {
            "import": "sklearn.linear_model",
            "name": "LassoCV",
            "flags": [TaskTypes.regression],
        },
        "LassoLars": {
            "import": "sklearn.linear_model",
            "name": "LassoLars",
            "flags": [TaskTypes.regression],
        },
        "LassoLarsCV": {
            "import": "sklearn.linear_model",
            "name": "LassoLarsCV",
            "flags": [TaskTypes.regression],
        },
        "LassoLarsIC": {
            "import": "sklearn.linear_model",
            "name": "LassoLarsIC",
            "flags": [TaskTypes.regression],
        },
        "OrthogonalMatchingPursuit": {
            "import": "sklearn.linear_model",
            "name": "OrthogonalMatchingPursuit",
            "flags": [TaskTypes.regression],
        },
        "OrthogonalMatchingPursuitCV": {
            "import": "sklearn.linear_model",
            "name": "OrthogonalMatchingPursuitCV",
            "flags": [TaskTypes.regression],
        },
        "ARDRegression": {
            "import": "sklearn.linear_model",
            "name": "ARDRegression",
            "flags": [TaskTypes.regression],
        },
        "BayesianRidge": {
            "import": "sklearn.linear_model",
            "name": "BayesianRidge",
            "flags": [TaskTypes.regression],
        },
        "MultiTaskElasticNet": {
            "import": "sklearn.linear_model",
            "name": "MultiTaskElasticNet",
            "flags": [TaskTypes.regression],
        },
        "MultiTaskElasticNetCV": {
            "import": "sklearn.linear_model",
            "name": "MultiTaskElasticNetCV",
            "flags": [TaskTypes.regression],
        },
        "MultiTaskLasso": {
            "import": "sklearn.linear_model",
            "name": "MultiTaskLasso",
            "flags": [TaskTypes.regression],
        },
        "MultiTaskLassoCV": {
            "import": "sklearn.linear_model",
            "name": "MultiTaskLassoCV",
            "flags": [TaskTypes.regression],
        },
        "HuberRegressor": {
            "import": "sklearn.linear_model",
            "name": "HuberRegressor",
            "flags": [TaskTypes.regression],
        },
        "QuantileRegressor": {
            "import": "sklearn.linear_model",
            "name": "QuantileRegressor",
            "flags": [TaskTypes.regression],
        },
        "RANSACRegressor": {
            "import": "sklearn.linear_model",
            "name": "RANSACRegressor",
            "flags": [TaskTypes.regression],
        },
        "TheilSenRegressor": {
            "import": "sklearn.linear_model",
            "name": "TheilSenRegressor",
            "flags": [TaskTypes.regression],
        },
        "PoissonRegressor": {
            "import": "sklearn.linear_model",
            "name": "PoissonRegressor",
            "flags": [TaskTypes.regression],
        },
        "TweedieRegressor": {
            "import": "sklearn.linear_model",
            "name": "TweedieRegressor",
            "flags": [TaskTypes.regression],
        },
        "GammaRegressor": {
            "import": "sklearn.linear_model",
            "name": "GammaRegressor",
            "flags": [TaskTypes.regression],
        },
        "PassiveAggressiveRegressor": {
            "import": "sklearn.linear_model",
            "name": "PassiveAggressiveRegressor",
            "flags": [TaskTypes.regression],
        },
        "KNeighborsRegressor": {
            "import": "sklearn.neighbors",
            "name": "KNeighborsRegressor",
            "flags": [TaskTypes.regression],
        },
        "RadiusNeighborsRegressor": {
            "import": "sklearn.neighbors",
            "name": "RadiusNeighborsRegressor",
            "flags": [TaskTypes.regression],
        },
        "MLPRegressor": {
            "import": "sklearn.neural_network",
            "name": "MLPRegressor",
            "flags": [TaskTypes.regression],
        },
        "LinearSVR": {
            "import": "sklearn.svm",
            "name": "LinearSVR",
            "flags": [TaskTypes.regression],
        },
        "NuSVR": {
            "import": "sklearn.svm",
            "name": "NuSVR",
            "flags": [TaskTypes.regression],
            "language": ProgrammingLanguages.Python
        },
        "SVR": {
            "import": "sklearn.svm",
            "name": "SVR",
            "flags": [TaskTypes.regression],
        },
        "DecisionTreeRegressor": {
            "import": "sklearn.tree",
            "name": "DecisionTreeRegressor",
            "flags": [TaskTypes.regression],
        },
        "ExtraTreeRegressor": {
            "import": "sklearn.tree",
            "name": "ExtraTreeRegressor",
            "flags": [TaskTypes.regression],
        },
        # ############ Classification Algorithms #############
        "AdaBoostClassifier": {
            "import": "sklearn.ensemble",
            "name": "AdaBoostClassifier",
            "flags": [TaskTypes.classification],
        },
        "BaggingClassifier": {
            "import": "sklearn.ensemble",
            "name": "BaggingClassifier",
            "flags": [TaskTypes.classification],
        },
        "ExtraTreesClassifier": {
            "import": "sklearn.ensemble",
            "name": "ExtraTreesClassifier",
            "flags": [TaskTypes.classification],
        },
        "GaussianProcessClassifier": {
            "import": "sklearn.gaussian_process",
            "name": "GaussianProcessClassifier",
            "flags": [TaskTypes.classification],
        },
        "GradientBoostingClassifier": {
            "import": "sklearn.ensemble",
            "name": "GradientBoostingClassifier",
            "flags": [TaskTypes.classification],
        },
        "HistGradientBoostingClassifier": {
            "import": "sklearn.ensemble",
            "name": "HistGradientBoostingClassifier",
            "flags": [TaskTypes.classification],
        },
        "LinearDiscriminantAnalysis": {
            "import": "sklearn.discriminant_analysis",
            "name": "LinearDiscriminantAnalysis",
            "flags": [TaskTypes.classification],
        },
        "LogisticRegression": {
            "import": "sklearn.linear_model",
            "name": "LogisticRegression",
            "flags": [TaskTypes.classification],
        },
        "LogisticRegressionCV": {
            "import": "sklearn.linear_model",
            "name": "LogisticRegressionCV",
            "flags": [TaskTypes.classification],
        },
        "PassiveAggressiveClassifier": {
            "import": "sklearn.linear_model",
            "name": "PassiveAggressiveClassifier",
            "flags": [TaskTypes.classification],
        },
        "Perceptron": {
            "import": "sklearn.linear_model",
            "name": "Perceptron",
            "flags": [TaskTypes.classification],
        },
        "QuadraticDiscriminantAnalysis": {
            "import": "sklearn.discriminant_analysis",
            "name": "QuadraticDiscriminantAnalysis",
            "flags": [TaskTypes.classification],
        },
        "RandomForestClassifier": {
            "import": "sklearn.ensemble",
            "name": "RandomForestClassifier",
            "flags": [TaskTypes.classification],
        },
        "RidgeClassifier": {
            "import": "sklearn.linear_model",
            "name": "RidgeClassifier",
            "flags": [TaskTypes.classification],
        },
        "RidgeClassifierCV": {
            "import": "sklearn.linear_model",
            "name": "RidgeClassifierCV",
            "flags": [TaskTypes.classification],
        },
        "SGDClassifier": {
            "import": "sklearn.linear_model",
            "name": "SGDClassifier",
            "flags": [TaskTypes.classification],
        },
        "SGDOneClassSVM": {
            "import": "sklearn.linear_model",
            "name": "SGDOneClassSVM",
            "flags": [TaskTypes.classification],
        },
        "StackingClassifier": {
            "import": "sklearn.ensemble",
            "name": "StackingClassifier",
            "flags": [TaskTypes.classification],
        },
        "VotingClassifier": {
            "import": "sklearn.ensemble",
            "name": "VotingClassifier",
            "flags": [TaskTypes.classification],
        },
        "BernoulliNB": {
            "import": "sklearn.naive_bayes",
            "name": "BernoulliNB",
            "flags": [TaskTypes.classification],
        },
        "CategoricalNB": {
            "import": "sklearn.naive_bayes",
            "name": "CategoricalNB",
            "flags": [TaskTypes.classification],
        },
        "ComplementNB": {
            "import": "sklearn.naive_bayes",
            "name": "ComplementNB",
            "flags": [TaskTypes.classification],
        },
        "GaussianNB": {
            "import": "sklearn.naive_bayes",
            "name": "GaussianNB",
            "flags": [TaskTypes.classification],
        },
        "MultinomialNB": {
            "import": "sklearn.naive_bayes",
            "name": "MultinomialNB",
            "flags": [TaskTypes.classification],
        },
        "KNeighborsClassifier": {
            "import": "sklearn.neighbors",
            "name": "KNeighborsClassifier",
            "flags": [TaskTypes.classification],
        },
        "RadiusNeighborsClassifier": {
            "import": "sklearn.neighbors",
            "name": "RadiusNeighborsClassifier",
            "flags": [TaskTypes.classification],
        },
        "NearestCentroid": {
            "import": "sklearn.neighbors",
            "name": "NearestCentroid",
            "flags": [TaskTypes.classification],
        },
        "MLPClassifier": {
            "import": "sklearn.neural_network",
            "name": "MLPClassifier",
            "flags": [TaskTypes.classification],
        },
        "LinearSVC": {
            "import": "sklearn.svm",
            "name": "LinearSVC",
            "flags": [TaskTypes.classification],
        },
        "NuSVC": {
            "import": "sklearn.svm",
            "name": "NuSVC",
            "flags": [TaskTypes.classification],
        },
        "SVC": {
            "import": "sklearn.svm",
            "name": "SVC",
            "flags": [TaskTypes.classification],
        },
        "DecisionTreeClassifier": {
            "import": "sklearn.tree",
            "name": "DecisionTreeClassifier",
            "flags": [TaskTypes.classification],
        },
        "ExtraTreeClassifier": {
            "import": "sklearn.tree",
            "name": "ExtraTreeClassifier",
            "flags": [TaskTypes.classification],
        },        
        "EasyEnsembleClassifier": {
            "import": "imblearn.ensemble",
            "name": "EasyEnsembleClassifier",
            "flags": [TaskTypes.classification],
        },
        "RUSBoostClassifier": {
            "import": "imblearn.ensemble",
            "name": "RUSBoostClassifier",
            "flags": [TaskTypes.classification],
        },
        "BalancedBaggingClassifier": {
            "import": "imblearn.ensemble",
            "name": "BalancedBaggingClassifier",
            "flags": [TaskTypes.classification],
        },
        "BalancedRandomForestClassifier": {
            "import": "imblearn.ensemble",
            "name": "BalancedRandomForestClassifier",
            "flags": [TaskTypes.classification],
        },
        "SequentialModel": {
            "import": _IMPORT_THIS,
            "name": "SequentialModel",
            "flags": [TaskTypes.timeseries_classification],
        },
    }
}

# Kernels are needed for gaussian process estimators
List_of_Kernels = {
    ProgrammingLanguages.Python: {
        "ConstantKernel": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "ConstantKernel",
        },
        "CompoundKernel": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "CompoundKernel",
        },
        "DotProduct": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "DotProduct",
        },
        "ExpSineSquared": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "ExpSineSquared",
        },
        "Exponentiati": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "Exponentiati",
        },
        "Hyperparamet": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "Hyperparamet",
        },
        "Matern": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "Matern"
        },
        "PairwiseKernel": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "PairwiseKernel",
        },
        "Product": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "Product",
        },
        "RBF": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "RBF"
        },
        "RationalQuadrati": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "RationalQuadrati",
        },
        "Sum": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "Sum",
        },
        "WhiteKernel": {
            "import": "sklearn.gaussian_process.kernels",
            "name": "WhiteKernel",
        },
    }
}


def generate_layer_dic_keras():
    list_ = inspect.getmembers(keras_layers)
    layer_dic = {}
    for name, obj in list_:
        layer_dic[name] = {
            "import": "keras.layers",
            "name": name,
            "flag": obj,
        }
    return layer_dic

List_of_KerasLayers = { ProgrammingLanguages.Python: generate_layer_dic_keras()}


class BaseDL(ABC):

    def __init__(self, target_col: str = None, identifier:str= None, sequence_column: str = None) -> None:
        super().__init__()
        self._target_col = target_col
        self._sequence_column = sequence_column
        self._identifier = identifier
        self.number_sequences = None
        self.number_features = None
        
        self._parameter_constraints = {
            "target_col": [str],
            "identifier": [str],
            "sequence_column": [str],
        }

    @abstractmethod
    def fit(self, X:DataFrame, y: DataFrame):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, X: ndarray):
        raise NotImplementedError()

    @abstractmethod
    def build_model(self, shape: tuple):
        raise NotImplementedError()
    
    @abstractmethod
    def score(self, X:DataFrame, y: DataFrame):
        raise NotImplementedError()
    
    def get_params(self, deep=True):
        params = vars(self).copy() 
        if deep:
            for attr, value in params.items():
                if hasattr(value, 'get_params'):
                    params[attr] = value.get_params(deep=True)
        return params
    
    def drop_keys(self, X:DataFrame):
        return X.drop(columns=[self._identifier, self._sequence_column])
    
    def get_len_sequence(self, X:DataFrame):
        return len(X[self._sequence_column].unique())
    
    def get_number_features(self, X:DataFrame):
        return len(X.columns) - 2 #identifier, sequence
    
    def get_number_patients(self, X:DataFrame):
        return int(len(X)/ self.number_sequences)

    def reshape_data_to_tensor(self, X:DataFrame, y:DataFrame):
        return self.reshape_X_to_tensor(X), self.reshape_y_to_tensor(y)
    
    def reshape_y_to_tensor(self, y:DataFrame):
        number_patients=self.get_number_patients(y)
        if isinstance(y,ndarray):
            y = y[::self.number_sequences].reshape(number_patients ,1 ,1)
        else:
            y = y[::self.number_sequences].values.reshape(number_patients ,1 ,1)
        return tf.convert_to_tensor(y, dtype_hint=tf.int64)
    
    def inflate_y(self, array : ndarray):
        repeated_array=np.repeat(array, self.number_sequences)
        return Series(repeated_array)
    
    def reshape_X_to_tensor(self, X:DataFrame):
        number_patients=self.get_number_patients(X)
        X = self.drop_keys(X)
        X = np.array(X.values).reshape((number_patients, self.number_sequences, self.number_features))
        return tf.convert_to_tensor(X, dtype_hint=tf.float32)
    
    def array_to_dataframe(self, array: ndarray):
        return DataFrame(array)

class SequentialModel(BaseDL):    
    def __init__(self,
                    target_col: str=None,
                    identifier: str=None,
                    sequence_column: str=None,
                    layers: list=None,
                    optimizer: str="rmsprop",
                    loss: str=None,
                    loss_weights=None,
                    metrics: list[str]=None,
                    weighted_metrics=None,
                    run_eagerly=False,
                    steps_per_execution=1,
                    jit_compile="auto",
                    #pss_evaluation_shards = 0,
                    #auto_scale_loss=True,         
                    batch_size=None,
                    epochs=1,
                    verbose="auto",
                    callbacks=None,
                    validation_split=0.0,
                    validation_data=None,
                    shuffle=True,
                    class_weight=None,
                    sample_weight=None,
                    initial_epoch=0,
                    steps_per_epoch=None,
                    validation_steps=None,
                    validation_batch_size=None,
                    steps=None,
                    validation_freq=1) -> None:
        super().__init__(target_col, identifier, sequence_column)
        self.layers_=layers
        self.optimizer=optimizer
        self.loss= loss
        self.loss_weights= loss_weights
        self.metrics= metrics
        self.weighted_metrics= weighted_metrics
        self.run_eagerly=run_eagerly
        self.steps_per_execution= steps_per_execution
        self.jit_compile=jit_compile
        #self.pss_evaluation_shards = pss_evaluation_shards
        #self.auto_scale_loss= auto_scale_loss
        self.batch_size=batch_size
        self.epochs=epochs
        self.callbacks=callbacks
        self.verbose=verbose
        self.validation_split=validation_split
        self.validation_data=validation_data
        self.shuffle=shuffle
        self.class_weight=class_weight
        self.sample_weight=sample_weight
        self.initial_epoch=initial_epoch
        self.steps_per_epoch=steps_per_epoch
        self.validation_steps=validation_steps
        self.validation_batch_size=validation_batch_size
        self.validation_freq=validation_freq
        self.steps=steps

        self._parameter_constraints.update({
            "layers": ['array-like', StrOptions({l for l in List_of_KerasLayers[ProgrammingLanguages.Python].keys() if not l.startswith('_')})],
            "optimizer": [StrOptions({"rmsprop", "adam", "adamw", "sgd",
                                      "adagrad", "adadelta", "adamax", "adafactor",
                                      "nadam", "ftrl", "lion", "lamb"})],
            "loss": [StrOptions({"mean_squared_error", "mean_absolute_error", "mean_absolute_percentage_error",
                                 "mean_squared_logarithmic_error", "kullback_leibler_divergence",
                                 "hinge", "cosine_similarity", "log_cosh", "categorical_crossentropy",
                                 "sparse_categorical_crossentropy", "binary_crossentropy"})],
            "metrics": ['array-like'],
            "run_eagerly": [bool],
            "steps_per_execution": [int],
            "batch_size": [int],
            "epochs": [int],
            "shuffle": [bool],
            "steps_per_epoch": [int],
            "validation_batch_size": [int],
            "validation_freq": [int],
            "steps": [int]
        })
        
    def predict(self, X: DataFrame):
        _logger.warning('predict')
        probability= self.proba(X)
        outcome = (probability > 0.5).astype('int32')
        return self.inflate_y(outcome)

    def proba(self, X: DataFrame):
        _logger.warning('proba')
        X_reshaped=self.reshape_X_to_tensor( X)
        _logger.warning('self.model.predict')
        return self.model.predict(X_reshaped, batch_size=self.batch_size, verbose=self.verbose, steps=self.steps, callbacks=self.callbacks)

    def score(self, X, y, **kargs ):
        score = self.evaluate(X,y)[0]
        return score
    
    def evaluate(self, X, y):
        X,y= self.reshape_data_to_tensor( X, y)
        score, acc = self.model.evaluate(X,y, batch_size=self.batch_size, sample_weight=self.sample_weight, steps=self.steps,callbacks=self.callbacks)
        return score, acc
    

    def fit(self, X:DataFrame, y: DataFrame):
        self.number_sequences=self.get_len_sequence(X)
        self.number_features=self.get_number_features(X)       
        X_reshaped,y_reshaped=self.reshape_data_to_tensor( X,y)
        self.build_model((self.number_sequences,self.number_features))
        return self.model.fit(X_reshaped, y_reshaped,
                            batch_size=self.batch_size,
                            epochs=self.epochs,
                            callbacks=self.callbacks,
                            verbose=self.verbose,
                            validation_split=self.validation_split,
                            validation_data=self.validation_data,
                            shuffle=self.shuffle,
                            class_weight=self.class_weight,
                            sample_weight=self.sample_weight,
                            initial_epoch=self.initial_epoch,
                            steps_per_epoch=self.steps_per_epoch,
                            validation_steps=self.validation_steps,
                            validation_batch_size=self.validation_batch_size,
                            validation_freq=self.validation_freq      
                            )
    
    def compile_model(self):
        return self.model.compile(optimizer = self.optimizer,
                                  loss = self.loss,
                                  loss_weights = self.loss_weights,
                                  metrics = self.metrics,
                                  weighted_metrics=self.weighted_metrics,
                                  run_eagerly= self.run_eagerly,
                                  steps_per_execution= self.steps_per_execution,
                                  jit_compile= self.jit_compile)
                                  #auto_scale_loss= self.auto_scale_loss)
                                  #pss_evaluation_shards=self.pss_evaluation_shards)

    def build_model(self, shape: tuple):
        self.model = Sequential()
        self.model.add(Input(shape=shape))
        for layer in self.layers_:
            self.model.add(layer)
        self.compile_model()
        return self.model


def get_parameter_type_and_options(algorithm_name: str, parameter: str):
    """
    Gets the type and options of the parameter for the given algorithm.
    """
    language = ProgrammingLanguages.Python
    
    def get_estimators_with_the_same_type(algorithm_name: str):
        current_algorithm_types = List_of_Algorithms[language][algorithm_name]['flags']
        list_of_estimators = []
        for estimator in List_of_Algorithms[language]:
            if estimator == algorithm_name:
                continue
            for current_algorithm_type in current_algorithm_types:
                if current_algorithm_type in List_of_Algorithms[language][estimator]['flags']:
                    list_of_estimators.append(estimator)
        return list_of_estimators
    
    param_type, param_options = None, None
    if algorithm_name in List_of_Algorithms[language]:
        algorithm_info = List_of_Algorithms[language][algorithm_name]
        algorithm = getattr(
            importlib.import_module(algorithm_info['import']),
            algorithm_info['name']
        )

    else:
        return param_type, param_options

    if hasattr(algorithm, '_parameter_constraints'):
        if parameter not in algorithm._parameter_constraints:
            return param_type, param_options
        if parameter in {'random_state', 'seed', 'n_jobs'}:
            param_type = 'int'
        elif parameter in {'estimator', 'final_estimator'}:
            param_type = 'Estimator'
            param_options = get_estimators_with_the_same_type(algorithm_name)
        elif parameter == 'estimators':
            param_type = 'list[Estimator]'
            param_options = get_estimators_with_the_same_type(algorithm_name)
        elif parameter == 'kernel':
            param_type = 'Kernel'
            param_options = list(get_kernels_list(ProgrammingLanguages.Python).keys())
        elif parameter == {'metric', 'scoring'}:
            param_type = 'Metric'
            param_options = get_algorithm_list("Metric", language)
        for t in algorithm._parameter_constraints[parameter]:
            if t:
                if t == 'boolean':
                    param_type = 'bool'
                elif t == 'cv_object':
                    param_type = 'int'
                elif t in {str, int, float}:
                    param_type = 'str'
                elif t == list:
                    param_type = 'list'
                elif t == 'array-like':
                    if parameter in {'monotonic_cst', 'hidden_layer_sizes', 'min_categories'}:
                        param_type = 'list[int]'
                    elif parameter in {'weights', 'alphas', 'priors', 'l1_ratios', 'class_prior'}:
                        param_type = 'list[float]'
                    elif parameter == 'metrics':
                        param_type = 'list[Metric]'
                        param_options = get_algorithm_list("Metric", language)
    return param_type, param_options