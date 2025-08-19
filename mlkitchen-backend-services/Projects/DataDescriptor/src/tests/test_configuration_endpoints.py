""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_feature_endpoint.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 08/2024
description: Testing if the Data Descriptor's configuration andpoints run
             as expected.
-----------------------------------------------------------------------------
"""


def test_saving_getting_metadata_file(client, sample_project, sample_metadata):
    """
    Testing if getting the metadata file works as expected
    """
    resp = client.post(f'/config/{sample_project}', json=sample_metadata)
    assert resp.status_code == 200

    # # check if the output makes sesne!
    result = resp.json()
    assert result['metadata'] == sample_metadata

    resp = client.get(f'/config/{sample_project}')
    assert resp.status_code == 200

    result = resp.json()
    assert result == sample_metadata