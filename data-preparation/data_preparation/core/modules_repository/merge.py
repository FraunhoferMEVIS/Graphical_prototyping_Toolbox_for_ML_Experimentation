""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: merge.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 12/2023
description: The module for a merging multiple tables
-----------------------------------------------------------------------------
"""
import logging
from data_preparation.core.modules_repository.base_node import Node, Socket, ModuleConfigParameter
from data_preparation.core.results_repository import \
                ResultsRepository,  FileResultsRepository, ResultTypes


__all__ = ["MergeTables"]
__logger = logging.getLogger(__name__)


class MergeTables(Node):
    """
    Generate a new column based on the input operator and one or more columns.
    """
    NAME = "table-merge"
    DESCRIPTION = "Merges two input tables to one table"
    IN_SOCKETS = [
        {
            "name": "input1",
            "description": "The left table",
            "required": True,
        },
        {
            "name": "input2",
            "description": "The right table",
            "required": True,
        },
    ]
    PARAMETERS = {
        "how": {
            "id": "how",
            "name": "how",
            "description": """The join can be Inner or Outer.""",
            "type": "string",
            "required": False,
            "value": "Inner",
            "allowedValues": {"Inner", "Outer", "Left", "Right"},
        },
        "left_keys": {
            "id": "left_keys",
            "name": "left_keys",
            "description": """The merge is done based on equality of this column/these columns \
                on the left input table, to a corresponding column in the right table.""",
            "type": "string",
            "required": True,
            "value": None,
            "multipleValues": True
        },
        "right_keys": {
            "id": "right_keys",
            "name": "right_keys",
            "description": """The merge is done based on equality of this column/these columns \
                on the right input table, to a corresponding column in the left table.\
                If not given, a same value as the "left_keys" is used.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "left_columns": {
            "id": "left_columns",
            "name": "left_columns",
            "description": """The columns that should be included in the output. If not given, all columns are used. /
                        If an empty list is given, the output merged result won't include any of the columns from the/
                        left table. Left table is then only used to filter the rows in the right table.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "right_columns": {
            "id": "right_columns",
            "name": "right_columns",
            "description": """The columns that should be included in the output. If not given, all columns are used. /
                        If an empty list is given, the output merged result won't include any of the columns from the/
                        right table. Right table is then only used to filter the rows in the right table.""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": True
        },
        "left_postfix": {
            "id": "left_postfix",
            "name": "left_postfix",
            "description": """If both tables have columns with the same name, \
                a postfix will be added to the name of the column, by default, \
                the postfix is the module's id. To have control on the name of \
                the columns, we encourage you to use postfixes..""",
            "type": "string",
            "required": False,
            "value": None,
            "multipleValues": False
        },
        "right_postfix": {
            "id": "right_postfix",
            "name": "right_postfix",
            "description": """If both tables have columns with the same name, \
                a postfix will be added to the name of the column, by default, \
                the postfix is the module's id. To have control on the name of \
                the columns, we encourage you to use postfixes..""",
            "type": "string",
            "required": False,
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
        output_metadadata = {
                'data_type': 'tabular',
                'keys': [], # list of str
                'features': [], # list of dicts
            }
        
        left_keys, right_keys = self._get_joining_keys()
        left_columns, right_columns = self._get_columns()
        left_postfix, right_postfx = self._get_postfixes()

        left_table = self.inputs[0]
        right_table = self.inputs[1]
        if self.inputs and len(self.inputs) >= 2 and left_table and right_table:
            metadata_left = input_metadata[left_table.name]
            metadata_right = input_metadata[right_table.name]

            def get_common_cols(cols_left: list[str], cols_right: list[str]):
                common = []
                for col_name in cols_left:
                    if col_name in cols_right:
                        common.append(col_name)
                return common

            def merge_metadata_and_common(metadata, common_cols, exclude_common=None, postfix=''):
                output_list = []

                for data in metadata:
                    if isinstance(data, dict):
                        # analyzing the features
                        if (col := data['name']) not in common_cols:
                            output_list.append(data)
                        elif exclude_common is None or col not in exclude_common:
                            data["name"] = f"{col}_{postfix}"
                            output_list.append(data)
                    elif data not in common_cols:
                        # analyzing the keys
                        output_list.append(data)
                    elif exclude_common is None or data not in exclude_common:
                        output_list.append(f"{data}_{postfix}")
                    else:
                        output_list.append(data)
                return output_list
            
            def get_metadata_selected_cols(metadata, selected_cols):
                """
                from the input metadata, returns only the ones that are listed in the selected_cols.
                If selected_cols include columns that are not in the metadata, it ignores them.
                """
                if selected_cols is None:
                    return metadata
                selected_metadata = {
                    "keys": [key for key in metadata["keys"] if key in selected_cols],
                    "features": [feature for feature in metadata["features"] if feature["name"] in selected_cols]
                }
                return selected_metadata
            
            def get_feature_names_from_metadata(metadata):
                """
                returns a list of feature names from the input metadata
                """
                return [feature['name'] for feature in metadata['features']]
            
            metadata_left = get_metadata_selected_cols(metadata_left, left_columns)
            metadata_right = get_metadata_selected_cols(metadata_right, right_columns)

            common = get_common_cols(get_feature_names_from_metadata(metadata_left)+metadata_left["keys"],
                            get_feature_names_from_metadata(metadata_right)+metadata_right["keys"])
            output_metadadata["features"] = merge_metadata_and_common(
                    metadata_left["features"], common, exclude_common=left_keys, postfix=left_postfix)
            output_metadadata["features"].extend(merge_metadata_and_common(
                    metadata_right["features"], common, exclude_common=right_keys, postfix=right_postfx))

            output_metadadata["keys"] = merge_metadata_and_common(
                    metadata_left["keys"], common, exclude_common=left_keys, postfix=left_postfix)
            output_metadadata["keys"].extend(merge_metadata_and_common(
                    metadata_right["keys"], common, exclude_common=right_keys, postfix=right_postfx))
            if left_keys:
                output_metadadata["keys"].extend(left_keys)
            if right_keys:
                output_metadadata["keys"].extend(right_keys)
            output_metadadata["keys"] = list(set(output_metadadata["keys"]))
            output_metadadata["features"] = [feature for feature in output_metadadata["features"] \
                                                        if feature["name"] not in output_metadadata["keys"]]
            return output_metadadata

        raise TypeError("Please check that the inputs are connected and the results are ready!")
    
    def _get_joining_keys(self):
        """
        returns the left and right keys sewlected for joining
        """
        left_keys = self.parameters["left_keys"].value
        if isinstance(left_keys, str):
            left_keys = [left_keys]
        right_keys = self.parameters["right_keys"].value
        if isinstance(right_keys, str):
            right_keys = [right_keys]
        if right_keys is None or len(right_keys) == 0:
            right_keys = left_keys

        if len(left_keys) != len(right_keys):
            raise ValueError("The number of keys for the left and right table should be equal.")
        return left_keys, right_keys


    def _get_columns(self):
        def get_union_of_lists(l1, l2):
            result = list(set(l1 + l2))
            return result
        
        left_keys, right_keys = self._get_joining_keys()
        left_columns = self.parameters["left_columns"].value
        if left_columns is not None and len(left_columns) > 0:
            left_columns = get_union_of_lists(left_columns,
                                              left_keys)

        right_columns = self.parameters["right_columns"].value
        if right_columns is not None and len(right_columns) > 0:
            right_columns = get_union_of_lists(right_columns,
                                               right_keys)
        
        return left_columns, right_columns
    
    def _get_postfixes(self):
        left_postfix = self.parameters["left_postfix"].value
        right_postfix = self.parameters["right_postfix"].value
        if left_postfix is None:
            left_postfix = self.inputs[0].value
        if right_postfix is None:
            right_postfix = self.inputs[1].value
        return left_postfix, right_postfix

    def run(self) -> None:
        """
          Implement the logic to add a new column based on the input operator and columns
        """
        super().run()
        
        left_keys, right_keys = self._get_joining_keys()

        left_table_name = self.inputs[0].value
        right_table_name = self.inputs[1].value

        how = self.parameters["how"].value.lower()

        output_meta = self.define_output_metadata(
            input_metadata=self.get_input_metadata())
        self.write_metadata(output_meta)

        left_columns, right_columns = self._get_columns()
        left_postfix, right_postfix = self._get_postfixes()

        try:
            # Read the input file
            for chunk in self._results_repo.get(self.parent_project,
                                                left_table_name,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                if left_columns:
                    chunk = chunk[left_columns]
                for other_chunk in self._results_repo.get(self.parent_project,
                                                right_table_name,
                                                ResultTypes.DATAFRAME,
                                                chunksize=self._CHUNKSIZE):
                    if right_columns:
                        other_chunk = other_chunk[right_columns]
                    result = chunk.merge(other_chunk,
                                         left_on=left_keys,
                                         right_on=right_keys, 
                                         how=how,
                                         suffixes=(f'_{left_postfix}', f'_{right_postfix}'))
                    if not self.write_output(result):
                        raise IOError(f"Failed to write output for module {self.NAME}")                
                self.valid_results = True
        except IOError as e:
            self.error_message = f"Failed to write output for module {self.NAME}"
            __logger.error(self.error_message)
            raise IOError(self.error_message) from e
        except NameError as e:
            self.error_message = f"The column is not part of the data (module {self.NAME}): {e}."
            __logger.error(self. error_message)
            raise NameError(self.error_message) from e
        except Exception as e:
            __logger.error("Failed to merge tables: %s", e)
            raise Exception(f"Failed to merge tables: {e}") from e
