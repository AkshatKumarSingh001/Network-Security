import sys

from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from Network_Security.exception.exception import NetworkSecurityException


def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    """Train and evaluate multiple models, returning test accuracy per model."""
    try:
        report = {}

        for model_name, model in models.items():
            param_grid = param.get(model_name, {})

            # Tune only when a parameter grid is provided.
            if param_grid:
                grid_search = GridSearchCV(model, param_grid=param_grid, cv=3)
                grid_search.fit(x_train, y_train)
                model = grid_search.best_estimator_
            else:
                model.fit(x_train, y_train)

            y_test_pred = model.predict(x_test)
            test_model_score = accuracy_score(y_test, y_test_pred)
            report[model_name] = test_model_score

            # Keep the selected/best estimator available for downstream use.
            models[model_name] = model

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
