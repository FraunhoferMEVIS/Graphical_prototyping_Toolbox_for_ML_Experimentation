""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: NewFeautre.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 01/2023
description: The implemented methods for NewFeature
-----------------------------------------------------------------------------
"""

import operator
from enum import Enum
from pandas import DataFrame
import numpy as np
import pandas as pd
from methods_repository.config_models import ProgrammingLanguages


INDICES_OF_DATA_INPUT = [0]
_IMPORT_THIS = "methods_repository.NewFeature.NewFeature"
List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        "operate": {
            "import": _IMPORT_THIS,
            "name": "operate",
        },
        "duration": {
            "import": _IMPORT_THIS,
            "name": "duration",
        },
        "convert_timediff_to_unit": {
            "import": _IMPORT_THIS,
            "name": "convert_timediff_to_unit",
        },
        "round_time": {
            "import": _IMPORT_THIS,
            "name": "round_time",
        },
        "round_numeric": {
            "import": _IMPORT_THIS,
            "name": "round_numeric",
        },
        "day_of_the_week": {
            "import": _IMPORT_THIS,
            "name": "day_of_the_week",
        },
        "name_of_the_day": {
            "import": _IMPORT_THIS,
            "name": "name_of_the_day",
        },
        "hour": {
            "import": _IMPORT_THIS,
            "name": "hour",
        },
        "second": {
            "import": _IMPORT_THIS,
            "name": "second",
        },
        "maximum": {
            "import": _IMPORT_THIS,
            "name": "maximum",
        },
        "minimum": {
            "import": _IMPORT_THIS,
            "name": "minimum",
        },
        "grouped": {
            "import": _IMPORT_THIS,
            "name": "grouped",
        },
        "flag": {
            "import": _IMPORT_THIS,
            "name": "flag",
        },
        "is_element": {
            "import": _IMPORT_THIS,
            "name": "is_element",
        },
        "recenter_time_wrt_t0": {
            "import": _IMPORT_THIS,
            "name": "recenter_time_wrt_t0",
        },
        "recenter_wrt_weekdays_in_unit": {
            "import": _IMPORT_THIS,
            "name": "recenter_wrt_weekdays_in_unit",
        },
        "time_window": {
            "import": _IMPORT_THIS,
            "name": "time_window",
        },
    },
    ProgrammingLanguages.R: {},
}


class ConditionalOperators(str, Enum):
    eq = "eq"
    ne = "ne"
    lt = "lt"
    le = "le"
    gt = "gt"
    ge = "ge"


class MathOperators(str, Enum):
    add = "add"
    sub = "sub"
    mul = "mul"
    truediv = "truediv"
    floordiv = "floordiv"
    mod = "mod"
    pow = "pow"
    neg = "neg"
    abs = "abs"
    pos = "pos"
    invert = "invert"
    lshift = "lshift"
    rshift = "rshift"
    and_ = "and"
    or_ = "or"
    xor = "xor"

class StatisticalMeasures(str, Enum):
    min = "min"
    max = "max"
    mean = "mean"
    median = "median"
    std = "std"
    sum = "sum"
    count = "count"
    first = "first"
    last = "last"


def duration(data: DataFrame, column_name: str, eventdate_column_name: str,
             base_column_name: str):
    """
    Adds a new feature to the data frame, which is the time difference
    between the eventdate and the base column.
    """
    data[column_name] = _time_diff(data[eventdate_column_name],
                                   data[base_column_name])
    return data


def round_time(data: DataFrame, column_name: str, base_column_name: str,
               frequence: str):
    """
    Rounds the time to the nearest frequence.
    """
    data[column_name] = data[base_column_name].dt.round(frequence)
    return data


def _days_to_int(days):
    return days.dt.dayofweek


def day_of_the_week(data: DataFrame, column_name: str,
                    base_column_name: str):
    """
    Day of the week as integer.
    Monday=0, ..., Sunday=7
    """
    data[column_name] = _days_to_int(data[base_column_name])
    return data


def name_of_the_day(data: DataFrame, column_name: str,
                    base_column_name: str):
    """Day of the week as string: Monday, Tuesday, ..."""
    data[column_name] = data[base_column_name].dt.day_name()
    return data


def convert_timediff_to_unit(data: DataFrame, column_name: str,
                             eventdate_column_name: str,
                             base_column_name: str,
                             unit: str = 's'):
    """
    Time difference eventdate_column_name- base_column_name is converted
    into the choosen unit.
    Default unit is seconds.
    """
    data[column_name] = _time_diff(data[eventdate_column_name],
                                   data[base_column_name]
                                   ) / np.timedelta64(1, unit)
    return data


def _time_diff(t1, t0):
    return t1 - t0


def recenter_time_wrt_t0(data: DataFrame, column_name: str,
                         eventdate_column_name: str,
                         base_column_name: str):
    """
    Time of an event is recentered with respect to a choosen datetime t0.
    E.g. set t0 = admission_time,
    therefore:
         eventtime_recentered= eventtime - t0 .
    """
    data[column_name] = _time_diff(data[eventdate_column_name],
                                   data[base_column_name])
    return data


def recenter_wrt_weekdays_in_unit(data: DataFrame, column_name: str,
                                  eventdate_column_name: str,
                                  base_column_name: str,
                                  unit: str = 's'):
    """
    Time of an event is recentered with respect to a choosen datetime t0,
    the day of the week is added and converted into chosen unit,
    default unit = seconds
    Choose functon to visualize timeseries of several patients to compare with
    the focus on weekdays.
    """
    day_of_week_int = _days_to_int(data[base_column_name])
    data[column_name] = (
                pd.to_timedelta(day_of_week_int, unit='d') +
                _time_diff(data[eventdate_column_name],
                           data[base_column_name])) / np.timedelta64(1, unit)
    return data


def hour(data: DataFrame, column_name: str,
         base_column_name: str):
    """
    Hour of the day as integer.
    """
    data[column_name] = data[base_column_name].dt.hour
    return data


def second(data: DataFrame, column_name: str,
           base_column_name: str):
    """
    second of the datetime in the column_name as integer.
    """
    data[column_name] = data[base_column_name].dt.second
    return data


def round_numeric(data: DataFrame, column_name: str, base_column_name: str,
                  decimals: int):
    """
    Rounds the numeric value to the nearest decimals.
    """
    data[column_name] = data[base_column_name].round(decimals)
    return data


def flag(data: DataFrame, column_name: str, base_column_name: str,
         condition_value: str,  condition_operator: ConditionalOperators):
    """
    Adds a new column to the data frame, which is a flag column.
    The flag is set to 1 if the condition is met, otherwise 0.
    """
    op = getattr(operator, condition_operator.value)
    if condition_value in data.columns:
        condition_value = data[condition_value]
    data[column_name] = 1
    data[column_name] = data[column_name].where(op(
                            data[base_column_name], condition_value), 0)
    return data


def is_element(data: DataFrame, column_name: str, base_column_name: list,
               elements: list[str | int | float]):
    """
    Adds a new column to the data frame, which is a flag column.
    The flag is set to 1 if the element is in the list, otherwise 0.
    """
    data[column_name] = data[base_column_name].isin(elements)
    return data


def operate(data: DataFrame, column_name: str, first_column_name: str,
            second_column_name: str, math_operator: MathOperators):
    """
    Adds a new column to the data frame, which is the result of the
    operation between two columns.
    """
    op = getattr(operator, math_operator.value)
    data[column_name] = op(data[first_column_name],
                           data[second_column_name])
    return data


def maximum(data: DataFrame, column_name: str, column_list: list,
            axis: str):
    """
    Maximium of numerical value or timestamp
    """
    if axis == 'columns':
        data[column_name] = data[column_list].max(axis='columns')
    else:
        data[column_name] = data[column_list].values.max()
    return data


def minimum(data: DataFrame, column_name: str, column_list: list,
            axis: str):
    """ Minimum of numerical value or timestamp """
    if axis == 'columns':
        data[column_name] = data[column_list].min(axis='columns')
    else:
        data[column_name] = data[column_list].values.min()
    return data


def grouped(data: DataFrame, column_name: str, base_column: str,
            group: list, statistical_measure: StatisticalMeasures):
    """
    Adds a new column to the data frame, which is the result of the
    statistical measure of the base column grouped by the group.
    """
    data[column_name] = data.groupby(group)[[base_column]].transform(
        statistical_measure)
    return data


def time_window(data: DataFrame, column_name: str, eventdate_column_name: str,
                base_column_name: str, period: int, time_length: int,
                unit: str):
    """ Time window in which event happened with respect to base column time t0
        (eventdate-date_t0)/period < max_timewindow"""
    data[column_name] = (
            _time_diff(data[eventdate_column_name],
                       data[base_column_name]) /
            (np.timedelta64(1, unit) * period)
        ).astype('int32') + 1
    data[column_name] = data[column_name].where((data[column_name] <
                                                 ((time_length/period)+1)) |
                                                (data[column_name] < 0), 0)
    return data
