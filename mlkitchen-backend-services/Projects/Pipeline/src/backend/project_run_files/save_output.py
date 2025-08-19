""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: .py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: Predicting and Saving the Prediction Results + Groundtruth
-----------------------------------------------------------------------------
"""

import os
from pandas import DataFrame
from mlflow.recipes import Recipe
from mlflow import MlflowException


profile = os.getenv("MLFLOW_RUN_NAME", "local")
recipe = Recipe(profile=profile)

model = recipe.get_artifact("model")
if not model:
    raise MlflowException(
        "There is no model saved for this run, Check the logs.")

run_artifact = recipe.get_artifact('run')
output_path = run_artifact.info.artifact_uri
if not output_path or not os.path.exists(output_path):
    raise IOError("No artifact was saved for this run")

output_path = os.path.join(output_path, "evaluate", "outputs")

step_train = recipe._get_step("train")
target_col = step_train.step_config.get("target_col")

if not os.path.exists(output_path):
    os.makedirs(output_path)

for evaluation_group in ("validation", "test"):
    data = recipe.get_artifact(f"{evaluation_group}_data")

    X = data.drop(columns=[target_col])
    y = data[target_col]

    prediction = model.predict(X)
    if isinstance(prediction, DataFrame):
        prediction["ground_truth"] = y
    else:
        prediction = {"prediction": prediction, "grount_truth": y}
        prediction = DataFrame(prediction)

    if id_field := os.environ.get("ID_FIELD"):
        prediction[id_field] = data[id_field]
        prediction.set_index(id_field, inplace=True)
    elif "subject_id" in data.columns:
        prediction["subject_id"] = data["subject_id"]
        prediction.set_index("subject_id", inplace=True)

    prediction.to_csv(os.path.join(output_path, f"{evaluation_group}.csv"))
