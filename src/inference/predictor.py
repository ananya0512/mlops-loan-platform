import numpy as np


def predict(model, request):

    features = np.array(
        [[
            request.age,
            request.income,
            request.loan_amount,
            request.credit_score,
            request.employment_years,
            request.existing_loans,
        ]]
    )

    prediction = model.predict(features)[0]

    prediction = int(prediction)

    decision = (
        "approved"
        if prediction == 1
        else "rejected"
    )

    return prediction, decision