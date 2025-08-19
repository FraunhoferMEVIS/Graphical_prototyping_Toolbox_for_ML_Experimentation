import json
import os
import csv
import yaml
import pandas as pd

from project import *
from typing import List
from datetime import datetime
from pydantic import BaseModel
from settings import projects_folder


class Export(BaseModel):
    project: str
    app: str
    date: str
    content: dict


def get_progress(project_id: str, tool_id: str):
    project_folder = os.path.join(projects_folder, project_id)
    if os.path.isdir(os.path.join(project_folder, tool_id)):
        if "export.json" in os.listdir(os.path.join(project_folder, tool_id)):
            return {"status": "finished"}
        else:
            return {"status": "in_progress"}
    return {"status": "unused"}


def create_export(project_id: str, source_tool: str, target_tool: str, export_file):
    if project_id not in get_projects():
        create_project(project_id)
    new_folder = os.path.join(projects_folder, project_id, source_tool)
    try:
        os.mkdir(new_folder)
    except:
        print("Error while creating export folder.")
        return False
    export: Export = {
        "project": project_id,
        "source_app": source_tool,
        "target_app": target_tool,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "content": export_file,
    }
    with open(os.path.join(new_folder, "export.json"), "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=4)
    return True


def save_file(project_id: str, app_name: str, file_name: str, file_content: dict):
    if project_id not in get_projects():
        create_project(project_id)
    new_folder = os.path.join(projects_folder, project_id, app_name)
    try:
        os.makedirs(new_folder, exist_ok=True)
    except:
        print("Error while creating export folder.")
        return False

    base_name, extension = os.path.splitext(file_name)

    try:
        with open(os.path.join(new_folder, file_name), "w", encoding="utf-8") as f:
            if extension == ".json":
                json.dump(file_content, f, ensure_ascii=False, indent=4)
            elif extension == ".txt":
                f.write(file_content)
            elif extension == ".csv":
                writer = csv.writer(f)
                for row in file_content:
                    writer.writerow(row)
            elif extension == ".yaml" or extension == ".yml":
                yaml.dump(file_content, f, default_flow_style=False)
            else:
                print("Unsupported file extension.")
                return False
    except:
        print("Error while saving file.")
        return False

    return True


def load_file(project_id: str, app_name: str, file_name: str):
    folder = os.path.join(projects_folder, project_id, app_name)
    if not os.path.exists(folder):
        print("Folder does not exist.")
        return {}

    base_name, extension = os.path.splitext(file_name)

    with open(os.path.join(folder, file_name), "r", encoding="utf-8") as f:
        if extension == ".json":
            return json.load(f)
        elif extension == ".txt":
            return f.read()
        elif extension == ".csv":
            reader = csv.reader(f)
            return [row for row in reader]
        elif extension == ".yaml" or extension == ".yml":
            return yaml.safe_load(f)
        else:
            print("Unsupported file extension.")
            return {}


def get_project_data(project_id) -> List[str]:
    data_folder = os.path.join(projects_folder, project_id, "data")
    print(os.listdir(data_folder))
    return [
        item
        for item in os.listdir(data_folder)
        if not os.path.isdir(os.path.join(data_folder, item))
    ]


def load_parquet(project_id: str, file_name: str) -> List[dict]:
    base_name, extension = os.path.splitext(file_name)
    if extension != ".parquet":
        print("Unsupported file extension.")
        return {}
    file_path = os.path.join(projects_folder, project_id, "data", file_name)
    try:
        df = pd.read_parquet(file_path)
        return df.fillna("").to_dict(orient="records")
    except:
        print("Error while loading Parquet file.")
        return {}


def save_parquet(project_id: str, file_name: str, file_content: dict):
    base_name, extension = os.path.splitext(file_name)
    if extension != ".parquet":
        print("Unsupported file extension.")
        return False

    if project_id not in get_projects():
        create_project(project_id)
    new_folder = os.path.join(projects_folder, project_id, "data")
    try:
        os.makedirs(new_folder, exist_ok=True)
    except:
        print("Error while creating export folder.")
        return False

    with open(os.path.join(new_folder, file_name), "wb") as f:
        df = pd.DataFrame(file_content)
        df.to_parquet(os.path.join(new_folder, file_name))

    return True
