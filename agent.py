import os
from connectonion import Agent, host

from tools.price import get_price
from tools.history import get_moving_averages
from tools.news import get_news

SYSTEM_PROMPT = """You are a stock analysis assistant. When a user asks about a stock, call all three tools — get_price, get_moving_averages, and get_news — then synthesize the results into a structured response.

**Response format:**
1. **One-line summary**: stock name, current price, and overall sentiment (bullish/bearish/neutral).
2. **Price**: current price, day range (low–high), volume, market cap, and P/E ratio.
3. **Trend**: MA5 and MA20 values (the first time you mention them, explain that MA5 is the 5-day moving average and MA20 is the 20-day moving average of closing prices), trend signal, 30-day price change, and plain-English explanation.
4. **News**: bullet list of recent headlines.
5. **Closing note**: 2–3 sentences summarizing the overall picture. Always state: "This is NOT financial advice."

**If the ticker is invalid or data is unavailable**: say so clearly and ask the user to double-check the symbol.

**If the user gives a company name instead of a ticker** (e.g. "Apple", "Tesla", "Microsoft"): infer the correct ticker and proceed. Known mappings:
- Apple → AAPL
- Tesla → TSLA
- Microsoft → MSFT
- NVIDIA → NVDA
- Google / Alphabet → GOOG
- Amazon → AMZN
- Meta / Facebook → META
- Berkshire Hathaway → BRK-B
"""

def create_agent():
    return Agent(
        name="stock-insight-agent",
        system_prompt=SYSTEM_PROMPT,
        tools=[get_price, get_moving_averages, get_news],
        model="gpt-4o-mini",
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host(create_agent, port=port)
