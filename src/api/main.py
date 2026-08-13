## API orchestration layer
import os
from fastapi import FastAPI
from src.inference.model_loader import load_model   ## This file imports functions from model_loader.py
from src.inference.predictor import predict         ## predictor.py
from src.inference.schemas import (                 ## schemas.py
    LoanPredictionRequest,
    LoanPredictionResponse,
)

app = FastAPI(                                      ## This creates the FastAPI application object.
    title="Loan Approval API",                      ## Can be run using "uvicorn src.api.main:app --reload"
)

model = load_model()                                ## loads model

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "LoanApprovalModel",
)

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
)

@app.post(                                    ## Tells FastAPI when someone sends an HTTP POST request to /predict execute the below function
    "/predict",
    response_model=LoanPredictionResponse,
)
def predict_loan(
    request: LoanPredictionRequest,           ## This is where schemas.py comes into play. LoanPredictionRequest is class from schemas.py
):                                            ## The input JSON by user comes to LoanPredictionRequest, Pydantic validation occurs and gets passed to predict_loan() 
    prediction, decision = predict(           ## calling predictor.py. This passed model+validated request to predictor.py
        model,                                ## Predictor - request -> extract 6 features -> NumPy array -> model.predict() -> 0 or 1 -> approved/rejected
        request,
    )

    return LoanPredictionResponse(            ## creates the response
        prediction=prediction,
        decision=decision,
    )

@app.get("/model-info")                       ## This lets you verify which model your API thinks it is serving by passing model name and version
def model_info():
    return {
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
    }   