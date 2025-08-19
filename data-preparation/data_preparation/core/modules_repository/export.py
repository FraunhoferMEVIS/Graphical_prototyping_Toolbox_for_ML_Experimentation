""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: export.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 08/2024
description: The module for exporting data to mlkitchen and datadescriptor
-----------------------------------------------------------------------------
"""
import os
from statistics import mean, stdev, quantiles 
import logging
import requests
from pandas import DataFrame
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes
from data_preparation.core.modules_repository.utils import remove_file_if_exists
from data_preparation.core.app_config import (
            DATA_DESCRIPTOR_URL, AISANDBOX_URL, DATA_PREPARATION_PROJECTS_FOLDER)


__all__ = ["Export"]
_logger = logging.getLogger(__name__)

_REGRESSION_TASK = 'regression'
_CLASSIFICATION_TASK = 'classification'
_UNKNOWN_TASK = 'unknown'

class Export(Node):
    """
    Exports the table and the metadata for the use by other tools.
    """
    NAME = "export"
    DESCRIPTION = "Exports the table and the metadata for the use by other tools"
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The input table to export.",
            "required": True,
        },
    ]
    OUT_SOCKETS = []
    PARAMETERS = {
        'target': {
            'id': 'target',
            'name': 'target',
            'type': 'string',
            'description': '''The name if the column that will be used as target in \
                the training and prediction process.''',
            "required": True,
            "value": None,
            "multipleValues": False
        }
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

    def define_output_metadata(self, input_metadata: dict = None) -> dict:
        """
        Defines the output metadata, based on the input metadata and the target.
        This metadata will be exported to the data descriptor
        """
        metadata = input_metadata[self.inputs[0].name]
        metadata['data_type'] = ['tabular']
        metadata['target'] = self.parameters['target'].value
        return metadata
    
    def run(self) -> None:
        """
          Implement the logic for exporting the data
        """
        super().run()
        # save file as parquet
        try:
            tmp_parquet_file = f'{DATA_PREPARATION_PROJECTS_FOLDER}/{self.parent_project}/data.parquet'
            self._convert_input_table_to_parquet(output_file=tmp_parquet_file)
            self.valid_results = True
            
            resp_ai_sandbox = resp_data_desc = resp_proj_mngr = None
            # post the parquet file to aisandbox
            if AISANDBOX_URL is not None:
                with open(tmp_parquet_file, 'rb') as fid:
                    resp_ai_sandbox = requests.post(f'{AISANDBOX_URL}/data/{self.parent_project}/file',
                                files={'file': fid}, timeout=300)
            # post the metadata to DataDescriptor
            if DATA_DESCRIPTOR_URL is not None:
                metadata = self.define_output_metadata(
                    input_metadata=self.get_input_metadata()
                )
                resp_data_desc = requests.post(f'{DATA_DESCRIPTOR_URL}/config/{self.parent_project}',
                            json=metadata, timeout=300)
            
            if resp_ai_sandbox and resp_ai_sandbox.status_code >= 400:
                raise Exception(f"Problem with exporting the data to mlkitchen: {resp_ai_sandbox.text}")
            if resp_data_desc and resp_data_desc.status_code >= 400:
                raise Exception(f"Problem with exporting the data to mlkitchen. Please make sure that the AI-Sandbox is running. {resp_data_desc.text}.")
            if resp_proj_mngr and resp_proj_mngr.status_code >= 400:
                raise Exception(f"Problem with updating the project status in the project manager: {resp_proj_mngr.text}")
        except IOError as e:
            self.error_message = f"Failed to write data for module {self.NAME}: {e}"
            _logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            _logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except Exception as e:
            _logger.error("Failed to export data: %s", e)
            raise Exception(f"Failed to export data (module {self.NAME}): {e}") from e
        finally:
            # cleanup the tmp file
            remove_file_if_exists(tmp_parquet_file)

    def _get_task_type(self) -> str:
        """
        returns the task type, based on the input target column.
        The task type is either classification or regresison
        """
        metadata = self.define_output_metadata(
                input_metadata=self.get_input_metadata()
            )
        if (target := metadata['target']) in metadata['keys']:
            return 'classification'
        for feature in metadata['features']:
            if target == feature['name']:
                if feature['type'] == 'numerical':
                    return _REGRESSION_TASK
                if feature['type'] == 'categorical':
                    return _CLASSIFICATION_TASK
                return _UNKNOWN_TASK
        raise ValueError(f"The selected target, {target} is not part of the input!")

    def _convert_input_table_to_parquet(self, output_file: str):
        # remove the file if it exists from previous exports:
        remove_file_if_exists(output_file)
        target_col = self.parameters['target'].value
        target_vals = []
        num_features = 0
        
        no_nan_features = no_nan_target = no_rows_with_missing_values = 0
        for chunk in self._results_repo.get(self.parent_project,
                                            self.inputs[0].value,
                                            ResultTypes.DATAFRAME,
                                            chunksize=self._CHUNKSIZE):
            if target_col not in chunk.columns:
                raise ValueError(f'The selected column, {target_col} not found in the input table.')

            num_features = max(num_features, len(chunk.columns)-1)
            target_vals.extend(list(chunk[target_col]))

            no_nan_features += chunk.dropna(subset=[target_col]).isna().sum().sum()
            no_nan_target += chunk[target_col].isna().sum()
            no_rows_with_missing_values += chunk.isnull().any(axis=1).sum()

            append = os.path.exists(output_file)
            chunk.to_parquet(output_file,
                                engine='fastparquet',
                                compression='snappy',
                                append=append)
        
        metadata = self.get_input_metadata()['input1']
        # Stats:
        # number of rows
        # number of features
        # for numerical target:
        #   min, max, avg, std, percentile 25, 50, 75
        # for categorical target:
        #   num categories, different values, num rows per category
       
        num_features_categorical = num_features_numerical = 0
        
        for feature in metadata['features']:
            if feature['type'] == 'numerical':
                num_features_numerical += 1
            elif feature['type'] == 'categorical' and feature['name'] != target_col and feature['name'] not in metadata['keys']:
                num_features_categorical += 1

        num_features_categorical += len(metadata['keys'])

        stats = {
            "data_modality": "tabular",
            "target_variable": [target_col],
            "task_type": [self._get_task_type()],
            "n_observations": [len(target_vals)],
            "n_features": [num_features],
            "n_features_categorical": [num_features_categorical],
            "n_features_numeric": [num_features_numerical],
            "na_ratio_features_values": [no_nan_features/len(target_vals)],
            "na_ratio_features_obs": [no_rows_with_missing_values/len(target_vals)],
            "na_ratio_target": [no_nan_target/len(target_vals)],
            "contains_na_only_in_outcome": [no_nan_target > 0 and no_nan_features == 0]
        }
        if stats['task_type'][0] == _REGRESSION_TASK:
            stats['min'] = [min(target_vals)]
            stats['max'] = [max(target_vals)]
            stats['avg'] = [mean(target_vals)]
            stats['stdev'] = [stdev(target_vals)]
            quantile = quantiles(target_vals, n=4)
            stats['percentile25'] = [quantile[0]]
            stats['percentile50'] = [quantile[1]]
            stats['percentile75'] = [quantile[2]]
        elif stats['task_type'][0] == _CLASSIFICATION_TASK:
            categories = sorted(list(set(target_vals)), reverse=True)
            stats['n_classes'] = [len(categories)]
            class_distribution = []
            for cat in categories:
                stats[f'category_{cat}'] = [len([v for v in target_vals if v==cat])]
                class_distribution.append(f"{stats[f'category_{cat}'][0]/len(target_vals):.3f}")
            stats['class_distribution'] = [";".join(class_distribution)]
        self.write_output(DataFrame.from_dict(stats), append=False)


def _dataframe_to_dict(df: DataFrame) -> dict:
    """
    Converts a DataFrame to a dictionary
    """
    result = {}
    for col in df.columns:
        val = df[col].tolist()
        if len(val) == 1:
            val = val[0]
        result[col] = val
    
    return result