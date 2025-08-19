import os
import shutil
from settings import projects_folder

def get_projects() -> list[str]:
    return [
        item
        for item in os.listdir(projects_folder)
        if os.path.isdir(os.path.join(projects_folder, item))
    ]


def create_project(project_id: str) -> bool:
    os.mkdir(os.path.join(projects_folder, project_id))
    return True

def prepare_kitchen(project_id: str) -> bool:
    mlkitchen = os.path.join(projects_folder, project_id, "mlkitchen")
    mlkitchen_prepared = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mlkitchen_prepared")
    shutil.copytree(mlkitchen_prepared, mlkitchen)
    return True


def rename_project(project_id: str, new_project_id: str) -> bool:
    dst = os.path.join(projects_folder, new_project_id)
    if os.path.exists(dst):
        # on UNIX systems existing dst directory is silently replaced if empty
        # https://docs.python.org/3/library/os.html#os.rename
        raise FileExistsError

    os.rename(
        os.path.join(projects_folder, project_id),
        dst,
    )
    return True


def delete_project(project_id: str) -> bool:
    p = os.path.join(projects_folder, project_id)
    shutil.rmtree(p)
    return True
