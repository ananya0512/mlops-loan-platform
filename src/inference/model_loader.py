import os

import mlflow
import mlflow.sklearn


MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "LoanApprovalModel",
)

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
)


def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = (
        f"models:/{MODEL_NAME}/{MODEL_VERSION}"
    )

    model = mlflow.sklearn.load_model(
        model_uri
    )

    return model