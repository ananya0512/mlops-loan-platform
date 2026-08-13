import os
from fastapi import FastAPI
from src.inference.model_loader import load_model
from src.inference.predictor import predict
from src.inference.schemas import (
    LoanPredictionRequest,
    LoanPredictionResponse,
)

app = FastAPI(
    title="Loan Approval API",
)

model = load_model()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "LoanApprovalModel",
)

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
)

@app.post(
    "/predict",
    response_model=LoanPredictionResponse,
)
def predict_loan(
    request: LoanPredictionRequest,
):
    prediction, decision = predict(
        model,
        request,
    )

    return LoanPredictionResponse(
        prediction=prediction,
        decision=decision,
    )

@app.get("/model-info")
def model_info():
    return {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
    }   