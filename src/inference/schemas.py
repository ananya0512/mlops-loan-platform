from pydantic import BaseModel, Field


class LoanPredictionRequest(BaseModel):
    age: int = Field(
        ...,
        ge=18,
        le=100,
    )

    income: float = Field(
        ...,
        gt=0,
    )

    loan_amount: float = Field(
        ...,
        gt=0,
    )

    credit_score: int = Field(
        ...,
        ge=300,
        le=850,
    )

    employment_years: int = Field(
        ...,
        ge=0,
    )

    existing_loans: int = Field(
        ...,
        ge=0,
    )


class LoanPredictionResponse(BaseModel):
    prediction: int
    decision: str