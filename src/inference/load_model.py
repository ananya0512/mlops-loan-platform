import mlflow
import mlflow.sklearn


MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"


def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = "models:/LoanApprovalModel/1"

    model = mlflow.sklearn.load_model(
        model_uri
    )

    return model


if __name__ == "__main__":
    model = load_model()

    print("Model loaded successfully")
    print(model)