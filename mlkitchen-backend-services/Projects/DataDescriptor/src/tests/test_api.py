""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_api.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: testing if the Data Descriptor api starts
-----------------------------------------------------------------------------
"""


def test_application_running(client):
    """
    test proper run of the app
    """
    resp = client.get('/docs')
    assert resp.status_code == 200
