# features.py
from ta.momentum import StochRSIIndicator, RSIIndicator


def engineer_features(data):
    # Create example features
    data['price_change'] = ((data['C'] - data['C'].shift(1)) / data['C'].shift(1) * 100).round(0)
    data['rsi'] = RSIIndicator(data['C'], window=14).rsi() # 14-day RSI

    # data['5_day_avg'] = data['C'].rolling(window=5).mean()
    # data['10_day_avg'] = data['C'].rolling(window=10).mean()

    data['tenkan_sen'] = (data['H'].rolling(window=9).max() + data['L'].rolling(window=9).min()) / 2
    data['tenkan_sen_up'] = (data['tenkan_sen'] > data['tenkan_sen'].shift(1)).astype(int)

    # Kijun-sen (17-period)
    data['kijun_sen_17'] = (data['H'].rolling(window=17).max() + data['L'].rolling(window=17).min()) / 2
    data['kijun_sen_17_up'] = (data['kijun_sen_17'] > data['kijun_sen_17'].shift(1)).astype(int)

    # Kijun-sen (65-period)
    dao65 = 65
    if len(data) < 65:
        dao65 = len(data)
    data['kijun_sen_65'] = (data['H'].rolling(window=dao65).max() + data['L'].rolling(window=dao65).min()) / 2
    data['kijun_sen_65_up'] = (data['kijun_sen_65'] > data['kijun_sen_65'].shift(1)).astype(int)

    # # Kijun-sen (129-period)
    dao129 = 129
    if len(data) < 129:
        dao129 = len(data)
    data['kijun_sen_129'] = (data['H'].rolling(window=dao129).max() + data['L'].rolling(window=dao129).min()) / 2
    data['kijun_sen_129_up'] = (data['kijun_sen_129'] > data['kijun_sen_129'].shift(1)).astype(int)

    # Drop rows with NaN values from rolling averages
    data.dropna(inplace=True)

    # Define target variable (price increase or decrease)
    data['target'] = (data['C'].shift(-2) >= (1.02*data['C'])).astype(int)
    data.dropna(inplace=True)  # Remove any rows with missing target values
    #data.drop(['tenkan_sen', 'kijun_sen_17', 'kijun_sen_65', 'kijun_sen_129', 'O', 'H', 'C', 'L', 'V', 'Date'], axis=1, inplace=True)

    return data
