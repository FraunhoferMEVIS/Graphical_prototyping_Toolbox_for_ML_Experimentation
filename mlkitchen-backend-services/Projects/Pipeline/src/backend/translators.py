""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: translators.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The translators for different types of mlflow recepies
-----------------------------------------------------------------------------
"""

import shutil
import os
from copy import deepcopy
from abc import ABC, abstractmethod
from methods_repository.Metric.Metric import get_greater_is_better, \
                                             List_of_Algorithms as Metrics
from methods_repository.config_models import ProgrammingLanguages, \
                                             TaskTypes
from methods_repository.NewFeature.NewFeature import List_of_Algorithms \
    as New_Feature
from methods_repository.config_models import RecipeConfig, \
                                             ColumnTransformerConfig
from .data_catalog import DataAccess
from .app_config import DATA_DESCRIPTOR_URL
from .utilities import save_config_to_yaml, input_parameters_to_str


class TranslatorBase(ABC):
    """
    The base translator class. All inherited classed should implement
    "save_user_config_to_mlops" function.
    """
    def __init__(self, project_name,  project_path) -> None:
        super().__init__()
        self.name = project_name
        self._project_path = project_path

    @abstractmethod
    def config_to_recipe(self, config: RecipeConfig) -> None:
        """
        saves the input configuration as an mlflow recipe
        """
        raise NotImplementedError()


class TabularTranslator(TranslatorBase):
    """
    A translator for Tabular data. It supports conversion for
    regression and classification.
    """
    def __init__(self, project_name, project_path) -> None:
        super().__init__(project_name, project_path)
        self._atributes = None

    def config_to_recipe(self, config: RecipeConfig):
        _EVALUATION_MIN_THRESHOLD = 0.01
        _EVALUATION_MAX_THRESHOLD = 99.99

        data_type = "parquet"
        input_data_location = os.path.join(self._project_path,
                                           "data", "data.parquet")
        if "timeseries" in config.task.value:
            timeseries = True  
            if config.task.value == "timeseries_regression":
                config.task = TaskTypes.regression
            elif config.task.value == "timeseries_classification":
                config.task = TaskTypes.classification
        else: 
            timeseries = False 

        if not config.target_col:
            data_descriptor = DataAccess(data_descriptor_url=DATA_DESCRIPTOR_URL,
                                 project_id=self.name)
            config.target_col = data_descriptor.get_target_col()

        ml_config = {
            "recipe": f"{config.task.value}/v1",
            "target_col": config.target_col,
            "steps": {
                "ingest": {"using": data_type,
                           "location": input_data_location},
                "register": {
                    "model_name":
                        f"{self.name}_{config.task.name}",
                    "allow_non_validated_model": True},
                "ingest_scoring": {"using": data_type,
                                   "location": input_data_location},
                "predict": {
                    "output": {
                        "using": data_type,
                        "location": os.path.join(self._project_path, "data",
                                                 "sample_output.parquet")},
                },
            },
        }
        if config.task == TaskTypes.classification:
            if not config.positive_class:
                raise ValueError(
                    f"""The 'positive_class' must be defined \
                        for a {config.task.name} task.""")

            if isinstance(config.positive_class, str) and config.positive_class.isnumeric():
                config.positive_class = int(config.positive_class)

            ml_config["positive_class"] = config.positive_class

        if data_type not in {"parquet"}:
            ml_config["steps"]["ingest"]["loader_method"] = \
                "load_file_as_dataframe"

        ml_config["steps"]["split"] = {
            "using": "custom",
            "split_method": "split_fn"
        }
        shutil.copy(os.path.join('.', 'src', 'backend', 'code_snippets',
                                 'split.py'),
                    os.path.join(self._project_path, 'steps'))
   
        ml_config["steps"]["transform"] = {
            "transformer_method": "transformer_fn"
            }
        self.__create_transformation_steps(config, timeseries)
        
        if config.sampling:
            resampling_minority_percentage = config.sampling.resampling_minority_percentage
        else:
            resampling_minority_percentage = 0.000001

        if config.estimator:
            estimator_name = config.estimator.name.lower()
            ml_config["steps"]["register"]["model_name"] += \
                f'_{estimator_name}'
            ml_config["steps"]["train"] = {
                "estimator_method":
                    f"estimator_{estimator_name}",
                "using": "custom",    
            }
            if config.task == TaskTypes.classification:
                ml_config["steps"]["train"]["resampling_minority_percentage"] = \
                                    resampling_minority_percentage
            self.__create_train_step(config)

        if config.metrics:
            validation_criteria_configs = []
            custom_metrics = []
            for m in config.metrics:
                greater_is_better_val = get_greater_is_better(m)
                
                if m.threshold is not None:
                    threshold = m.threshold
                elif greater_is_better_val:
                    threshold = _EVALUATION_MIN_THRESHOLD
                else:
                    threshold = _EVALUATION_MAX_THRESHOLD
            
                validation_criteria_configs.append(
                    {"metric": m.name,
                     "threshold": threshold})
                
                custom_metrics.append(
                    {"name": m.name,
                     "function": f"{m.name}_",
                     "greater_is_better": greater_is_better_val})
                
            ml_config["steps"]["evaluate"] = {
                "validation_criteria": validation_criteria_configs}
            ml_config["custom_metrics"] = custom_metrics

            if config.primaryMetric:
                ml_config["primary_metric"] = config.primaryMetric
            self.__define_metrics(config)
        save_config_to_yaml(ml_config, os.path.join(self._project_path,
                                                    'recipe.yaml'))

    def __project_columns_attributes(
            self,
            configurations: ColumnTransformerConfig,
            transformation: str,  # imputer or encoders
            target_col: str
            ) -> None:
        if self._atributes is None:
            data_accessor = DataAccess(DATA_DESCRIPTOR_URL, self.name)
            self._atributes = {}
            for key in data_accessor.get_data_keys():
                self._atributes[key] = {'type': 'key'}
            for column in data_accessor.get_attributes_list():
                if column == target_col:
                    continue
                self._atributes[column] = {}
                if data_type := data_accessor.data_type(column):
                    self._atributes[column]['type'] = data_type
        if configurations:
            where_to_apply = {
                'all': [],
                'all_categorical': [],
                'all_numerical': [],
                'individuals': {}
            }

            def add_or_append(in_dict, member, value):
                out_dict = deepcopy(in_dict)
                if member in in_dict:
                    out_dict[member].append(value)
                else:
                    out_dict[member] = [value]
                return out_dict

            for conf in configurations:
                alg_parameters = conf.parameters
                alg_settings = {
                    "name": conf.name,
                    "parameters": alg_parameters if alg_parameters else {}
                }
                if alg_parameters:
                    if 'all_categorical' in conf.parameters:
                        conf.all_categorical = conf.parameters['all_categorical']
                    if 'all_numerical' in conf.parameters:
                        conf.all_numerical = conf.parameters['all_numerical']
                if not conf.language:
                    conf.language = "python"
                if conf.column_name:
                    if isinstance(conf.column_name, list):
                        for column in conf.column_name:
                             where_to_apply["individuals"] = \
                        add_or_append(where_to_apply["individuals"],
                                      column,
                                      alg_settings)
                    else:
                        where_to_apply["individuals"] = \
                        add_or_append(where_to_apply["individuals"],
                                      conf.column_name,
                                      alg_settings)
                elif conf.all_numerical:
                    where_to_apply = \
                        add_or_append(where_to_apply,
                                      "all_numerical",
                                      alg_settings)
                elif conf.all_categorical:
                    where_to_apply = \
                        add_or_append(where_to_apply,
                                      "all_categorical",
                                      alg_settings)
                else:
                    where_to_apply = \
                        add_or_append(where_to_apply,
                                      "all",
                                      alg_settings)

            def transfer_methods_to_columns(method_list,
                                            setting,
                                            transformation):
                for method in method_list:
                    setting = add_or_append(
                                setting,
                                transformation,
                                method)
                return setting

            for column, setting in self._atributes.items():
                if column in where_to_apply["individuals"]:
                    for method in where_to_apply["individuals"][column]:
                        setting = add_or_append(
                                    setting,
                                    transformation,
                                    method)
                elif setting['type'] == 'categorical' and \
                        where_to_apply["all_categorical"]:
                    setting = transfer_methods_to_columns(
                        where_to_apply["all_categorical"],
                        setting,
                        transformation)
                elif setting['type'] == 'numerical' and \
                        where_to_apply["all_numerical"]:
                    setting = transfer_methods_to_columns(
                        where_to_apply["all_numerical"],
                        setting,
                        transformation)
                elif where_to_apply["all"]:
                    setting = transfer_methods_to_columns(
                        where_to_apply["all"],
                        setting,
                        transformation)
                self._atributes[column] = deepcopy(setting)

        save_config_to_yaml(self._atributes,
                            os.path.join(
                                self._project_path,
                                "steps",
                                "attributes.yml"))

    def __create_transformation_steps(self, config: RecipeConfig, timeseries: bool = False) -> None:
        """
        The transformation step is generated based on the input config file.
        The transformation consists of imputation, onehot and scalar encoding.
        Based on the type of each column one or two of these transformations
        are applied. If the impute key exists in the config, then the
        defined algorithms are going to included in the transformation step.
        Otherwise, only onehot and scalar encoders are applie to the
        categorical and numerical columns, respectively.
        params:
            config: RecipeConfig the entire configuration of the recipes
        result:
            the respective attributes.yaml file and the transform.py files
            will be added to the project_folder/steps
        """
        self.__project_columns_attributes(
                                            config.imputation,
                                            'imputer',
                                            config.target_col)
        self.__project_columns_attributes(
                                            config.encoders,
                                            'encoders',
                                            config.target_col)
        shutil.copy(os.path.join('.', 'src', 'backend', 'code_snippets',
                                 'transform.py'),
                    os.path.join(self._project_path, 'steps'))

        # generate code for new features
        new_feature_call = self.__create_new_feature(config)

        # generate code for droping columns
        drop_columns_code = self.__drop_columns_code(config, timeseries)
            

        # generate code for fearue selection
        featur_selection_script = self.__create_feature_selection(config)

        transfomation_script = new_feature_call + drop_columns_code + \
            featur_selection_script

        with open(os.path.join(self._project_path, 'steps',
                               'transform.py'), 'at',
                  encoding="utf-8") as file:
            file.write(transfomation_script)

    def __drop_columns_code(self, config: RecipeConfig, timeseries: bool) -> str:
        data_accessor = DataAccess(DATA_DESCRIPTOR_URL, self.name)
        columns_to_drop = data_accessor.get_data_keys()
        if not columns_to_drop or timeseries or config.task not in {TaskTypes.classification,
                                                      TaskTypes.regression}:
             script = """

