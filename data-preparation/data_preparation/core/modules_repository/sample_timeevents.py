""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: sample_timeevents.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 07/2024
description: The module for sample time events
-----------------------------------------------------------------------------
"""
import logging
import pandas as pd
from pandas import Series
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from .new_column import (string_to_function, get_operation_output_type)
from .aggregate import _operators


__all__ = ["SampleTimeEvents"]
_logger = logging.getLogger(__name__)


def sort_and_ffill(df, fill_column):
    df[fill_column]= df[fill_column].ffill()
    return df

def sort_and_bfill(df, fill_column):
    df[fill_column] =  df[fill_column].bfill()
    return df

def interpolate_linear(df, fill_column):
    df[fill_column] =  df[fill_column].interpolate(method='linear')
    return df

def _None():
    pass

_operate_fill_nan = {
"interpolate_linear": {
        "method": interpolate_linear,
        "output_type": "numerical",
        "allowed_input_type": ["numerical"]
    },
"fill_with_previous_value": {
        "method": sort_and_ffill,
        "output_type": "numerical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
"fill_with_next_value": {
        "method": sort_and_bfill,
        "output_type": "numerical",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
"None": {
        "method": _None,
        "output_type": "",
        "allowed_input_type": ["numerical","categorical", "time"]
    },
}

class SampleTimeEvents(Node):
    """
    It samples the column values based on its time window and its key. Values can be sampled with a chosen function. 
    The first and last time window can be specified by the user. If it is not specified, the smallest and greatest time windows are used to define the range.
    If an identifier has no value, NaN is assigned. The user can choose a fact to fill it (e.g., interpolate, previous value, ... )
    """
    NAME = "sample-timeevents"
    DESCRIPTION = "The module samples the values based on its time window. Missing time windows are created."
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to be filtered",
            "required": True,
        },
    ]
    PARAMETERS = {
        "grouping_keys": {
            "id": "grouping_keys",
            "name": "grouping keys",
            "description": """The keys to group, e.g. patient_id., \
                it can also be a list of keys to be used for grouping.""",
            "type": "string",
            "required": True,
            "value": ["result"],
            "multipleValues": True
        },
        "time_window": {
            "id": "time_window",
            "name": "time_window keys",
            "description": """The column which assigns the time window.""",
            "type": "string",
            "required": True,
            "value": ["time_window"],
            "multipleValues": True
        },
        "operator": {
            "id": "operator",
            "name": "operator",
            "description": "The operator to be applied to the columns",
            "type": "string",
            "required": False,
            "value": ["sum"],
            "allowedValues": set(_operators.keys()),
            "multipleValues": True
        },
        
        "upper_bound_timewindow": {
            "id": "upper_bound_timewindow",
            "name": "upper_bound_timewindow",
            "description": "The upper bound of the time window range. If not specified, the greatest window is used.",
            "type": "integer",
            "required": False,
            "value": None
        },

        "lower_bound_timewindow": {
            "id": "lower_bound_timewindow",
            "name": "lower_bound_timewindow",
            "description": "The lower bound of the time window range. If not specified, the smallest window is used.",
            "type": "integer",
            "required": False,
            "value": None
        },
        "operator_fill_nan": {
            "id": "operator_fill_nan",
            "name": "operator_fill_nan",
            "description": "How to fill generated time windows, e.g. use previous value. If none is chosen, NaN remains.",
            "type": "string",
            "required": False,
            "value": "None",
            "allowedValues": set(_operate_fill_nan.keys()),
            "multipleValues": False
        },
        "refrence_column_fill_nan": {
            "id": "refrence_column_fill_nan",
            "name": "refrence_column_fill_nan",
            "description": "If a operator for fill NaN is chosen, this is the referenced time column. For instance, if chosen fill with last value, the column with the time of the event should be chosen here.  ",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "columns": {
            "id": "columns",
            "name": "columns",
            "description": "The columns to apply the operation on. As input, a list of columns or all_numerical, all_categorical, all_time is possibile. Please consider that operator and operator_fill_nan can handle the column type.",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "output_column_name": {
            "id": "output_column_name",
            "name": "output column name",
            "description": "The name of the output column that is generated.",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
     }

    def __init__(self,
                 module_id: str = "",
                 label: str = None,
                 inputs: list[Socket] = None,
                 config: dict[str, ModuleConfigParameter] = None,
                 valid_results: bool = False,
                 position: dict = None,
                 parent_project: str = None,
                 result_repo: ResultsRepository = FileResultsRepository(),
                ):
        super().__init__(
                 module_id=module_id,
                 label=label,
                 inputs=inputs,
                 config=config,
                 valid_results=valid_results,
                 position=position,
                 parent_project=parent_project,
                 result_repo=result_repo,
                 )

    def check_feature_type(self,columns, operators, operator_set):
        feature_dict=self.get_columns_to_operate_on(columns)
        for feature_name,feature_type in feature_dict.items(): 
            for operator in operators:
                allowed_input_types=get_operation_input_type(operator,operator_set)
                if feature_type not in allowed_input_types:
                    raise ValueError(f"Feature '{feature_name}' with type '{feature_type}' is not allowed for fill_nan_operator '{operator}'. Allowed types are: {allowed_input_types}")

    def get_columns_to_operate_on(self,columns)-> dict:
        input_metadata=self.get_input_metadata()
        input_metadata=input_metadata[self.inputs[0].name].get('features', [])
        columns_to_apply_on={}
        for feature in input_metadata:
            if feature['name'] in columns:
                columns_to_apply_on[feature['name']] = feature['type']
        return columns_to_apply_on
        
    def apply_fill_nans(self, chunk, fill_column, group_key):
        ops_NaNs = self.parameters["operator_fill_nan"].value
        functions = get_operator(ops_NaNs,_operate_fill_nan)
        def apply_funcs_to_group(group):
            for func in functions:
                group = func(group, fill_column)
            return group        
        grouped = chunk.groupby(by=group_key).apply(apply_funcs_to_group).reset_index(drop=True)
        return grouped
    
    def get_columns(self,columns):
        column_list=[]
        for column in columns:
            if column=="all_numerical":
                column_list=column_list+self.get_features_of_type("numerical")
            elif  column=="all_categorical":
                column_list=column_list+self.get_features_of_type("categorical")
            elif  column == "all_time":
                column_list=column_list+self.get_features_of_type("time")
            elif column == self.parameters["time_window"].value:
                continue
            else:
                column_list.append(column)

        column_list=list(set(column_list))
        column_list=[item for item in column_list if item not in self.parameters["time_window"].value]
        return column_list
    
    def get_features_of_type(self,_type):
        input_metadata=self.get_input_metadata()
        input_meta=input_metadata[self.inputs[0].name].get('features', [])
        features_ = []
        for feature in input_meta:
            if feature['type'] == _type:
                features_.append(feature['name'])
        return features_

    def _get_output_column_names_as_dict(self):
        columns = to_list(self.parameters["columns"].value)
        names = self._get_output_column_names()
        names = {col["column_name"]: col["function"] for col in names.values()}
        agg_dict = {}
        for col in columns:
            for name, func in names.items():
                if col in name: 
                    agg_dict[f'{col}_{name.split("_")[1]}'] = (col, func)
        return agg_dict

    def _get_output_column_names(self):
        ops = to_list(self.parameters["operator"].value)
        output_column_name = self.parameters["output_column_name"].value
        columns = to_list(self.parameters["columns"].value)
        functions = [string_to_function(op, operators=_operators) for op in ops]
        self.check_feature_type(columns, ops, _operators)
        if output_column_name:
            if len(output_column_name) != len(functions) * len(columns):
                raise ValueError("The output_column_name should have the same length as the number of functions times the number of columns.")
            
            names = {}
            idx = 0
            for col in columns:
                for i, op in enumerate(ops):
                    
                    key = f'{col}_{op}'
                    names[key] = {
                        "column_name": output_column_name[idx],
                        "function": functions[i]
                    }
                    idx += 1
        else:
            names = {}
            for col in columns:
                for i, op in enumerate(ops):
                    key = f'{col}_{op}'
                    names[key] = {
                        "column_name": key,
                        "function": functions[i]
                    }

        return names

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        output_metadata = {
            "keys": [],
            "features": []
        }
        if self.inputs and self.inputs[0].name:
            grouping_keys = to_list(self.parameters["grouping_keys"].value,self.parameters["time_window"].value)
            in_meta = input_metadata[self.inputs[0].name]
            for key in grouping_keys:
                if key in in_meta["keys"] or in_meta["features"] :
                    output_metadata["keys"].append(key)
                else:
                    raise ValueError(f"The {key} could not be found in the input table.")

            ops = to_list(self.parameters["operator"].value)
            columns = to_list(self.parameters["columns"].value)
            col_types = {}
            for feature in in_meta["features"]:
                if feature["name"] in columns:
                    col_types[feature["name"]] = feature["type"]
            for col in columns:
                for op in ops:
                    output_metadata["features"].append({
                    "name": f'{col}_{op}',
                    "type": get_operation_output_type(op, input_type=col_types[col], operators=_operators)
                })
            return output_metadata
        raise TypeError("Please check that the inputs are connected and the results are ready!")

    def run(self):
        super().run()
        fill_nans = False
        columns = self.get_columns(self.parameters["columns"].value)
        self.parameters["columns"].value = columns
        grouping_keys = to_list(self.parameters["grouping_keys"].value)
        time_window = to_list(self.parameters["time_window"].value)
        grouping_columns = to_list(grouping_keys,time_window)
        lower_bound = self.parameters["lower_bound_timewindow"].value
        upper_bound = self.parameters["upper_bound_timewindow"].value
        agg_dict = self._get_output_column_names_as_dict()
        
        ##output meta
        output_meta = self.define_output_metadata(input_metadata = self.get_input_metadata())
        output_meta["keys"] = output_meta["keys"]
        self.write_metadata(output_meta)

        if self.parameters["operator_fill_nan"].value is not None and \
                self.parameters["operator_fill_nan"].value != "None":
            fill_nans=True
            time_reference_column = to_list(self.parameters["refrence_column_fill_nan"].value)  
            if time_reference_column is None:
                raise IOError("Reference column for fill NaNs is None!")     
            self.check_feature_type(columns, to_list(self.parameters["operator_fill_nan"].value), _operate_fill_nan)           
            
        try:
            for chunk in self._results_repo.get(self.parent_project,
                                                self.inputs[0].value,
                                                ResultTypes.DATAFRAME,
                                                chunksize=1000000):
                chunk= merge_missing_timewindows(chunk,grouping_keys, time_window, lower_bound, upper_bound)
                if fill_nans:
                    chunk=chunk.sort_values(by=grouping_columns+time_reference_column)
                    chunk=self.apply_fill_nans( chunk, columns,grouping_keys)
                result = chunk.groupby(grouping_columns).agg(**agg_dict).reset_index()
                if not self.write_output(result):
                    raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except KeyError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self.error_message)
            raise KeyError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to add new column: %s", e)
            raise Exception(f"Failed to add new column: {e}") from e


def get_lower_bound(time_window_column: Series, lower_bound: int | None):
    return lower_bound if lower_bound is not None else int(time_window_column.min())

def get_upper_bound(time_window_column: Series, upper_bound: int | None):
    return upper_bound if upper_bound is not None else  int(time_window_column.max())

def create_series(df, time_window_column_name, lower_bound: int | None, upper_bound: int | None):
    lower_bound_=get_lower_bound(df[time_window_column_name], lower_bound)
    upper_bound_=get_upper_bound(df[time_window_column_name], upper_bound)
    series = pd.DataFrame(data=list(range(lower_bound_, upper_bound_+1)), columns=time_window_column_name)
    return series

def merge_missing_timewindows(df,primary_key, time_window_column_name, lower_bound, upper_bound):
    timewindows_df=create_series(df, time_window_column_name, lower_bound, upper_bound)
    all_combinations = df[primary_key].drop_duplicates().assign(key=1).merge(timewindows_df.assign(key=1), on='key').drop('key', axis=1)
    result_df = pd.merge(all_combinations, df, on=primary_key+time_window_column_name, how='left')
    return result_df

def to_list(*args):
    list_=[]
    for arg in args:
        if arg is None:
            continue
        list_ = list_ + [arg] if isinstance(arg, str) else list_ + arg
    return list_

def get_operator(ops, allowed_operator):
        ops=to_list(ops)
        return [string_to_function(op, operators=allowed_operator)
                        for op in ops]


def get_operation_input_type(operator_name: str, operators: dict=None) -> str:
    if operators is None:
        operators = _operators
    if operator_name in operators:
        return operators[operator_name]["allowed_input_type"]
    raise ValueError(f"Unknown operator: {operator_name}")