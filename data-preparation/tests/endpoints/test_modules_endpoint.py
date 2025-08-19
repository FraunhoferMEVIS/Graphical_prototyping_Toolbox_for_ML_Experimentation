""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_modules_endpoint.py
author: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 10/2023
description: testing the modules endpoints of the api
-----------------------------------------------------------------------------
"""


def test_get_modules(client):
    """
    test get_modules: To test if getting module metadata \
    is working as expected
    """
    resp = client.get("/modules")

    # check if running
    assert resp.status_code == 200
    assert len(resp.json()) > 0
