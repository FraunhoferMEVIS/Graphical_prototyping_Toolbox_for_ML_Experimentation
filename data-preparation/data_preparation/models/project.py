""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: project.py
author: Lucas Rebscher
date: 12/2023
description: project models
-----------------------------------------------------------------------------
"""

from pydantic import BaseModel


class ProjectPostBody(BaseModel):
    name: str


class ProjectPostResponse(BaseModel):
    message: str
    status: bool


class ProjectGetResponse(BaseModel):
    name: str