def get_drop_columns_transformer():
    return None
"""
             return script
        script = f"""

def get_drop_columns_transformer():
    parameters = {{
        "feature_names": {columns_to_drop},
        "keep": False
    }}
    return (
            "drop_columns",
            ModuleFinder.use_method(
                "FeatureSelection",
                "SelectByName",
                **parameters
            ))
"""
        return script

    def __create_new_feature(self, config: RecipeConfig) -> str:
        sample_code = """

def {func}_{column_name}_(data: DataFrame):
    from {pkg} import {func}
    return {func}(data,
            {indentation}'{column_name}',
            {indentation}{params})
"""
        methods = ""
        transformers = """

def get_function_transformers():
    function_transformer_params = ({"feature_names_out": "one-to-one"})
    steps = [
"""
        if config.new_feature:
            for feature in config.new_feature:
                language = feature.language or ProgrammingLanguages.Python
                if feature.name in New_Feature[language]:
                    pkg = New_Feature[language][feature.name]["import"]
                    func = New_Feature[language][feature.name]["name"]
                    column_name = feature.column_name
                    params = input_parameters_to_str(feature.parameters)
                    methods += sample_code.format(func=func, pkg=pkg,
                                                  indentation=' '*len(func),
                                                  column_name=column_name,
                                                  params=(",\n" +
                                                          " "*(len(func)+11)
                                                          ).join(
                                                            params.split(',')))
                    transformers += f"""
        ("calculate_{column_name}",
         FunctionTransformer({func}_{column_name}_,
                             **function_transformer_params)),
"""
        transformers += """
        ]
    return steps
