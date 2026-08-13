import os
import mlflow
import joblib
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,   ## Out of all predictions how may are correct
    precision_score,  ## Of all the customers we predicted as approved, how many were actually approved?
    recall_score,     ## Of all the customers who were actually approved, how many did the model correctly identify?
    f1_score,         ## Precision + Recall. useful when you want to balance false positives and false negatives.
)
from sklearn.model_selection import train_test_split
from src.config.features import FEATURES, TARGET      ## import parameters from src/config/features.py

MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
DATA_PATH = "data/raw/loan_data.csv"
TARGET_COLUMN = "loan_approved"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def prepare_data(df):
    X = df.drop(columns=[TARGET_COLUMN])   ## Removing the target from X. Results in features
    y = df[TARGET_COLUMN]                  ## target/label.

    return X, y


def train_model(X_train, y_train):    ## function responsible for training the model. X_train-training features, y_train-training labels
    model = RandomForestClassifier(
        n_estimators=100,             ## Create 100 decision trees inside the Random Forest.
        random_state=42               ## Machine-learning algorithms often involve randomness. Setting this makes the result reproducible.
    )

    model.fit(X_train, y_train)       ## actual ML training step

    return model


def evaluate_model(model, X_test, y_test):               ## model evaluation so it uses the test features and labels and model as input
    predictions = model.predict(X_test)                  ## trained model looks at the test features and create predictions

    metrics = {                                          ## Creating the metrics dictionary
        "accuracy": accuracy_score(y_test, predictions), ## compares test label values with the prediction values and calculate accuracy
        "precision": precision_score(                    ## Calculates precision
            y_test,                                      ## test labels
            predictions,                                 ## model's prediction
            zero_division=0                              ## If the calculation requires dividing by 0, just return 0 instead of throwing a warning or error
        ),
        "recall": recall_score(                          ## Calculates recall score - accuracy + prediction
            y_test,
            predictions,
            zero_division=0
        ),
        "f1": f1_score(                                  ## Calculates F1 score
            y_test,
            predictions,
            zero_division=0
        ),
    }

    return metrics                                       ## returns metrics dictionary


def main():                         ## main workflow of your training script.Think of it as the orchestrator.
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("loan-approval")   ## set the mlflow experiment under which runs will be there
    df = load_data()                ## load datset, read csv and return df

    X, y = prepare_data(df)         ## This calls prepare_data(df) and recieves X → features and y → target

    X_train, X_test, y_train, y_test = train_test_split(   ## Splitting x and y into training and testing sets
        X,                                                 ## complete features dataset
        y,                                                 ## complete labels dataset
        test_size=0.2,                                     ## this means 20% testing and 80% training
        random_state=42,                                   ## reproducibility
        stratify=y                                         ## training and testing datasets to maintain approximately the same ratio
    )
    with mlflow.start_run():                     ## starts mlflow run

        model = train_model(X_train, y_train)    ## This calls train_model() and executes random forest

        os.makedirs("models", exist_ok=True)     ## DVC assumes that a stage's outputs can be deleted and regenerated from its dependencies. So it needs to be created.
        joblib.dump(
            model,
            "models/loan_model.pkl"
        )

        metrics = evaluate_model(                ## Take this trained model, make predictions on this unseen test data
            model,                               ## compare those predictions against the actual test labels, and calculate the metrics
            X_test,
            y_test
        )

        mlflow.log_param(                        ## log parameters (configurations or hyperparameters chosen during training)
            "n_estimators",
            100
        )

        mlflow.log_param(
            "random_state",
            42
        )

        mlflow.log_metrics(metrics)             ## logs metrices

        model_info = mlflow.sklearn.log_model(          ## Save/log this trained model as an MLflow model artifact
            sk_model=model,
            name="LoanApprovalModel"
        )

        print("\nModel Metrics")

        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")


if __name__ == "__main__":    ## this means run the main() only when the python file is being executed directly.
    main()                    ## if the file is being imported by another python file main() will not run automatically, its functions can be used by the importing file.