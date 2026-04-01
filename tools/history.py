import yfinance as yf


def get_moving_averages(ticker: str) -> dict:
    """
    Compute MA5 and MA20 moving averages and generate a trend signal for a stock.

    Parameters:
        ticker (str): Stock ticker symbol, e.g. "AAPL", "TSLA", "MSFT".

    Returns a dict with the following keys:
        ticker (str): Uppercased ticker symbol.
        ma5 (float): 5-day moving average of closing prices, rounded to 2 decimal places.
        ma20 (float): 20-day moving average of closing prices, rounded to 2 decimal places.
        trend_signal (str): One of "BULLISH", "BEARISH", or "NEUTRAL".
        trend_explanation (str): Plain English explanation of the trend including MA values.
        price_change_30d (float): Percentage price change over the last 30 days, e.g. 4.23 means +4.23%.
        error (str or None): None on success, error message string on failure.
    """
    try:
        hist = yf.Ticker(ticker.upper()).history(period="60d")

        if hist is None or len(hist) == 0:
            return {"error": "No historical data available for: " + ticker}
        if len(hist) < 20:
            return {"error": "Insufficient historical data (need at least 20 days) for: " + ticker}

        closes = hist["Close"]

        ma5 = round(closes.tail(5).mean(), 2)
        ma20 = round(closes.tail(20).mean(), 2)
        diff_pct = (ma5 - ma20) / ma20 * 100

        if diff_pct > 0.5:
            trend_signal = "BULLISH"
            trend_explanation = (
                "The 5-day moving average ($" + str(ma5) + ") is above the "
                "20-day moving average ($" + str(ma20) + "), indicating upward momentum."
            )
        elif diff_pct < -0.5:
            trend_signal = "BEARISH"
            trend_explanation = (
                "The 5-day moving average ($" + str(ma5) + ") is below the "
                "20-day moving average ($" + str(ma20) + "), indicating downward pressure."
            )
        else:
            trend_signal = "NEUTRAL"
            trend_explanation = (
                "The 5-day moving average ($" + str(ma5) + ") and the "
                "20-day moving average ($" + str(ma20) + ") are close, suggesting no clear trend."
            )

        if len(closes) >= 30:
            start_price = closes.iloc[-30]
        else:
            start_price = closes.iloc[0]

        end_price = closes.iloc[-1]
        price_change_30d = round((end_price - start_price) / start_price * 100, 2)

        return {
            "ticker": ticker.upper(),
            "ma5": ma5,
            "ma20": ma20,
            "trend_signal": trend_signal,
            "trend_explanation": trend_explanation,
            "price_change_30d": price_change_30d,
            "error": None,
        }
    except Exception as e:
        return {"error": str(e)}
