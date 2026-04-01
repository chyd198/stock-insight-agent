import yfinance as yf


def get_price(ticker: str) -> dict:
    """
    Fetch current market data for a stock ticker from Yahoo Finance.

    Parameters:
        ticker (str): Stock ticker symbol, e.g. "AAPL", "TSLA", "MSFT".

    Returns a dict with the following keys:
        ticker (str): Uppercased ticker symbol.
        current_price (float): Current market price.
        open (float): Opening price of the day.
        day_high (float): Highest price of the day.
        day_low (float): Lowest price of the day.
        volume (int): Trading volume.
        market_cap (str): Formatted market cap string, e.g. "$2.8T".
        pe_ratio (float or None): Trailing P/E ratio, or None if unavailable.
        error (str or None): None on success, error message string on failure.
    """
    try:
        t = yf.Ticker(ticker.upper())
        info = t.info

        if not info or info.get("regularMarketPrice") is None:
            return {"error": "Invalid ticker or no market data available for: " + ticker}

        raw_cap = info.get("marketCap")
        if raw_cap is not None:
            if raw_cap >= 1_000_000_000_000:
                market_cap = "$" + str(round(raw_cap / 1_000_000_000_000, 1)) + "T"
            elif raw_cap >= 1_000_000_000:
                market_cap = "$" + str(round(raw_cap / 1_000_000_000, 1)) + "B"
            else:
                market_cap = "$" + str(round(raw_cap / 1_000_000, 1)) + "M"
        else:
            market_cap = "N/A"

        return {
            "ticker": ticker.upper(),
            "current_price": info.get("regularMarketPrice"),
            "open": info.get("regularMarketOpen"),
            "day_high": info.get("regularMarketDayHigh"),
            "day_low": info.get("regularMarketDayLow"),
            "volume": info.get("regularMarketVolume"),
            "market_cap": market_cap,
            "pe_ratio": info.get("trailingPE"),
            "error": None,
        }
    except Exception as e:
        return {"error": str(e)}
