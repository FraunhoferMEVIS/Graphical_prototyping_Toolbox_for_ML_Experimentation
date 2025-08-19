""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: serve.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 03/2023
description: Serving the Data Descriptor
-----------------------------------------------------------------------------
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from data_provider_src.routes.api import router as api_router
from data_provider_src.backend.app_config import Data_INGEST_HOST, Data_INGEST_PORT, ROOT_PATH


tags_metadata = [
    {
        "name": "Data",
        "description": "Set up and edit an mlflow recipe project.",
    }
]

app = FastAPI(
    title="Data Provider",
    description="""This service gets data from the source, splits the data \
                   and provide each dataset, upon request""",
    version="1.0.0",
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
    uvicorn.run("serve_data_provider:app", host=Data_INGEST_HOST,
                port=Data_INGEST_PORT, root_path=ROOT_PATH,
                log_level="info", reload=True)
