""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: features.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: The models defined for the features endpoints of the api
-----------------------------------------------------------------------------
"""

from typing import List, Union
from enum import Enum
from pydantic import BaseModel


class FeatureTypes(str, Enum):
    """
    Different type of features that we support
    """
    key = "key"
    numerical = "numerical"
    categorical = "categorical"
    time = "time"
    data = "date"
    interval = "interval"
    text = "text"
    image = "image"
    signal = "signal"
    other = "other"
    # video: 'video'

class DataTypes(str, Enum):
    """
    supported data types
    """
    tabular = "tabular"


# class Units(str, Enum):
#     # time units
#     msec: 'msec'
#     second: 'second'
#     minute: 'minute'
#     hour: 'hour'
#     day: 'day'
#     week: 'week'
#     month: 'month'
#     year: 'year'
#     decade: 'decade'
#     # length units
#     nanometre: 'nanometre'
#     macrometre: 'macrometre'
#     milimetre: 'milimetre'
#     centimetre: 'centimetre'
#     metre: 'metre'
#     kilometre: 'kilometre'
#     inch: 'inch'
#     foot: 'foot'
#     yard: 'yard'
#     mile: 'mile'
#     # area units
#     mm2: 'mm2'
#     cm2: 'cm2'
#     m2: 'm2'
#     ha: 'ha' # hectare
#     acre: 'acre'
#     # volume units
#     mm3: 'mm3'
#     cm3: 'cm3'
#     m3: 'm3'
#     litre: 'litre'
#     dl: 'dl'
#     ml: 'ml'
#     cc: 'cc'
#     oz: 'oz'
#     # Weight units
#     mg: 'mg'
#     grams: 'grams'
#     kg: 'kg'
#     lbs: 'lbs'
#     # temprature units
#     C: 'C' # °C centigrade
#     F: 'F' # °F Fahrenheit
#     # energy units
#     cal: 'cal'
#     Kcal: 'Kcal'
#     kJ: 'kJ'
#     # other units
#     percent: 'percent'
#     degree: 'degree'
#     bpm: 'bpm'  # beat per min
#     cmH2O: 'cmH2O'
#     cmH2O_L_seconds: 'cmH2O_L_seconds'
#     dose: 'dose'
#     dynes_sec_cm5: 'dynes_sec_cm5' # dynes*sec/cm5
#     dynes_sec_cm5_m2: 'dynes_sec_cm5_m2' # dynes*sec/cm5/m2
#     g_dl: 'g_dl' #  g/dl
#     insp_min: 'insp_min' # insp/min
#     InternationalUnits: 'InternationalUnits'
#     mmHg: 'mmHg'
#     mlSC: 'mlSC'
#     mL_min_m2: 'mL_min_m2' # mL/min/m2
#     mL_min: 'mL_min' # mL/min
#     mL_m2: 'mL_m2' # mL/m2
#     mL_hr: 'mL_hr' # mL/hr
#     mL_beat: 'mL_beat' # mL/beat
#     _min: '_min' # /min
#     mg_hour: 'mg_hour' # mg_hour
#     mA: 'mA'


class Feature(BaseModel):
    """
    Feature Configuration
    What are the best descriptors of a Feature
    """
    name: str
    displayName: Union[str, None] = None
    type: FeatureTypes
    loader: Union[str, None] = None
    min: Union[int, float, None] = None
    max: Union[int, float, None] = None
    unique: Union[bool, None] = None

    def to_yaml_dict(self):
        result = {
            'name': self.name,
            'type': self.type.name,
        }
        if self.displayName:
            result['displayName'] = self.displayName
        if self.loader:
            result['loader'] = self.loader
        if self.min:
            result['min'] = self.min
        if self.max:
            result['max'] = self.max
        if self.unique:
            result['unique'] = self.unique
        return result
    # unit: Units | None  # does it make sense to support units?


# class Keys(BaseModel):
#     """
#     The keys configuration
#     """
#     name: str
#     displayName: str = None
#     unique: Union[bool, None] = None


class MetadataModel(BaseModel):
    """
    The model for metadata 
    """
    data_type: list[DataTypes]
    keys: list[str]
    target: str
    features: list[Feature]

    def to_yaml_dict(self):
        result = {}
        result['data_type'] = [data_type.name for data_type in self.data_type]
        result["target"] = self.target
        result['keys'] = [key for key in self.keys]
        result['features'] = [
            feature.to_yaml_dict()
            for feature in self.features
        ]
        return result


class NewFeatureConfig(Feature):
    """"
    Configuration for defining new features.
    """
    method: str
    input_features: Union[List[str], None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "icu_stay_duration",
                "type": "numerical",
                "method": "duration",
                "input_features": ["ICU_intime", "ICU_outtime"]
            }]
        }
    }
