""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: project.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The main class, defining the mlflow project
-----------------------------------------------------------------------------
"""

import os
import shutil
import datetime
import logging
from glob import glob
from copy import deepcopy
from pydantic import BaseModel
from fastapi import UploadFile
from src.models.recipe import StepConfig
from methods_repository.config_models import RecipeConfig
from .methods_list import Steps
from .translators import Translator
from .app_config import AISANDBOX_PROJECTS_FOLDER, AISANDBOX_TRACKING_URI, \
                        AISANDBOX_ARTIFACTS_FOLDER, DATA_PROVIDER_URL
from .utilities import save_config_to_yaml, load_yaml, handle_requests, \
                       get_largest_file_number_in_path, load_json


_logger = logging.getLogger(__name__)


class Project(BaseModel):
    """
    Project class to generate a project for mlflow
    """
    name: str

    def create(self, conf: RecipeConfig):
        response = {}
        if not self.__exists():
            response["message"] = \
                f"{self.name} does not exist, creating one ..."
        else:
            response["message"] = \
                f"{self.name} already exists, replacing the configuration ..."
        self._setup_folders()
        cookbook = CookBook(project_name=self.name)
        cookbook.build(conf)
        return response

    def __project_path(self) -> str:
        """
        returns the project's path
        """
        return os.path.join(AISANDBOX_PROJECTS_FOLDER, self.name)

    def __mlkitchen_path(self) -> str:
        """
        returns the mlkitchen path of the project.
        """
        return os.path.join(self.__project_path(), "mlkitchen")

    def translate_mlops_to_user_config(self) -> RecipeConfig:
        """
        generate a configuration from the mlops. For documentation reasons.
        """

    def add_step(self, step: StepConfig):
        """
        Add a step to the project.
        """

    def delete_step(self, step: StepConfig):
        """"
        delete a step from the project
        """

    def edit_step(self, step: StepConfig):
        """
        edit the settings for a given step
        """

    def run_step(self, step: Steps, algs: StepConfig):
        """
        Run only a specific step
        """

    def get_job_status(self):
        """
        What is the current job status?
        """
        if not self.__exists():
            return {"Status": f"{self.name} project does'nt exist."}
        call_history_folder = os.path.join(self.__mlkitchen_path(),
                                           "call_history"
                                           )
        current_call_number = get_largest_file_number_in_path(
            call_history_folder)
        if current_call_number < 0:
            return {
                "Status": "no execution history",
            }
        runs_info = {}
        for run in os.listdir(os.path.join(call_history_folder, str(current_call_number))):
            TOTAL_TIME = 100 # currently set, can be calculated
            submit_time = None
            run_filename = os.path.join(call_history_folder,
                                        str(current_call_number),
                                        run)
            run_name = ''.join(run.split(".")[:-1])
            if not run_filename.endswith(".json"):
                continue
            try:
                current_run_info = load_json(run_filename)
            except Exception as e:
                print(f"Error loading JSON from {run_filename}: {e}")
                continue

            if "SubmitTime" in current_run_info and current_run_info["SubmitTime"]:
                submit_time = datetime.datetime.fromtimestamp(int(current_run_info["SubmitTime"][0:10]))
                current_run_info["SubmitTime"] = submit_time.strftime("%Y-%m-%d %H:%M:%S")

            runs_info[run_name] = {info: current_run_info.get(info, "") for info in ("Status", "SubmitTime", "out_log", "error_log")}
            
            # Update progress based on status and submit time
            if runs_info[run_name]["Status"] == "pending":
                runs_info[run_name]["Progress"] = 0
            elif runs_info[run_name]["Status"] == "running":
                if submit_time is not None:
                    time_passed = (datetime.datetime.now() - submit_time).total_seconds()
                    runs_info[run_name]["progress"] = max(0, min(99, int(time_passed / TOTAL_TIME * 100)))
                else:
                    runs_info[run_name]["progress"] = 0
            else:
                if "error_log" not in runs_info[run_name] or "error:" in runs_info[run_name]["error_log"].lower():
                    runs_info[run_name]["Status"] = "failed"
                else:
                    runs_info[run_name]["Status"] = "finished"
                runs_info[run_name]["Progress"] = 100

        return runs_info

    def get_results(self):
        """
        Get an overview of the results
        """

    def create_report(self):
        """
        Generate a report from the project and the results.
        """

    def get_report(self):
        """
        Get final report after running the whole recipe
        """

    def get_missing_mandatory_steps(self) -> dict:
        """
        What are the mandatory steps that are not defined yet
        """

    def _setup_folders(self) -> None:
        project_folder = self.__project_path()
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
        working_dir = self.__mlkitchen_path()
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        for folder in ("data", "cookbook_archive", "call_history"):
            if not os.path.exists(os.path.join(working_dir, folder)):
                os.mkdir(os.path.join(working_dir, folder))

    def __exists(self) -> bool:
        return os.path.exists(self.__mlkitchen_path())

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "sample_project"
                }
            ]
        }
    }

    def receive_file(self, file: UploadFile):
        if not file.filename.endswith('.parquet'):
            raise ValueError("The file should be in 'parquet' format.")
        data_foler = os.path.join(self.__mlkitchen_path(), 'data')
        if not os.path.exists(data_foler):
            self._setup_folders()
        data_path = os.path.join(data_foler, 'data.parquet')
        with open(data_path, "wb+") as fid:
            shutil.copyfileobj(file.file, fid)    


class CookBook():
    """
    A class to keep track of all recipes in a project
    """
    def __init__(self, project_name: str):
        self.name = project_name
        self._project_path = os.path.join(AISANDBOX_PROJECTS_FOLDER,
                                          self.name, 'mlkitchen')
        if not os.path.exists(self._project_path):
            raise KeyError(f"Project: '{self.name}' does not exist!")
        self.__previous = self.get_config()['previous']
        for folder in ("data", "cookbook_archive", "call_history"):
            if not os.path.exists(os.path.join(self._project_path, folder)):
                os.mkdir(os.path.join(self._project_path, folder))

    def get_config(self) -> RecipeConfig:
        """
        Loads and returns the cookbook configuration of a given project.
        """
        cookbook_file = os.path.join(self._project_path, "cookbook.yaml")
        if os.path.exists(cookbook_file):
            return load_yaml(cookbook_file)
        return {'previous': -1}

    def build(self, config: RecipeConfig):
        """
        Builds a cookbook that contains recipes based on the input
        config and saves the input config to MLFLOW recipes.
        :config: a RecipeConfig containing all the project configuration
        """
        _logger.info("saving the user input as mlops configs.")

        estimators = config.estimator
        if not isinstance(estimators, list):
            estimators = [estimators]
        primaryMetrics = config.primaryMetric
        if not isinstance(primaryMetrics, list):
            primaryMetrics = [primaryMetrics]

        self._archive_cookbook()
        new_cookbook = config.to_yaml_dict()
        new_cookbook['previous'] = self.__previous
        save_config_to_yaml(new_cookbook,
                            os.path.join(self._project_path,
                                         "cookbook.yaml"))
        n = 1
        self._cleanup_old_recipes()
        for estimator in estimators:
            for primaryMetric in primaryMetrics:
                current_recipe_path = os.path.join(self._project_path,
                                                   f'run{n}')
                current_recipe_config = deepcopy(config)
                current_recipe_config.estimator = estimator
                current_recipe_config.primaryMetric = primaryMetric
                if not os.path.exists(current_recipe_path):
                    os.makedirs(current_recipe_path)
                self._setup_folders(current_recipe_path)
                translator = Translator.use_recipe(
                    current_recipe_config,
                    self.name,
                    current_recipe_path
                )
                translator.config_to_recipe(current_recipe_config)
                n += 1

    def save_recipe_profiles(self):
        num_splits = self.get_num_splits()
        for recipe in self.get_list_of_recipes():
            for split_number in range(num_splits):
                self._save_profile(recipe, str(split_number))

    def get_list_of_recipes(self):
        return glob(os.path.join(self._project_path, 'run*'))

    def is_new_split_needed(self) -> bool:
        """
        Checks of ot os required to make a new split or not,
        based on the configuration changes and existing files.
        """
        resp = handle_requests(
                    url=f'{DATA_PROVIDER_URL}/{self.name}/split_exist',
                    method="GET")
        if not resp['exists']:
            return True
        current_cookbook = self.get_config()
        if 'previous' in current_cookbook:
            previous = current_cookbook['previous']
        else:
            return True
        previous_cookbook_path = os.path.join(
            self._project_path, "cookbook_archive",
            f"cookbook{previous}.yaml")
        if os.path.exists(previous_cookbook_path):
            previous_cookbook = load_yaml(previous_cookbook_path)
        else:
            return True
        if 'split' in current_cookbook and 'split' in previous_cookbook and \
                current_cookbook['split'] == previous_cookbook['split']:
            return False
        return True

    def _cleanup_old_recipes(self):
        recipes = glob(os.path.join(self._project_path,
                                    'run*'))
        for recipe in recipes:
            shutil.rmtree(recipe)

    def _setup_folders(self, recipe_folder) -> None:
        for folder in ("steps", "profiles", "data"):
            if not os.path.exists(os.path.join(recipe_folder, folder)):
                os.makedirs(os.path.join(recipe_folder, folder))

        shutil.copyfile(
            os.path.join(os.path.abspath('.'), 'src', 'backend',
                         'project_run_files', 'requirements.txt'),
            os.path.join(recipe_folder, 'requirements.txt'))
        shutil.copyfile(
            os.path.join(os.path.abspath('.'), 'src', 'backend',
                         'project_run_files', 'run_experiment.sh'),
            os.path.join(recipe_folder, 'run_experiment.sh'))
        shutil.copyfile(
            os.path.join(os.path.abspath('.'), 'src', 'backend',
                         'project_run_files', 'save_output.py'),
            os.path.join(recipe_folder, 'save_output.py'))

    def _save_profile(self, recipe_folder, split_number) -> None:
        _logger.info("Saving the profile")
        run_name = self.get_run_name(recipe_folder, split_number)
        profile = {
            "experiment": {
                "name": self.name,
                "run_name_prefix": run_name,
                "tracking_uri": AISANDBOX_TRACKING_URI,
                "artifact_location": AISANDBOX_ARTIFACTS_FOLDER
            },
            "model_registry": {
                "model_name": f"{self.name}"
            },
        }
        save_config_to_yaml(
            profile,
            os.path.join(recipe_folder,
                         'profiles',
                         f'{run_name}.yaml'))

    def get_run_name(self, recipe: str, split_number: int) -> str:
        """
        defines a representative name for the experiment, based on the input
        recipe and the fold number
        : recipe: path to the recipe.yaml file
        : split_number: the fold number
        """
        name_array = []
        recipe_config = load_yaml(os.path.join(recipe, 'recipe.yaml'))
        if "target_col" in recipe_config:
            name_array.append(recipe_config['target_col'])
        if "steps" in recipe_config and "train" in recipe_config["steps"] and \
                "estimator_method" in recipe_config["steps"]["train"]:
            name_array.append(
                recipe_config['steps']['train']['estimator_method'][10:])
        if 'primary_metric' in recipe_config:
            name_array.append(recipe_config['primary_metric'])
        num_splits = self.get_num_splits()
        if split_number and num_splits > 1:
            name_array.append(f"fold{split_number}of{num_splits}")
        return '_'.join(name_array)

    def _archive_cookbook(self):
        current_cookbook = self.get_config()
        self.__previous = current_cookbook['previous'] + 1
        if os.path.exists(os.path.join(self._project_path, "cookbook.yaml")):
            shutil.move(os.path.join(self._project_path, "cookbook.yaml"),
                        os.path.join(self._project_path, "cookbook_archive",
                                     f"cookbook{self.__previous}.yaml"))

    def _perform_data_split(self):
        """
        This method will split the data based on the input config file and
        save the indices in the "data" folder of the relevant recipe.
        In case of using the same split for all recipes, the same indices
        are saved for all of them. But for cross validation, leave one out,
        etc. the method will take care of these splits and indices of each
        individual recipe.
        """
        resp = handle_requests(url=f'{DATA_PROVIDER_URL}/{self.name}/split',
                               method="POST",
                               request_json=self.get_config())
        return resp

    def get_num_splits(self):
        resp = handle_requests(
            url=f'{DATA_PROVIDER_URL}/{self.name}/num_folds',
            method="GET")
        return int(resp['num_folds'])
