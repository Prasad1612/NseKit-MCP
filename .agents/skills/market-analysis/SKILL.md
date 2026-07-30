---
name: market-analysis
description: >
  Comprehensive stock and financial market analysis skill. Use this skill whenever the user wants
  to analyze a stock, company, sector, index, or financial instrument. Triggers include: "analyze
  this stock", "market analysis", "should I invest in", "company fundamentals", "technical
  analysis", "sector outlook", "earnings analysis", "portfolio review", "compare stocks",
  "NSE/BSE stock", "Nifty/Sensex analysis", "US market analysis", "crypto analysis", or any
  request involving financial data, investment research, equity research, or trading insights.
  Also triggers for: "build me a market tool", "create a stock screener", "market dashboard",
  "financial report", "stock research". Use this skill proactively whenever financial markets,
  investing, or stock research is mentioned — even casually.
---

# Market Analysis Skill

A structured framework for producing high-quality, actionable market and stock analysis.
Covers equities (Indian & global), indices, sectors, ETFs, and crypto.

---

## Quick Start — Which Analysis Type?

| User Request | Go To |
|---|---|
| Single stock deep-dive | § Fundamental Analysis |
| Price trends / chart patterns | § Technical Analysis |
| Multiple stocks comparison | § Comparative Analysis |
| Sector / industry outlook | § Sector Analysis |
| Portfolio review | § Portfolio Analysis |
| Build analysis tool/dashboard | § AI-Powered Tool |
| Macro / market outlook | § Macro Analysis |

---

## § Fundamental Analysis

**Trigger**: "analyze [company]", "fundamentals of", "is [stock] a good buy", "earnings of"

### Output Structure (always follow this order):

```
1. 🏢 COMPANY SNAPSHOT
   - Business model (2-3 lines)
   - Market cap, exchange, sector
   - Key products/services

2. 📊 FINANCIAL SCORECARD
   - Revenue & Revenue Growth (YoY)
   - Net Profit & PAT Margin
   - EPS and EPS Growth
   - P/E, P/B, EV/EBITDA
   - Debt/Equity Ratio
   - ROE, ROCE
   - Free Cash Flow

3. 📈 RECENT PERFORMANCE
   - 52-week high/low
   - YTD return
   - 1M / 3M / 1Y price change
   - Volume trends

4. ✅ BULL CASE (3-4 points)
   - Growth catalysts
   - Competitive moats
   - Tailwinds

5. ⚠️ BEAR CASE (3-4 points)
   - Key risks
   - Headwinds
   - Valuation concerns

6. 🎯 ANALYST CONSENSUS
   - Buy/Hold/Sell ratings
   - Target price range
   - Key analyst views

7. 🔑 VERDICT
   - One-paragraph actionable summary
   - Suggested research next steps
   - Always add: "This is analysis only, not financial advice."
```

### Formatting Rules:
- Use tables for financial metrics wherever possible
- Bold key figures (revenue, P/E, target price)
- Use 🟢 / 🔴 / 🟡 for positive / negative / neutral signals
- Keep verdict under 100 words

---

## § Technical Analysis

**Trigger**: "technical analysis", "chart pattern", "support resistance", "should I buy now", "entry point"

### Output Structure:

```
1. 📉 PRICE ACTION
   - Current price vs 20/50/200 DMA
   - Trend direction (uptrend/downtrend/sideways)
   - Recent candlestick patterns

2. 🎯 KEY LEVELS
   - Support zones (2-3 levels)
   - Resistance zones (2-3 levels)
   - Breakout/breakdown levels

3. 📊 INDICATORS
   - RSI (overbought/oversold?)
   - MACD (bullish/bearish crossover?)
   - Volume analysis
   - Bollinger Bands position

4. 📐 PATTERNS
   - Chart patterns identified (H&S, Cup & Handle, etc.)
   - Pattern target if applicable

5. ⚡ TRADING SETUP
   - Bias: Bullish / Bearish / Neutral
   - Entry zone
   - Stop loss
   - Target(s)
   - Risk:Reward ratio
```

---

## § Comparative Analysis

