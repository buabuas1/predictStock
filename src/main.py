# main.py
from data.read_ami import get_data
from data_loader import load_data
from features import engineer_features
from model import train_model
from src.prediction import predict_tomorrow


def main():

    all_stocks = ["BVH","HVN","ANV"]
    up_predict = []
    for stock in all_stocks:
        # Load data
        print("Loading data from Ami...")
        ohcl = get_data(stock, 1000)
        print("Data loaded successfully.")

        # Engineer features
        print("Engineering features...")
        data = engineer_features(ohcl.copy())
        print("Features engineered.")

        # Train model
        print("Training model...")
        model = train_model(data)
        print("Model trained successfully.")

        is_up = predict_tomorrow(model, ohcl.copy(), stock)
        if is_up:
            up_predict.append(stock)

    if len(up_predict) > 0:
        for s in up_predict:
            print(f"{s}")
if __name__ == "__main__":
    main()
