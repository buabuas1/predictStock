# data_loader.py
from pymongo import MongoClient
import pandas as pd

username = "admin"
password = "admin"
host = "localhost"  # Or your MongoDB host/IP
port = 27017  # Default MongoDB port
database = "admin"  # Database you want to connect to

# Create connection string with authentication
connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database}"

# Connect to MongoDB
def load_data(stock_code):
    client = MongoClient(connection_string)
    db = client['admin']
    collection = db['Intraday']
    record = collection.find({'StockCode': stock_code})
    # Load data from MongoDB and convert it to a DataFrame
    data = pd.DataFrame(list(collection.find({'StockCode': stock_code})))
    for index, item in data.iterrows():
        trades = item['Trades']
        if trades:
            # Set 'O', 'C', 'H', 'L' based on 'Trades' list
            data.at[index, 'O'] = float(trades[-1]['Price'])  # Close price (last trade)
            data.at[index, 'C'] = float(trades[0]['Price'])  # Open price (first trade)
            data.at[index, 'H'] = float(max(trade['Price'] for trade in trades))  # High price
            data.at[index, 'L'] = float(min(trade['Price'] for trade in trades))  # Low price
            data.at[index, 'V'] = float(sum(trade['Volume'] for trade in trades))  # Low price
    return data