"""
        return methods + transformers

    def __create_feature_selection(self, config: RecipeConfig):
        if not config.feature_selection:
            transformers = """
def get_feature_selection_transformer():
    return None
"""
            return transformers

        algorithm_name = config.feature_selection.name
        transformer_script = """

def get_feature_selection_transformer():
    # It will import the selected feature selection algorithm,
    # based on the user's input.
"""
        if config.feature_selection.parameters:
            transformer_script += f"""
    parameters = {config.feature_selection.parameters}
"""
        else:
            transformer_script += """
    parameters = {}"""

        transformer_script += f"""
    transformer = ("feature_selection_{algorithm_name}",
                   ModuleFinder.use_method(
                    "FeatureSelection",
                    "{algorithm_name}",
                    **parameters),
                   )
    return transformer
"""
        return transformer_script

    def __create_train_step(self, config: RecipeConfig) -> None:
        if config.estimator.language is None or \
           config.estimator.language == "python":
            if os.path.exists(os.path.join(self._project_path,
                                           'steps',
                                           'train.py')):
                with open(os.path.join(self._project_path,
                                       'steps',
                                       'train.py'),
                          'rt', encoding='utf-8') as train_file:
                    estimator_func = train_file.read()
            else:
                estimator_func = '''"""
This module defines the following routines used by the 'train' step of the
recipe:
- ``estimator_fn``: Defines the customizable estimator type and parameters
  that are used during training to produce a model recipe.
