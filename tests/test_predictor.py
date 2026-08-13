from src.inference.schemas import LoanPredictionRequest


def test_prediction_request():

    request = LoanPredictionRequest(
        age=35,
        income=75000,
        loan_amount=25000,
        credit_score=720,
        employment_years=8,
        existing_loans=1,
    )

    assert request.age == 35
    assert request.income == 75000
    assert request.loan_amount == 25000
    assert request.credit_score == 720
    assert request.employment_years == 8
    assert request.existing_loans == 1