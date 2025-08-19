""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: serve.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: Serving the Data Descriptor
-----------------------------------------------------------------------------
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.routes.api import router as api_router
from src.backend.app_config import DATADESCRIPTOR_HOST, DATADESCRIPTOR_PORT, ROOT_PATH


tags_metadata = [
    {
        "name": "Features",
        "description": "Set up and edit an mlflow recipe project.",
    },
    {
        "name": "Modules",
        "description":
            """Retrieve the modules to load features, \
               find existing functions to define new features, ...""",
    }
]

app = FastAPI(
    title="Data Descriptor",
    description="Data Descriptor for Tabular Database",
    version="1.0.0",
    contact={
        "name": "Elham Taghizadeh",
        "email": "kifdz@mevis.fraunhofer.de",
    },
    openapi_tags=tags_metadata,
)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def redirect():
    """
    redirect to the /docs
    """
    return RedirectResponse(url=ROOT_PATH + "/docs")


if __name__ == '__main__':
    uvicorn.run("serve:app", host=DATADESCRIPTOR_HOST, port=DATADESCRIPTOR_PORT, root_path=ROOT_PATH,
                log_level="info", reload=True)
