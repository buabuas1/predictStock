from datetime import datetime
import win32com.client
import pandas as pd

# Connect to AmiBroker application
amibroker = win32com.client.Dispatch("Broker.Application")

# Load the database (change the path as per your AmiBroker database)
amibroker.LoadDatabase("D:\\stock\\AmiBroker\\eod")


def get_data(symbol, num_bars=100):
    # Connect to the specified symbol in AmiBroker
    stock = amibroker.Stocks(symbol)

    if not stock:
        print(f"Symbol {symbol} not found.")
        return None

    # Retrieve quotations
    quotations = stock.Quotations
    num_bars = min(num_bars, quotations.Count)  # Limit to available data
    max_bar = quotations.Count
    # Store data in a list of dictionaries
    data = []
    for i in range(num_bars):
        quotation = quotations((max_bar - num_bars + i))
        # Convert quotation.Date to datetime
        date = quotation.Date.date()

        data.append({
            "Date": date,
            "O": quotation.Open,
            "H": quotation.High,
            "L": quotation.Low,
            "C": quotation.Close,
            "V": quotation.Volume,
            "Symbol": symbol
        })

    # Convert to a DataFrame
    df = pd.DataFrame(data)
    #print(df)
    return df
