import pandas as pd
from features import engineer_features
from src.constants import CONST_FEATURE


# Function to prepare and predict tomorrow's price movement
def predict_tomorrow(model, historical_data, symbol):
    # Prepare the feature set for tomorrow's prediction (assuming the data is the most recent one)

    # Engineer features for the latest data (ensure it's processed the same way as the training data)
    features = engineer_features(historical_data)  # Assuming your feature engineering is already defined

    # Check if the engineered features contain any data
    if features.empty:
        print("No valid data for prediction. Please check the feature engineering process.")
        return

    # Specify the feature columns
    feature_columns = CONST_FEATURE  # Adjust if needed
    X_new = features[feature_columns]

    # Remove rows with missing values (if any)
    X_new = X_new.dropna()

    # If no valid data after dropping NaNs, print a message and return
    if X_new.empty:
        print("No valid data for prediction due to missing values.")
        return

    # Get the predicted probability for both classes (0 and 1)
    probability = model.predict_proba(X_new)  # This returns the probabilities for both classes
    probability_length = len(probability)
    # Probability for "Price Increase" (class 1)
    prob_increase = probability[probability_length-1][1] * 100  # Convert to percentage

    # Probability for "Price Decrease" (class 0)
    prob_decrease = probability[probability_length-1][0] * 100  # Convert to percentage

    # Get the predicted class (0 or 1) for "Price Increase" or "Price Decrease"
    prediction = model.predict(X_new)
    prediction_length = len(prediction)
    # Print the result: "Up" for increase, "Down" for decrease
    print(f"Stock: {symbol}")
    print(f"Tomorrow's predicted price movement: {'Up' if prediction[prediction_length-1] == 1 else 'Down'}")
    print(f"Probability of price increase (Up): {prob_increase:.2f}%")
    print(f"Probability of price decrease (Down): {prob_decrease:.2f}%")

    return prediction[0] == 1

