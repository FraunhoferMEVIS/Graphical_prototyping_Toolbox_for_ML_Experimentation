import os
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import project as project_service
from typing import Optional
from export import *
from settings import api_version, projects_folder, root_path


tags_metadata = []

app = FastAPI(
    title="AI Sandbox Project Manager",
    description="",
    version=api_version,
    openapi_tags=tags_metadata,
    root_path=root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(projects_folder, exist_ok=True)


class Project(BaseModel):
    """API representation of a project."""
    id: str


@app.get("/")
def alive():
    return "AI Sandbox Project Manager is alive"


@app.get("/list", deprecated=True)
def get_projects() -> list[str]:
    """Deprecated enpdoint to fetch projects."""
    # TODO: remove this once the old demo is not used anymore.
    return project_service.get_projects()


@app.get("/projects", tags=["projects"])
def get_projects() -> list[str]:
    return project_service.get_projects()


@app.post("/projects", tags=["projects"])
def create_project(project: Project) -> bool:
    try:
        return project_service.create_project(project.id)
    except FileExistsError:
        raise HTTPException(
            status_code=400, detail=f"Project '{project.id}' already exists"
        )

@app.get("/prepare_kitchen/{project_id}", tags=["projects"])
def prepare_kitchen(project_id: str) -> bool:
    return project_service.prepare_kitchen(project_id)

@app.put("/projects/{project_id}", tags=["projects"])
def update_project(project_id: str, project: Project) -> bool:
    try:
        return project_service.rename_project(
            project_id=project_id, new_project_id=project.id
        )
    except FileExistsError:
        raise HTTPException(
            status_code=400, detail=f"Project '{project.id}' already exists"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Project '{project.id}' not found")


@app.delete("/projects/{project_id}", tags=["projects"])
def delete_project(project_id: str) -> bool:
    try:
        return project_service.delete_project(project_id=project_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")


@app.get("/progress/{project_id}/{tool_id}", response_model=dict[str, str])
def get_progress_api(project_id: str, tool_id: str):
    return get_progress(project_id, tool_id)


@app.post("/export/{project_id}/{source_tool}/{target_tool}", response_model=bool)
def create_export_api(
    project_id: str, source_tool: str, target_tool: str, export_file: dict
):
    return create_export(project_id, source_tool, target_tool, export_file)

@app.get("/getProjectData/{project_id}/", response_model=List[str])
def get_project_data_api(project_id: str):
    return get_project_data(project_id)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=80, proxy_headers=True)
