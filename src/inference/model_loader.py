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

WINDOWS_MLFLOW_ROOT = os.getenv(
    "WINDOWS_MLFLOW_ROOT",
    "C:/Users/Ananya/Documents/projects/mlops-loan-platform/mlflow",
)

CONTAINER_MLFLOW_ROOT = os.getenv(
    "CONTAINER_MLFLOW_ROOT",
    "/mlflow",
)


def load_model():

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    print(
        f"Loading model: "
        f"{MODEL_NAME} version: {MODEL_VERSION}"
    )

    client = mlflow.MlflowClient()

    version = client.get_model_version(
        MODEL_NAME,
        MODEL_VERSION,
    )

    print(f"Model source: {version.source}")

    artifact_uri = client.get_model_version_download_uri(
        MODEL_NAME,
        MODEL_VERSION,
    )

    print(f"MLflow artifact URI: {artifact_uri}")

    if artifact_uri.startswith("file:"):

        artifact_path = artifact_uri.replace(
            "file:",
            "",
            1,
        )

        artifact_path = artifact_path.replace(
            WINDOWS_MLFLOW_ROOT,
            CONTAINER_MLFLOW_ROOT,
        )

        artifact_path = artifact_path.replace(
            "\\",
            "/",
        )

        print(
            f"Container artifact path: "
            f"{artifact_path}"
        )

        if not os.path.exists(artifact_path):

            raise RuntimeError(
                "MLflow artifact does not exist "
                f"in container: {artifact_path}"
            )

        print(
            "Loading model from "
            "container artifact path..."
        )

        model = mlflow.sklearn.load_model(
            artifact_path
        )

    else:

        model = mlflow.sklearn.load_model(
            f"models:/{MODEL_NAME}/{MODEL_VERSION}"
        )

    print("MODEL LOADED SUCCESSFULLY")

    return model