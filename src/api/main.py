## API orchestration layer
import os
import logging

logging.basicConfig(
    level=logging.INFO,
)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.inference.model_loader import load_model   ## This file imports functions from model_loader.py
from src.inference.predictor import predict         ## predictor.py
from src.inference.schemas import (                 ## schemas.py
    LoanPredictionRequest,
    LoanPredictionResponse,
)

logger = logging.getLogger(__name__)

model = None

@asynccontextmanager                                ## defines what happens during the application lifecycle.
async def lifespan(app: FastAPI):

    global model

    logger.info("Loading ML model...")

    try:
        model = load_model()

        logger.info(
            "ML model loaded successfully"
        )

    except Exception:

        logger.exception(
            "Failed to load ML model"
        )

        raise

    yield

    logger.info(
        "Application shutting down"
    )


app = FastAPI(
    title="Loan Approval API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/ready")
def ready():

    if model is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not ready",
        )

    return {
        "status": "ready"
    }


@app.get("/model-info")
def model_info():

    return {
        "model_name": os.getenv(
            "MODEL_NAME",
            "LoanApprovalModel",
        ),
        "model_version": os.getenv(
            "MODEL_VERSION",
            "1",
        ),
    }


@app.post(
    "/predict",
    response_model=LoanPredictionResponse,
)
def predict_loan(
    request: LoanPredictionRequest,
):

    if model is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not loaded",
        )

    try:

        prediction, decision = predict(
            model,
            request,
        )

        logger.info(
            "Prediction generated: %s",
            prediction,
        )

        return LoanPredictionResponse(
            prediction=prediction,
            decision=decision,
        )

    except Exception:

        logger.exception(
            "Prediction failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed",
        )

# app = FastAPI(                                      ## This creates the FastAPI application object.
#     title="Loan Approval API",                      ## Can be run using "uvicorn src.api.main:app --reload"
# )

# model = load_model()                                ## loads model

# MODEL_NAME = os.getenv(
#     "MODEL_NAME",
#     "LoanApprovalModel",
# )

# MODEL_VERSION = os.getenv(
#     "MODEL_VERSION",
#     "1",
# )

# @app.post(                                    ## Tells FastAPI when someone sends an HTTP POST request to /predict execute the below function
#     "/predict",
#     response_model=LoanPredictionResponse,
# )
# def predict_loan(
#     request: LoanPredictionRequest,           ## This is where schemas.py comes into play. LoanPredictionRequest is class from schemas.py
# ):                                            ## The input JSON by user comes to LoanPredictionRequest, Pydantic validation occurs and gets passed to predict_loan() 
#     prediction, decision = predict(           ## calling predictor.py. This passed model+validated request to predictor.py
#         model,                                ## Predictor - request -> extract 6 features -> NumPy array -> model.predict() -> 0 or 1 -> approved/rejected
#         request,
#     )

#     return LoanPredictionResponse(            ## creates the response
#         prediction=prediction,
#         decision=decision,
#     )

# @app.get("/model-info")                       ## This lets you verify which model your API thinks it is serving by passing model name and version
# def model_info():
#     return {
#         "model_name": MODEL_NAME,
#         "model_version": MODEL_VERSION,
#     }   