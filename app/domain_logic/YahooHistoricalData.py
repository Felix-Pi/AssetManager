import yfinance as yf


# locale.setlocale(locale.LC_TIME, "de_DE")

def get_historical_data(symbol, period, interval):
    print(period, interval)
    symbol = yf.Ticker(symbol)
    hist = symbol.history(period=period, interval=interval)

    hist['Median'] = ((hist['High'] + hist['Low']) / 2)
    hist['timestamps'] = hist['High'].keys()

    hist = parse_historical_data(hist, period)

    return hist.to_json()


def parse_historical_data(df, period):
    if '1d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%H:%M")
    if '2d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%a, %H:%M")
    if '5d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%a, %d %b %H:%M")
    if '1mo' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b, %H:%M")
    if '3mo' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b")
    if '1y' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b %Y")
    if '5y' == period or 'max' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%b %Y")

    return df
