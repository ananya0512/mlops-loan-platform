## Converts API input into ML input
## This file's responsibility is: Take the validated API request and convert it into the exact feature structure expected by the ML model.

import numpy as np

from src.config.features import FEATURES   ## import parameters from src/config/features.py

def predict(model, request):

    # features = np.array(                 ## coverts input into [[feature1, feature2, feature3, feature4, feature5, feature6]] format
    #     [[
    #         request.age,
    #         request.income,
    #         request.loan_amount,
    #         request.credit_score,
    #         request.employment_years,
    #         request.existing_loans,
    #     ]]
    # )

    feature_values = [                    ## features comes from src/config/features.py
        getattr(request, feature)         ## this automatically reproduces the above commented request.feature s
        for feature in FEATURES
    ]

    features = np.array(
        [feature_values]
    )

    prediction = model.predict(features)[0]   ## calling the model and making prediction on the input features

    prediction = int(prediction)   ## Convert NumPy integer to Python integer

    decision = (                   ## Convert prediction into business meaning
        "approved"
        if prediction == 1
        else "rejected"
    )

    return prediction, decision
