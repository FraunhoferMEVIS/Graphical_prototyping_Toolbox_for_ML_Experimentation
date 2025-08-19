""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_api.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: testing if the ai-sandbox api starts
-----------------------------------------------------------------------------
"""


def test_application_running(client):
    """
    test proper run of the app
    """
    resp = client.get('/docs')
    assert resp.status_code == 200
