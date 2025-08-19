""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: aisandbox_server.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: API  and function initialization 
-----------------------------------------------------------------------------
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.routes.api import router as api_router
from src.backend.app_config import AISANDBOX_HOST, AISANDBOX_PORT, ROOT_PATH

tags_metadata = [
    {
        "name": "Recipe",
        "description": "Set up and edit an mlflow recipe project.",
    },
    {
        "name": "Methods",
        "description":
            "Retrieve information about available machine learning methods.",
    },
    {
        "name": "Execute",
        "description": "Execute specified mlflow recipe.",
    },
    {
        "name": "Results",
        "description": "Retrieve mlflow experiment results.",
    }
]

app = FastAPI(
    title="AI Sandbox",
    description="KI-FDZ AI Sandbox Core Application",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.include_router(api_router)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def redirect():
    RedirectResponse(url=ROOT_PATH + "/docs")


if __name__ == '__main__':
    uvicorn.run("aisandbox_server:app",
                host=AISANDBOX_HOST,
                port=AISANDBOX_PORT,
                root_path=ROOT_PATH,
                log_level="info",
                reload=True,
                proxy_headers=True)
