""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: test_feature_endpoint.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 02/2023
description: Testing if the Data Descriptor's Feature andpoints run
             as expected.
-----------------------------------------------------------------------------
"""


def test_getting_list_of_features(client, sample_metadata, sample_project):
    """
    Testing if getting list of features work and the output results
    are meaningful
    """
    resp = client.post(f'/config/{sample_project}', json=sample_metadata)
    assert resp.status_code == 200

    resp = client.get(f'/features/{sample_project}/list')
    assert resp.status_code == 200

    # # check if the output makes sesne!
    result = resp.json()
    assert 'keys' in result and 'features' in result
    assert result['keys'] == sample_metadata['keys']
    assert result['features'] == sample_metadata['features']

