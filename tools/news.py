import yfinance as yf


def get_news(ticker: str) -> dict:
    """
    Fetch recent news headlines for a stock from Yahoo Finance.

    Parameters:
        ticker (str): Stock ticker symbol, e.g. "AAPL", "TSLA", "MSFT".

    Returns a dict with the following keys:
        ticker (str): Uppercased ticker symbol.
        headlines (list of str): Up to 5 recent news headline strings.
        error (str or None): None on success, error message string on failure.
    """
    try:
        news = yf.Ticker(ticker.upper()).news

        if not news:
            return {
                "ticker": ticker.upper(),
                "headlines": [],
                "error": None,
            }

        headlines = []
        for item in news[:5]:
            title = item.get("title", "")
            if not title:
                title = item.get("content", {}).get("title", "")
            if title:
                headlines.append(title)

        return {
            "ticker": ticker.upper(),
            "headlines": headlines,
            "error": None,
        }
    except Exception as e:
        return {"error": str(e)}
