""" Copyright (c) Fraunhofer MEVIS, Germany. All rights reserved.
**InsertLicense** code
-----------------------------------------------------------------------------
file: Sampling.py
authors: Elham Taghizadeh, Melissa Finster, Johannes Bunk
date: 11/2022
description: The available Sampling algorithms in the repository
-----------------------------------------------------------------------------
"""

import logging
from methods_repository.config_models import SamplingTypes, \
                                             ProgrammingLanguages


_logger = logging.getLogger(__name__)


List_of_Algorithms = {
    ProgrammingLanguages.Python: {
        # ############ Oversampling #############
        "RandomOverSampler": {
            "import": "imblearn.over_sampling",
            "name": "RandomOverSampler",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": False
        },
        "SMOTE": {
            "import": "imblearn.over_sampling",
            "name": "SMOTE",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": False
        },
        "SVMSMOTE": {
            "import": "imblearn.over_sampling",
            "name": "SVMSMOTE",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": True  # Default SVC
        },
        "KMeansSMOTE": {
            "import": "imblearn.over_sampling",
            "name": "KMeansSMOTE",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": True  # Default MiniBatchKMeans
        },
        "BorderlineSMOTE": {
            "import": "imblearn.over_sampling",
            "name": "BorderlineSMOTE",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": False
        },
        "SMOTEN": {
            "import": "imblearn.over_sampling",
            "name": "SMOTEN",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": False
        },
        "ADASYN": {
            "import": "imblearn.over_sampling",
            "name": "ADASYN",
            "flags": [SamplingTypes.oversampling],
            "require_estimator": False
        },
        # ############ Undersampling #############
        "RandomUnderSampler": {
            "import": "imblearn.under_sampling",
            "name": "RandomUnderSampler",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "TomekLinks": {
            "import": "imblearn.under_sampling",
            "name": "TomekLinks",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "ClusterCentroids": {
            "import": "imblearn.under_sampling",
            "name": "ClusterCentroids",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": True  # Default KMeans estimator
        },
        "CondensedNearestNeighbour": {
            "import": "imblearn.under_sampling",
            "name": "CondensedNearestNeighbour",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": True  # Default n_neighbors estimator
        },
        "EditedNearestNeighbours": {
            "import": "imblearn.under_sampling",
            "name": "EditedNearestNeighbours",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "RepeatedEditedNearestNeighbours": {
            "import": "imblearn.under_sampling",
            "name": "RepeatedEditedNearestNeighbours",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "AllKNN": {
            "import": "imblearn.under_sampling",
            "name": "AllKNN",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "InstanceHardnessThreshold": {
            "import": "imblearn.under_sampling",
            "name": "InstanceHardnessThreshold",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": True  # Default RandomForestClassifier
        },
        "NearMiss": {
            "import": "imblearn.under_sampling",
            "name": "NearMiss",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "NeighbourhoodCleaningRule": {
            "import": "imblearn.under_sampling",
            "name": "NeighbourhoodCleaningRule",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        "OneSidedSelection": {
            "import": "imblearn.under_sampling",
            "name": "NeighbourhoodCleaningRule",
            "flags": [SamplingTypes.undersampling],
            "require_estimator": False
        },
        # ############ Combinations of over- and undersampling #############
        "SMOTEENN": {
            "import": "imblearn.combine",
            "name": "SMOTEENN",
            "flags": [SamplingTypes.over_undersampling],
            "require_estimator": True
            # Default EditedNearestNeighbours "all" and SMOTE
        },
        "SMOTETomek": {
            "import": "imblearn.combine",
            "name": "SMOTETomek",
            "flags": [SamplingTypes.over_undersampling],
            "require_estimator": True  # Default TomekLinks "all" and SMOTE
        },
    }
}
