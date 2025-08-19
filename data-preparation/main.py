""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: main.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: 
-----------------------------------------------------------------------------
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from data_preparation.routes.api import router as api_router
from data_preparation.core.app_config import DATA_PREPROCESSING_PORT, ROOT_PATH, DATA_PREPARATION_CSV_REPO, DATA_PREPARATION_PROJECTS_FOLDER
import os
import shutil


tags_metadata = [
    {
        "name": "Network",
        "description":
            "The data preparation network of the project at the 'current' session.",
    },
    {
        "name": "Modules",
        "description": "The modules that can be added to the network.",
    },
    {
        "name": "Execute",
        "description": "Execute the process of the entire network.",
    },
    {
        "name": "Script",
        "description": "Edit/Add Scripts to a Network.",
    },
    {
        "name": "Sessions",
        "description": "Manage the sessions of a given project.",
    },
]

# For Demo Only
if DATA_PREPARATION_CSV_REPO:
    if not os.path.exists(DATA_PREPARATION_CSV_REPO):
        os.makedirs(DATA_PREPARATION_CSV_REPO)

app = FastAPI(
    title="Data Preparation",
    description="KI-FDZ Data Preparation Core Application",
    version="1.0.0",
    contact={
        "name": "Elham Taghizadeh"
    },
    openapi_tags=tags_metadata,
)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect():
    return RedirectResponse(url=ROOT_PATH + "/docs")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=DATA_PREPROCESSING_PORT,
        root_path=ROOT_PATH,
        log_level="info",
        reload=True,
    )
