""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: utils.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 06/2024
description: The functions and class utilities that could be used by all modules
-----------------------------------------------------------------------------
"""
import os
import logging
import re
from math import (inf, pi, nan, e,
                  ceil, floor, log, sqrt, sin, cos, tan, acos, asin, atan
                )
from random import randint, random
from datetime import datetime, timedelta
from numpy import isnan
from dateutil import parser
from simpleeval import simple_eval


__logger = logging.getLogger(__name__)


def remove_file_if_exists(filepath: str):
    """
    Removes the input file, if it exists.
    If it doesn't, it doesn't do anything.
    """
    if os.path.exists(filepath):
        os.remove(filepath)


def validate_expression_code(expression: str,
                             sample_inputs: tuple | list):
    """
    Valdates the input expression. Example valid expressions are:
        floor(e ** (pow(x1, 5) + pi))
        ceil(pow(e, x1+x2)) < 10
    :param: expression: a string for a mathematical expression. \
            The input params are represented as x1, x2, x3, ....
    :param: sample_inputs: the sample inputs of the expression.
            They can come from the input data columns.
    """
    sample_inputs = {f"x{i+1}": inp for i, inp in enumerate(sample_inputs)}
    try:
        get_expression_function(expression, len(sample_inputs))(**sample_inputs)
        return True
    except SyntaxError as syntax_error:
        __logger.error("""Syntax Error in expression, %s:
                            %s""", expression, syntax_error)
        raise SyntaxError from syntax_error
    except Exception as exception:
        __logger.error("""Error in expression, %s:
                         %s""", expression, exception)
        raise Exception from exception


def parse_time(input_str: str) -> datetime:
    """
    Parses the input str and returns the datetime format of it.
    """
    return parser.parse(input_str)


def get_expression_function(expression: str, num_inputs: int) -> callable:
    funcs = {
        "ceil": ceil,
        "floor": floor,
        "log": log,
        "sqrt": sqrt,
        "pow": pow,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "acos": acos,
        "asin": asin,
        "atan": atan,
        "randint": randint,
        "random": random,
        "time": parse_time,
        "isnan": isnan,
        "timedelta": timedelta
    }
    consts = {
        "inf": inf,
        "pi": pi,
        "nan": nan,
        "e": e
    }
    expression = clean_expression(expression)
    if num_inputs == 0:
        return lambda: simple_eval(expression,
                                 functions=funcs,
                                 names=consts)
    if num_inputs == 1:
       return lambda x1: simple_eval(expression,
                                 functions=funcs,
                                 names= consts | {
                                     "x1": x1,
                                 })
    if num_inputs == 2:
        return lambda x1, x2: simple_eval(
                                 expression,
                                 functions=funcs,
                                 names= consts | {
                                     "x1": x1,
                                     "x2": x2,
                                 })
    if num_inputs == 3:
        return lambda x1, x2, x3: simple_eval(
                                 expression,
                                 functions = funcs,
                                 names = consts | {
                                     "x1": x1,
                                     "x2": x2,
                                     "x3": x3,
                                 })
    if num_inputs == 4:
        return lambda x1, x2, x3, x4: simple_eval(
                                 expression,
                                 functions = funcs,
                                 names = consts | {
                                     "x1": x1,
                                     "x2": x2,
                                     "x3": x3,
                                     "x4": x4,
                                 })
    if num_inputs == 5:
        return lambda x1, x2, x3, x4, x5: simple_eval(
                                 expression,
                                 functions = funcs,
                                 names = consts | {
                                     "x1": x1,
                                     "x2": x2,
                                     "x3": x3,
                                     "x4": x4,
                                     "x5": x5,
                                 })
    raise ValueError("Too many inputs! Currently, we don't support more than 5 number of inputs.")


def clean_expression(expression):
    # Define the regex pattern to match 'x1 == nan' or 'x1 is nan' with optional whitespaces
    pattern_equal = r'\b(x[1-5])\s*(==|is)\s*nan\b'
    pattern_not_equal = r'\b(x[1-5])\s*(!=|is\s+not)\s*nan\b'
    
    # Replace the matched pattern with 'isnan(x1)'
    expression = re.sub(pattern_equal, r'isnan(\1)', expression)
    # Replace the matched pattern with 'not isnan(x1)'
    expression = re.sub(pattern_not_equal, r'not isnan(\1)', expression)
    return expression
