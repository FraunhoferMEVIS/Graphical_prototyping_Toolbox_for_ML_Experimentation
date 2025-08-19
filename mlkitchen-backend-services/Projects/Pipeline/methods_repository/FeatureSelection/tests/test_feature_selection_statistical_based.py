import pytest
from methods_repository.abstraction import ModuleFinder


@pytest.mark.parametrize("algorithm", [
    "GenericUnivariateSelect", "SelectPercentile", "SelectKBest",
    "VarianceThreshold"])
def test_feature_selection_statistical_based(house_prices, algorithm):

    parameters = {
        'score_func': 'mutual_info_regression',

        # Generic Univariate Select parameters
        'mode': 'k_best',
        'param': 2,

        # SelectPercentile parameters
        'percentile': 20,

        # SelectKBest parameters
        'k': 3
    }

    feature_selection_object = ModuleFinder.use_method("FeatureSelection",
                                                       algorithm, **parameters)

    X = house_prices.data
    y = house_prices.target

    # Train
    X_new = feature_selection_object.fit_transform(X, y)
    print(X_new.shape)
