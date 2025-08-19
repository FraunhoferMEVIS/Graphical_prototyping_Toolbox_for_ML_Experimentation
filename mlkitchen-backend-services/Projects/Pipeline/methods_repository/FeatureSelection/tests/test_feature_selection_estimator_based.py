import pytest
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize("algorithm", ["RFE", "SequentialFeatureSelector",
                                       "SelectFromModel", "RFECV"])
def test_feature_selection_estimator_based(iris_dataset, algorithm):

    parameters = {

        "estimators": [
         {
            'name': "RandomForestClassifier",
            'parameters': {
                "C": 1.0,
                "epsilon": 0.2,
                "kernel": [{
                    "name": "RBF",
                    "parameters": {
                            "kernel": [{
                                "name": "RBF",
                                "length_scale": 1.0}
                                ]}
                    }],

            }
         }
        ],
        # RFE parameters
        "n_features_to_select": 3,
        "step": 1,
        # SequentialFeatureSelector parameters
        "direction": 'backward',
        "cv": 5,
        # SelectFromModel parameters
        "max_features": 4
        }

    feature_selection_object = ModuleFinder.use_method("FeatureSelection",
                                                       algorithm, **parameters)

    X = iris_dataset.data
    y = iris_dataset.target

    # Train
    X_new = feature_selection_object.fit_transform(X, y)
    print(X_new.shape)