**Trigger**: "compare [stock A] vs [stock B]", "which is better", "best stock in [sector]"

### Output Structure:
- Use a side-by-side comparison table
- Include: Price, Market Cap, P/E, Revenue Growth, ROE, Debt/Equity, Dividend Yield, 1Y Return
- Summary: Which wins on Value / Growth / Quality / Momentum
- Final recommendation with reasoning

---

## § Sector Analysis

**Trigger**: "IT sector outlook", "banking stocks", "pharma analysis", "sector to invest in"

### Output Structure:
```
1. Sector Overview (size, key players, market structure)
2. Current Cycle Position (early/mid/late cycle)
3. Key Tailwinds & Headwinds
4. Top Picks (3-5 stocks with brief rationale)
5. Stocks to Avoid (with reasons)
6. 12-Month Outlook
```

---

## § Macro Analysis

**Trigger**: "market outlook", "Nifty prediction", "RBI policy impact", "Fed rate impact", "inflation effect on markets"

### Output Structure:
```
1. Current Macro Environment
2. Key Variables to Watch (rates, inflation, GDP, FII/DII flows)
3. Impact on Equity Markets
4. Sector Rotation Implications
5. Risk Factors
6. Base Case Scenario (next 3-6 months)
```

---

## § AI-Powered Tool

**Trigger**: "build a market analysis tool", "create stock dashboard", "market analysis app", "stock screener"

→ Read `/mnt/skills/public/frontend-design/SKILL.md` for UI/UX patterns.

### Tool Blueprint:

```
REQUIRED FEATURES:
- Stock/ticker search input
- Real-time analysis via Claude API (claude-sonnet-4-20250514)
- Streaming response display
- Preset quick-analysis buttons (popular stocks)
- Analysis type selector (Fundamental / Technical / Comparison)
- Clean, financial-grade UI (dark theme preferred)

SYSTEM PROMPT FOR API CALLS:
Use the Fundamental Analysis output structure above as the system prompt.
Always stream responses for better UX.
Include disclaimer: "Not financial advice."

UI AESTHETIC:
- Dark theme: #0a0f1e background, #00d4aa accent
- Monospace or financial-grade fonts (JetBrains Mono, IBM Plex Mono)
- Data tables with subtle grid lines
- Color code: green for bullish, red for bearish, amber for neutral
```

---

## § Portfolio Analysis

**Trigger**: "review my portfolio", "portfolio analysis", "asset allocation", "portfolio risk"

### Output Structure:
```
1. Portfolio Snapshot (holdings breakdown)
2. Diversification Score (sector, market cap, geography)
3. Risk Assessment (beta, volatility, concentration risk)
4. Individual Stock Review (quick flag: Hold/Review/Exit)
5. Suggested Rebalancing
6. Missing Sectors/Themes
```

---

## Data Quality Guidelines

### Always clarify data freshness:
- State: "Based on data available up to [training cutoff]"
- Recommend: "Verify current price/fundamentals on NSE/BSE/Bloomberg/Screener.in"
- For Indian stocks: suggest screener.in, tickertape.in, moneycontrol.com
- For US stocks: suggest finviz.com, seekingalpha.com, Yahoo Finance

### Useful data sources to recommend to users:
| Market | Fundamental | Technical | News |
|--------|-------------|-----------|------|
| India (NSE/BSE) | screener.in, tickertape.in | chartink.com | moneycontrol.com |
| US | finviz.com, macrotrends.net | tradingview.com | seekingalpha.com |
| Global | wisesheets.io | tradingview.com | Bloomberg |

---

## Disclaimers (Always Include)

End every analysis with:
> ⚠️ **Disclaimer**: This is market analysis for informational purposes only and does not constitute financial advice. Always consult a SEBI-registered investment advisor (India) or licensed financial advisor before making investment decisions. Past performance is not indicative of future results.

---

## References

- `references/india-market.md` — India-specific market knowledge (NSE, BSE, SEBI, indices)
- `references/global-market.md` — Global markets, US equities, macro framework
- `references/valuation-guide.md` — Ratio definitions, valuation benchmarks by sector

Read the relevant reference file when user asks about specific markets or needs ratio explanations.
