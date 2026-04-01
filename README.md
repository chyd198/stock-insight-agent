# Stock Insight Agent

> A conversational AI agent built with ConnectOnion that analyzes stocks using real-time price data, moving average trend signals, and recent news — deployed as a live web service.

**Live demo:** [chat.openonion.ai](https://chat.openonion.ai/0x2f68a71646c1d50a40b435a3a2ace60273b3c91fb8f3c5185305d5d6de6cd89c) · invite code: `OpenOnion`  
**API:** `https://confident-blessing-production-ff81.up.railway.app`  
**Built with:** [ConnectOnion](https://connectonion.com) · Python · yfinance · Railway

---

## What This Does

You type a stock ticker (e.g., `AAPL`, `TSLA`) into a chat interface. The agent:

1. Fetches the **current price**, day range, volume, market cap, and P/E ratio
2. Pulls **60 days of historical data** and computes MA5 / MA20 moving averages to generate a BULLISH / BEARISH / NEUTRAL trend signal
3. Retrieves the **5 most recent news headlines**
4. Synthesizes everything into a clear, plain-English analysis

It does not give financial advice. It presents data and explains what it means.

---

## Why I Built This

I have a financial systems background from an internship at Hundsun Technologies (China's leading fintech infrastructure company), where I worked on SQL-based data pipelines for asset management platforms. This project applies that domain knowledge to an AI agent use case — specifically, making stock data accessible through natural conversation rather than dashboards.

I built it using the ConnectOnion framework because its protocol-first, tool-based architecture maps cleanly to how financial data workflows are structured: discrete data sources (price feeds, news APIs, analytics) that need to be orchestrated and summarized for an end user.

---

## Architecture

```
User (chat UI)
     │
     ▼
ConnectOnion Agent  ← system prompt defines behavior
     │
     ├── get_price()          → yfinance: current price, stats
     ├── get_moving_averages() → yfinance: 60d history, MA5/MA20, 30d change
     └── get_news()           → yfinance: recent headlines
     │
     ▼
Structured natural language response
```

The agent uses ConnectOnion's `Agent` class with three registered tool functions. Each tool is a plain Python function with type hints and a docstring — ConnectOnion handles the tool schema generation automatically.

The agent is served via ConnectOnion's `host()` function, which spins up an HTTP server compatible with the ConnectOnion chat UI.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Agent framework | `connectonion` | Protocol-first agent architecture, built-in hosting |
| Stock data | `yfinance` | Free, no API key, covers NYSE/NASDAQ |
| LLM | GPT-4o-mini via ConnectOnion | Cost-efficient, fast tool use |
| Deployment | Railway (Docker) | Simple, supports persistent HTTP servers |

---

## Project Structure

```
stock-insight-agent/
├── agent.py              # Agent definition, system prompt, host() call
├── tools/
│   ├── __init__.py
│   ├── price.py          # get_price(ticker) → current price and stats
│   ├── history.py        # get_moving_averages(ticker) → MA5/MA20/trend
│   └── news.py           # get_news(ticker) → recent headlines
├── requirements.txt      # connectonion, yfinance
├── Dockerfile
├── railway.json
└── README.md
```

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/chyd198/stock-insight-agent
cd stock-insight-agent
pip install -r requirements.txt

# Set your OpenAI key (ConnectOnion reads this automatically)
export OPENAI_API_KEY=sk-...

# Run
python agent.py
```

Then open the ConnectOnion chat UI at `https://chat.openonion.ai/<your-agent-address>` — the address is printed in the terminal when the agent starts. Enter invite code `OpenOnion` to authenticate.

Try asking:
- `"Analyze AAPL"`
- `"What's Tesla's trend?"`
- `"Any recent news on NVDA?"`

---

## Tool Reference

### `get_price(ticker: str) -> dict`

Fetches current market data from Yahoo Finance.

Returns: `current_price`, `open`, `day_high`, `day_low`, `volume`, `market_cap`, `pe_ratio`

### `get_moving_averages(ticker: str) -> dict`

Computes 5-day (MA5) and 20-day (MA20) moving averages from 60 days of closing prices.

Returns: `ma5`, `ma20`, `trend_signal` (BULLISH/BEARISH/NEUTRAL), `trend_explanation`, `price_change_30d`

**Signal logic:**
- BULLISH → MA5 > MA20 by >0.5% (short-term momentum above mid-term)
- BEARISH → MA5 < MA20 by >0.5% (short-term momentum below mid-term)
- NEUTRAL → MA5 and MA20 within 0.5% of each other

### `get_news(ticker: str) -> dict`

Returns up to 5 recent news headlines from Yahoo Finance's news feed.

Returns: `headlines` (list of strings)

---

## Deployment

Deployed on Railway using Docker. ConnectOnion's `host()` function binds to the port Railway provides via the `PORT` environment variable.

Environment variables required in Railway dashboard:
- `OPENAI_API_KEY` — your OpenAI key

```bash
# Deploy
railway login
railway link
railway up
```

---

## Limitations

- **15-minute data delay** — yfinance is not real-time
- **US markets only** — NYSE and NASDAQ tickers
- **MA signals are simple indicators** — not a complete trading system, not financial advice
- **News availability varies** — smaller stocks may have fewer headlines

---

## About the Author

David Chen — final-year CS (AI) student at UNSW Sydney, graduating May 2026.  
Previously interned at Hundsun Technologies (SQL/data pipelines for financial systems) and SUPERPOP Information Technology (full-stack React/Node.js).

GitHub: [chyd198](https://github.com/chyd198)  
Built as a portfolio project using the [ConnectOnion](https://connectonion.com) framework.