"""
from methods_repository.abstraction import ModuleFinder

'''
            # if function with this name already exists, do not need to add
            if f'def estimator_{(config.estimator.name).lower()}' in \
                    estimator_func:
                return

            estimator_func += f'''
def estimator_{(config.estimator.name).lower()}(*args, **kwargs):
    """
    Returns an *unfitted* estimator that defines ``fit()`` and ``predict()``
    methods. The estimator's input and output signatures should be compatible
    with scikit-learn estimators.
    """'''
            if config.estimator.parameters:
                if "hyper_parameter_tuning" in config.estimator.parameters and "scoring" not in config.estimator.parameters:
                    config.estimator.parameters["scoring"] = config.primaryMetric
                estimator_func += f'''
    parameters = {config.estimator.parameters}'''
            else:
                estimator_func += '''
    parameters = {}'''

            estimator_func += f'''
    return ModuleFinder.use_method("Estimator",
                                   "{config.estimator.name}",
                                   **parameters)

'''
            with open(os.path.join(self._project_path,
                                   'steps',
                                   'train.py'),
                      'wt',
                      encoding="utf-8") as train_file:
                train_file.write(estimator_func)

    def __define_metrics(self, config: RecipeConfig) -> None:
        language = ProgrammingLanguages.Python
        one_metric_code = """
def {metric.name}_(
    eval_df: DataFrame,
    builtin_metrics: dict[str, float]) -> float:
    from {pkg} import {func}
    return {func}(
        eval_df["target"],
        eval_df["prediction"],
        {params})

"""
        shutil.copy(os.path.join('.', 'src', 'backend', 'code_snippets',
                                 'custom_metrics.py'),
                    os.path.join(self._project_path,
                                 'steps'))
        for metric in config.metrics:
            if metric.name in Metrics[language]:
                pkg = Metrics[language][metric.name]["import"]
                func = Metrics[language][metric.name]["name"]
                params = input_parameters_to_str(metric.parameters)
                with open(os.path.join(self._project_path,
                                       "steps",
                                       "custom_metrics.py"),
                          'a', encoding="utf-8") as\
                        metric_code_file:
                    metric_code_file.write(one_metric_code.format(
                        metric=metric, pkg=pkg, func=func, params=params))


class Translator:
    """
    Defining the right translator based on the input config file
    """
    @staticmethod
    def use_recipe(config: RecipeConfig, project_name: str,
                   project_path: str) -> TranslatorBase:
        """
        returning the right translator for a given recipe
        :config a RecipeConfig that should contain a task.
        :project_name: An str, will contain the name of the project.
        :returns: a Translator module to translate a config to an mlflow recipe
        :raises NotImplementedError: if the recipe is not yet implemented.
        """
        if config.task.value in {'regression', 'classification',
                                 'timeseries_classification', 'timeseries_regression'}:
            return TabularTranslator(project_name, project_path)

        raise NotImplementedError(
            f"The {config.task.name} recipe is not supported yet.")
