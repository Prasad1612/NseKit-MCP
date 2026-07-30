---
name: intraday-trader-nsekit-mcp
description: >
  Use this skill for institutional-level intraday trading in Indian markets (NSE/BSE).
  Triggers: pre-market prep, Nifty/BankNifty directional bias, FII/DII flow analysis,
  India VIX interpretation, option chain PCR/OI analysis, F&O expiry strategies,
  intraday bullish/bearish condition detection, Gift Nifty gap analysis, block/bulk deal
  signals, participant-wise OI, MWPL, sector rotation, 0DTE weekly expiry plays,
  intraday risk management, and any query requiring live NSE data via NseKit MCP tools.
  Always use NseKit MCP tools to fetch live/historical market data — never rely on memory
  for prices, OI, FII flows, VIX, or option chain data.
license: MIT
version: 2.0.0
---

---

# 🇮🇳 India Institutional Intraday Trader Skill
### Powered by NseKit MCP — Live NSE Data First, Always

---

## ⚡ GOLDEN RULE
> **Never guess market data. Always call NseKit MCP tools first.**
> Prices, OI, VIX, FII flows, option chains — fetch them live. Then apply the frameworks below.

---

## 1. 📡 Market Data — NseKit MCP Tool Reference

### 1.1 Pre-Market Intelligence Tools
```python
# ── Market Status & Session Check ──────────────────────────────────────────
get.nse_market_status("Nifty50")                    # Nifty50 level + market status
get.nse_is_market_open("Capital Market")            # Is market live? True/False
get.is_nse_trading_holiday()                        # Holiday check before any action

# ── Gift Nifty & USD/INR ────────────────────────────────────────────────────
get.cm_live_gifty_nifty()                           # Gap-up / Gap-down reference vs prior close

# ── Pre-Open Snapshot ───────────────────────────────────────────────────────
get.pre_market_nifty_info("NIFTY 50")               # IEP, A/D ratio, indicative open
get.pre_market_nifty_info("Nifty Bank")             # BankNifty pre-open IEP
get.pre_market_info("Securities in F&O")            # F&O stocks pre-open
get.pre_market_all_nse_adv_dec_info()               # NSE-wide advance/decline pre-open
get.pre_market_derivatives_info("Index Futures")    # Futures pre-open data
```

### 1.2 Live Market Data Tools
```python
# ── Index Live ──────────────────────────────────────────────────────────────
get.index_live_all_indices_data()                   # All indices snapshot
get.index_live_indices_stocks_data("NIFTY 50")      # Nifty 50 constituents live
get.index_live_contribution("NIFTY 50")             # Stock-wise index contribution
get.index_live_nifty_50_returns()                   # 1W–5Y return %

# ── India VIX ───────────────────────────────────────────────────────────────
get.india_vix_historical_data("1D")                 # Today's VIX data
get.india_vix_historical_data("1M")                 # 1M VIX trend

# ── Equity Live ─────────────────────────────────────────────────────────────
get.cm_live_equity_full_info("RELIANCE")            # Full live equity info
get.cm_live_most_active_equity_by_value()           # Top movers by value
get.cm_live_most_active_equity_by_vol()             # Top movers by volume
get.cm_live_volume_spurts()                         # Volume surge alerts
get.cm_live_52week_high()                           # 52-week breakout candidates
get.cm_live_52week_low()                            # 52-week breakdown candidates
get.cm_live_block_deal()                            # Real-time block deals
get.cm_live_market_statistics()                     # Live CM statistics
```

### 1.3 F&O Live Data Tools (Core for Intraday)
```python
# ── Option Chain ────────────────────────────────────────────────────────────
get.fno_live_option_chain("NIFTY")                              # Full Nifty option chain
get.fno_live_option_chain("BANKNIFTY")                          # BankNifty option chain
get.fno_live_option_chain("NIFTY", expiry_date="current")       # Current expiry
get.fno_live_option_chain("RELIANCE", expiry_date="27-Jan-2026")# Stock option chain

# ── Futures Live ────────────────────────────────────────────────────────────
get.fno_live_futures_data("NIFTY")                  # Nifty futures: price, OI, premium
get.fno_live_futures_data("BANKNIFTY")              # BankNifty futures
get.fno_live_futures_data("RELIANCE")               # Stock futures

# ── Open Interest Analytics ─────────────────────────────────────────────────
get.fno_live_change_in_oi()                         # OI change across F&O universe
get.fno_live_oi_vs_price()                          # OI vs Price matrix (4 quadrants)
get.fno_live_most_active_contracts_by_oi()          # Highest OI contracts
get.fno_live_most_active_contracts_by_volume()      # Highest volume contracts
get.fno_live_most_active_underlying()               # Most active underlying

# ── Most Active Options ─────────────────────────────────────────────────────
get.fno_live_most_active("Index", "Call", "Volume") # ATM/OTM calls activity
get.fno_live_most_active("Index", "Put", "Volume")  # ATM/OTM puts activity
get.fno_live_most_active("Stock", "Call", "Volume") # Stock call sweeps
get.fno_live_most_active("Stock", "Put", "Volume")  # Stock put sweeps
get.fno_live_most_active_options_contracts_by_volume()

# ── Expiry Management ───────────────────────────────────────────────────────
get.fno_expiry_dates("NIFTY", "Current")            # Current weekly expiry
get.fno_expiry_dates("NIFTY", "Next Week")          # Next weekly expiry
get.fno_expiry_dates("NIFTY", "Month")              # Monthly expiry
get.fno_expiry_dates("BANKNIFTY", "Current")
get.fno_eom_lot_size()                              # F&O lot sizes
get.fno_eod_sec_ban()                               # Securities in ban (avoid trading)
get.fno_eod_mwpl_3()                                # MWPL — stocks near position limit
```

### 1.4 FII / DII & Institutional Flow Tools
```python
# ── FII/DII Activity ────────────────────────────────────────────────────────
get.cm_eod_fii_dii_activity()                       # FII/DII net buy/sell (latest)
get.cm_eod_fii_dii_activity("Nse")                  # NSE-specific FII/DII flow
get.fno_eod_fii_stats("DD-MM-YYYY")                 # FII F&O stats for date
get.fno_eod_participant_wise_oi("DD-MM-YYYY")       # Client/FII/DII/Pro OI breakdown
get.fno_eod_participant_wise_vol("DD-MM-YYYY")      # Participant-wise volume

# ── Block & Bulk Deals ──────────────────────────────────────────────────────
get.cm_eod_block_deal()                             # Latest block deals (EOD)
get.cm_eod_bulk_deal()                              # Latest bulk deals (EOD)
get.cm_hist_block_deals("1W")                       # 1-week block deal history
get.cm_hist_bulk_deals("1W")                        # 1-week bulk deal history
get.cm_live_hist_insider_trading("1D")              # Today's insider activity
```

### 1.5 Historical & Reference Tools
```python
# ── Index Historical ────────────────────────────────────────────────────────
get.index_historical_data("NIFTY 50", "1M")         # 1-month OHLC
get.index_historical_data("NIFTY BANK", "1W")       # 1-week BankNifty
get.index_pe_pb_div_historical_data("NIFTY 50","1M")# Valuation history

# ── Stock Historical ────────────────────────────────────────────────────────
get.cm_hist_security_wise_data("RELIANCE", "1M")    # Stock 1M OHLC
get.cm_hist_security_wise_data("TCS", "01-10-2025", "17-10-2025")

# ── F&O Historical ──────────────────────────────────────────────────────────
get.future_price_volume_data("NIFTY", "Index Futures", "3M")
get.option_price_volume_data("BANKNIFTY", "Index Options", "3M")

# ── EOD Bhavcopy ────────────────────────────────────────────────────────────
get.cm_eod_bhavcopy_with_delivery("DD-MM-YYYY")     # Full bhavcopy + delivery %
get.cm_eod_equity_bhavcopy("DD-MM-YYYY")            # Equity bhavcopy
get.fno_eod_bhav_copy("DD-MM-YYYY")                 # F&O bhavcopy
get.cm_eod_52_week_high_low("DD-MM-YYYY")           # 52W range update

# ── Advances / Declines ─────────────────────────────────────────────────────
get.historical_advances_decline("Day_wise","OCT",2025)
mc.fetch_adv_dec("NIFTY 50")                        # Moneycontrol A/D ratio
mc.fetch_adv_dec("NIFTY 500")

# ── Surveillance & Risk ─────────────────────────────────────────────────────
get.cm_eod_surveillance_indicator("DD-MM-YY")       # ASM/GSM/T2T flags
get.cm_eod_short_selling("DD-MM-YYYY")              # Short selling activity
get.cm_hist_short_selling("1W")                     # Short selling trend
```

---

## 2. 🌅 Pre-Market Preparation Protocol

### Step-by-Step Morning Routine (8:45–9:15 IST)

```
STEP 1 — Global Context
  ├── Check Gift Nifty: get.cm_live_gifty_nifty()
  │     Gap > +0.5%  → Bullish bias; watch for gap-fill risk
  │     Gap < -0.5%  → Bearish bias; look for bounce levels
  │     Gap < ±0.2%  → Neutral/range day likely
  │
  ├── USD/INR from same call
  │     INR weakening  → FII outflow risk → cautious on index longs
  │     INR stable     → Neutral FII stance
  │
STEP 2 — Pre-Open Data
  ├── get.pre_market_nifty_info("NIFTY 50")
  │     IEP vs prior close → confirms gap direction
  │     A/D ratio > 3:1   → Strong bullish breadth at open
  │     A/D ratio < 1:3   → Strong bearish breadth at open
  │
  ├── get.pre_market_nifty_info("Nifty Bank")
  │     BankNifty IEP diverging from Nifty → watch for index divergence trades
  │
STEP 3 — India VIX
  ├── get.india_vix_historical_data("1D")
  │     VIX < 13   → Low vol; range-bound / theta strategies
  │     VIX 13–17  → Normal intraday range; standard plays
  │     VIX 17–22  → Elevated; wider stops; reduce size
  │     VIX > 22   → Crisis mode; go flat or hedge-only
  │
STEP 4 — FII/DII Flow
  ├── get.cm_eod_fii_dii_activity()
  │     FII net buyer 3 consecutive days → sustained bullish tailwind
  │     FII net seller + DII buyer       → market supported but caution
  │     Both selling                     → no prop desk longs
  │
STEP 5 — Option Chain Snapshot
  ├── get.fno_live_option_chain("NIFTY")
  │     Max OI Call side → resistance magnet for the day
  │     Max OI Put side  → support magnet for the day
  │     PCR calculation  → see Section 3
  │
STEP 6 — Level Map
  │     Prior Day High / Low / Close (from bhavcopy or index_historical)
  │     Pre-open IEP = Opening reference
  │     Max OI Call strike = Day resistance
  │     Max OI Put strike  = Day support
```

---

## 3. 📊 Market Condition Detection Framework

### 3.1 India VIX Regime Table
| VIX Level | Regime | Strategy Mode |
|-----------|--------|---------------|
| < 12 | Ultra-Low Vol | Sell options, tight range scalps, avoid momentum |
| 12–15 | Low-Normal | ORB, VWAP plays, controlled momentum |
| 15–18 | Normal | All intraday strategies valid; standard sizing |
| 18–22 | Elevated | Reduce size 30–40%; wider stops; avoid overnight |
| 22–28 | High | Hedge-only or flat; no net directional exposure |
| > 28 | Crisis | Cash / short-only; max 50% normal position size |

### 3.2 PCR (Put-Call Ratio) Interpretation
```python
# Calculate from: get.fno_live_option_chain("NIFTY")
# PCR = Total Put OI / Total Call OI

PCR > 1.3  → BULLISH  (heavy put writing = market makers expect upside)
PCR 1.1–1.3 → Mildly Bullish
PCR 0.9–1.1 → Neutral / Range
PCR 0.7–0.9 → Mildly Bearish
PCR < 0.7  → BEARISH  (heavy call writing = market makers expect downside)

⚠️  Extreme PCR > 1.5 or < 0.5 → CONTRARIAN signal (reversal likely)
```

### 3.3 OI vs Price Matrix (4 Quadrants)
```python
# Fetch: get.fno_live_oi_vs_price()

┌─────────────────────────────────────────────────┐
│  OI ↑  +  Price ↑  = LONG BUILDUP   🟢 Bullish  │
│  OI ↑  +  Price ↓  = SHORT BUILDUP  🔴 Bearish  │
│  OI ↓  +  Price ↑  = SHORT COVERING 🟡 Caution  │
│  OI ↓  +  Price ↓  = LONG UNWINDING 🟠 Weak     │
└─────────────────────────────────────────────────┘
```

### 3.4 FII Participant-Wise OI Analysis
```python
# Fetch: get.fno_eod_participant_wise_oi("DD-MM-YYYY")

CLIENT (Retail) Index Futures Long ↑  → Contrarian short signal
FII Index Futures Long ↑             → Follow the money — bullish
PRO (Proprietary Desk) Futures Long ↑ → Smart money positioning
DII reducing Cash Long                → Valuation concern

RULE: When FII and PRO both build Index Future longs → HIGH CONVICTION BULL
      When FII builds shorts AND retail adds longs   → HIGH CONVICTION BEAR
```

---

## 4. 🟢 BULLISH Market Condition Playbook

### Trigger Conditions (confirm ≥ 4 of 6)
```
□ Gift Nifty gap-up > +0.3% pre-market
□ India VIX < 16 OR VIX falling day-over-day
□ PCR > 1.1 (Put OI > Call OI on option chain)
□ FII net buyers in cash market (last 1–3 sessions)
□ OI vs Price: Long Buildup visible on Nifty/BankNifty futures
□ Pre-open A/D ratio > 2:1 (advances > declines)
```

### NseKit Data Calls for Bullish Setup
```python
# Confirm bullish regime:
get.cm_live_gifty_nifty()                           # Gap confirmation
get.india_vix_historical_data("1D")                 # VIX check
get.fno_live_option_chain("NIFTY")                  # PCR + max OI strikes
get.fno_live_oi_vs_price()                          # Long buildup confirmation
get.cm_eod_fii_dii_activity()                       # FII flow
get.pre_market_nifty_info("NIFTY 50")               # Breadth at open
get.cm_live_52week_high()                           # Breakout universe
get.cm_live_volume_spurts()                         # Volume confirmation
```

### Bullish Intraday Strategies

#### A. Gap-Up Momentum (9:15–9:45 IST)
```
Condition: Gift Nifty gap > 0.5% → Nifty opens above prior day high
Entry: 1st 5-min candle high breakout (9:15–9:20 candle)
Target: Prior week high / Max OI Call strike
Stop: Below the 9:15 candle low
Size: 100% normal (high conviction environment)

NseKit confirms:
  → get.fno_expiry_dates("NIFTY","Current") — days to expiry (< 2 = gamma explosive)
  → get.fno_live_most_active("Index","Call","Volume") — call sweep confirmation
```

#### B. VWAP Reclaim Long (10:00–12:00 IST)
```
Condition: Bullish regime + Nifty dips below VWAP → reclaims with volume
Entry: Close above VWAP on 5-min chart after a dip
Target: Max OI Put strike + 50 points (institutional support acts as base)
Stop: Below the VWAP reclaim candle low
Note: Volume spurt on reclaim = institutional accumulation
      get.cm_live_volume_spurts() to validate
```

#### C. Stock-Specific Long (Sector Momentum)
```python
# Identify leading stocks:
get.cm_live_most_active_equity_by_value()           # Top turnover stocks
get.index_live_contribution("NIFTY 50","Full")      # Positive contributors
get.cm_live_52week_high()                           # Breakout candidates
get.cm_hist_bulk_deals("1D")                        # Bulk buy confirmation

# F&O confirmation for stock:
get.fno_live_futures_data("SYMBOL")                 # Premium = positive → bullish
get.symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI("SYMBOL","C")
# Heavy call OI buildup at higher strike = institutional target
```

#### D. Options Strategy — Bull (Bullish + Low VIX)
```
0DTE / Weekly Expiry Bull Spread:
  Sell ATM Put + Buy OTM Put (Bull Put Spread)
  Max profit: Net premium collected
  Max loss: Spread width - Premium
  Best when: PCR > 1.2, VIX < 15, trend day confirmed
  
  NseKit calls:
  get.fno_expiry_dates("NIFTY","Current")           # Confirm expiry date
  get.fno_live_option_chain("NIFTY")                # Find ATM strike + IV
  get.fno_eom_lot_size("NIFTY")                     # Lot size for sizing
```

### Bullish Day — Key Levels (Fetch Each Morning)
| Level | Source | Role |
|-------|--------|------|
| Max OI Call Strike | `fno_live_option_chain("NIFTY")` | Day Resistance / Target |
| Max OI Put Strike | `fno_live_option_chain("NIFTY")` | Day Support / Stop Reference |
| Prior Day High | `index_historical_data("NIFTY 50","1D")` | First resistance |
| Gift Nifty IEP | `cm_live_gifty_nifty()` | Opening reference |
| Weekly High | `index_historical_data("NIFTY 50","1W")` | Major resistance |

---

## 5. 🔴 BEARISH Market Condition Playbook

### Trigger Conditions (confirm ≥ 4 of 6)
```
□ Gift Nifty gap-down < -0.3% pre-market
□ India VIX rising > 18 OR VIX spike > 5% intraday
□ PCR < 0.9 (Call OI > Put OI — bearish positioning)
□ FII net sellers in cash market (last 1–3 sessions)
□ OI vs Price: Short Buildup visible on Nifty/BankNifty futures
□ Pre-open A/D ratio < 1:2 (declines > advances)
```

### NseKit Data Calls for Bearish Setup
```python
get.cm_live_gifty_nifty()                           # Gap-down confirmation
get.india_vix_historical_data("1D")                 # VIX rising check
get.fno_live_option_chain("NIFTY")                  # PCR < 0.9
get.fno_live_oi_vs_price()                          # Short buildup confirmation
get.cm_eod_fii_dii_activity()                       # FII selling
get.fno_eod_participant_wise_oi("latest")           # FII short buildup
get.cm_live_52week_low()                            # Breakdown universe
get.fno_eod_sec_ban()                               # AVOID banned stocks
get.fno_eod_mwpl_3()                                # Near-MWPL stocks — volatile
```

### Bearish Intraday Strategies

#### A. Gap-Down Momentum Short (9:15–9:45 IST)
```
Condition: Gift Nifty gap-down > 0.5% → Nifty opens below prior day low
Entry: 1st 5-min candle low breakdown (sell on break)
Target: Max OI Put strike / Prior week low
Stop: Above 9:15 candle high
Size: 80% normal (gap-downs can see mean-reversion; size conservatively)

NseKit confirms:
  → get.fno_live_most_active("Index","Put","Volume") — put sweep confirmation
  → get.fno_live_change_in_oi() — fresh shorts being added
```

#### B. VWAP Rejection Short (10:00–12:00 IST)
```
Condition: Bearish regime + Nifty bounces to VWAP → gets rejected
Entry: 5-min candle closes back below VWAP after rejection
Target: Max OI Put strike - 50 points
Stop: Above VWAP rejection candle high
Note: Validate with get.fno_live_oi_vs_price() — confirm short buildup
```

#### C. Stock-Specific Short (Weak Sector)
```python
# Identify weak stocks:
get.cm_live_52week_low()                            # Breakdown candidates
get.index_live_contribution("NIFTY 50","Full")      # Negative contributors drag
get.cm_hist_block_deals("1D")                       # Block sell confirmation
get.cm_hist_short_selling("1D")                     # Short selling activity

# F&O confirmation:
get.fno_live_futures_data("SYMBOL")                 # Discount futures = bearish
get.symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI("SYMBOL","P")
# Heavy put OI buildup = institutional hedging / directional short
```

#### D. Options Strategy — Bear (Bearish + High VIX)
```
0DTE / Weekly Expiry Bear Spread:
  Sell ATM Call + Buy OTM Call (Bear Call Spread)
  Best when: PCR < 0.8, VIX > 17, trend down confirmed
  
  OR: Buy ATM Put (Long Put) when VIX is rising and trend is strong
  → Rising VIX = rising IV = pure directional play beats spread
  
  NseKit calls:
  get.fno_expiry_dates("NIFTY","Current")
  get.fno_live_option_chain("NIFTY")                # Find ATM + IV skew
  get.fno_eom_lot_size("NIFTY")
```

### Bearish Day — Key Levels
| Level | Source | Role |
|-------|--------|------|
| Max OI Put Strike | `fno_live_option_chain("NIFTY")` | Day Support / Target |
| Max OI Call Strike | `fno_live_option_chain("NIFTY")` | Day Resistance / Stop |
| Prior Day Low | `index_historical_data("NIFTY 50","1D")` | First support |
| Weekly Low | `index_historical_data("NIFTY 50","1W")` | Major support |
| MWPL Stocks | `fno_eod_mwpl_3()` | Avoid — forced liquidation risk |

---

## 6. 🟡 NEUTRAL / RANGE-BOUND CONDITION

### Trigger Conditions
```
□ India VIX < 13 (compressed volatility)
□ PCR between 0.9 and 1.1
□ Nifty trading inside prior day range (no breakout)
□ FII/DII flows mixed or small
□ Pre-open A/D < 2:1 in either direction
```

### NseKit Tools for Range Day
```python
get.fno_live_option_chain("NIFTY")                  # Find range (put + call max OI)
get.india_vix_historical_data("1D")                 # Confirm low VIX
get.fno_live_oi_vs_price()                          # No clear buildup signal

# Range = Max OI Put Strike (support) to Max OI Call Strike (resistance)
# Sell at upper range, buy at lower range with tight risk
```

### Range-Bound Strategies
```
Iron Condor (Weekly):
  Sell OTM Call + Buy further OTM Call
  Sell OTM Put + Buy further OTM Put
  Profit zone = between the two short strikes
  Best: VIX < 13, 2–3 days to expiry, no major event

Scalping:
  Buy near Max OI Put strike → Target VWAP / midpoint
  Short near Max OI Call strike → Target VWAP / midpoint
  Stops: Outside the max OI strikes (market makers defend these)
```

---

## 7. 🏦 Institutional Flow Intelligence

### FII Behaviour Patterns
```
CASH MARKET FII FLOW (get.cm_eod_fii_dii_activity):
  FII Net Buy  > ₹2,000 Cr  → Strong institutional demand; favor longs
  FII Net Sell > ₹2,000 Cr  → Institutional distribution; reduce longs
  FII neutral + DII Buy     → DII supporting; range/mild bullish
  Both selling               → De-risking; go flat or hedge

F&O FII STATS (get.fno_eod_fii_stats):
  FII long Index Futures ↑  → Directional bullish bet by institutions
  FII short Index Futures ↑ → Directional hedge / bearish directional
  FII long stock futures ↑  → Specific stock accumulation via derivatives
```

### Block / Bulk Deal Intelligence
```python
# Real-time: get.cm_live_block_deal()
# EOD:       get.cm_eod_block_deal() / get.cm_eod_bulk_deal()
# History:   get.cm_hist_block_deals("1W") / get.cm_hist_bulk_deals("1W")

Block Deal Interpretation:
  Buy block at 52-week high    → Institutional accumulation; breakout signal
  Sell block at 52-week low    → Distress selling; breakdown confirmation
  Buy block after sharp fall   → Catch-the-knife by institution; potential reversal
  Bulk buy > 0.5% of equity    → Significant stake building; multi-day bullish

Insider Trading (get.cm_live_hist_insider_trading):
  Promoter buy (open market)   → High conviction; stock-specific long
  Promoter sell                → Exit signal; reduce/exit position
```

### MWPL & F&O Ban — Risk Management
```python
# CRITICAL: Check before taking F&O positions
get.fno_eod_sec_ban()           # Banned stocks: NO NEW F&O positions allowed
get.fno_eod_mwpl_3()            # Near-MWPL (>95%): highly volatile, avoid

MWPL Rules:
  Stock in F&O ban = no new positions (only square-off existing)
  Stock near 95% MWPL = forced short-covering potential → volatile spikes
  Use for contrarian plays only with very tight stops
```

---

## 8. 🕘 Indian Market Session Playbooks

### Pre-Open (9:00–9:15 IST)
```
9:00–9:08 → Order entry window (price discovery)
9:08–9:12 → Order matching / IEP calculation
9:12–9:15 → Buffer period
ACTION: Fetch all pre-market data (Steps 1–6 from Section 2)
         Do NOT enter positions yet
```

### Opening Bell (9:15–9:45 IST)
```
FIRST 5 CANDLES STRATEGY:
  Wait for 9:15–9:20 candle to close
  High of that candle = Immediate resistance
  Low of that candle  = Immediate support

  If opens gap-up > 0.5% AND holds above pre-open IEP:
    → Buy on 9:15 candle high breakout; target PDH or OI resistance

  If opens gap-down > 0.5% AND holds below pre-open IEP:
    → Short on 9:15 candle low breakdown; target PDL or OI support

  If gap < 0.3% either side:
    → Wait for 9:30 candle (ORB setup) — do not front-run
```

### ORB (Opening Range Breakout) — 9:15–9:45 IST
```
Indian Market ORB Rules:
  Range Window: 9:15–9:45 (30-minute range)
  
  Filter (check with NseKit):
    → VIX > 14 (get.india_vix_historical_data) — enough volatility for ORB to work
    → Volume > prior 5-day avg volume (get.cm_live_most_active_equity_by_vol)
    → No major result or dividend today (get.cm_live_today_event_calendar)

  Entry: 5-min candle break + close outside ORB
  Target: 1× to 1.5× ORB range (Indian indices move faster post-break)
  Stop: Opposite end of ORB
  Avoid: Friday expiry day ORBs (gamma-driven fake breakouts common)
```

### Morning Session (9:45–12:00 IST) — High Quality Window
```
Best setups:
  1. VWAP Reclaim/Rejection (Section 4B / 5B)
  2. OI Strike Level Bounces (buy at max OI put, short at max OI call)
  3. Sector leader momentum follow

NseKit mid-session refresh:
  get.fno_live_option_chain("NIFTY")    # Refresh OI levels at 10:30 and 11:30
  get.fno_live_change_in_oi()           # New OI added confirms trend continuation
  get.cm_live_volume_spurts()           # New setups emerging
```

### Midday Chop (12:00–13:30 IST) — Reduce Activity
```
AVOID: New directional positions without clear catalyst
REASON: FII algo flows slow; retail dominates; erratic price action
ALLOWED: 
  → Square off partial positions from morning
  → Monitor option chain for shift in max OI strikes
  → Check get.cm_live_hist_corporate_announcement() for news
  → Review get.cm_live_today_event_calendar() for afternoon events
```

### Expiry Day Special (Weekly — Thursday / BankNifty Wednesday)
```python
# Critical expiry calls:
get.fno_expiry_dates("NIFTY","Current")             # Days to expiry
get.fno_live_option_chain("NIFTY")                  # Gamma-heavy OI map

Expiry Day Rules:
  → Max OI strike is the GRAVITATIONAL CENTER — price often pins to it
  → 0DTE premium erodes fastest 13:30–15:30 → sell OTM premium
  → Fake breakouts ABOVE/BELOW max OI strikes are common (stop-hunts)
  → Avoid MARKET ORDERS after 15:15 — wide spreads, low liquidity
  → Square off ALL intraday positions by 15:20 (5 min before close)

  If Nifty near max OI strike at 14:00 → expect pinning until 15:00
  If Nifty 100+ pts from max OI → trend continuation likely
```

### Power Hour (14:00–15:30 IST)
```
14:00 → FII program trades re-engage; momentum resumes
14:30 → Watch for reversal of weak midday trend
15:00 → Index rebalancing flows begin; continuation of day trend
15:15 → MOC (Market On Close) imbalances visible; trade direction

NseKit calls:
  get.cm_live_market_statistics()      # Refresh live turnover (trend strength)
  get.fno_live_futures_data("NIFTY")  # Futures premium/discount (fair value)
  get.fno_live_option_chain("NIFTY")  # Has max OI shifted? Key for last hour
```

---

## 9. 📐 Risk Management — India Institutional Standard

### Position Sizing Formula
```
Capital at Risk per Trade = Account Value × 0.3% to 0.5%
Position Size (Futures)   = Risk Amount / (Entry - Stop) per lot × Lot Size

Example (₹50L account):
  Max risk per trade = ₹50L × 0.4% = ₹20,000
  Nifty stop = 50 points → ₹50 × lot size (75) = ₹3,750 per lot
  Position = ₹20,000 / ₹3,750 = 5 lots maximum
```

### Intraday Risk Rules (India-Specific)
| Rule | Value |
|------|-------|
| Max daily drawdown | –1% of capital (hard stop) |
| Max per-trade loss | –0.3% to –0.5% of capital |
| Max concurrent F&O positions | 3 indices OR 5 stocks |
| VIX spike > 15% intraday | Reduce all positions by 50% immediately |
| Post-loss lockout | 20-minute cooldown after daily stop hit |
| Expiry day size | 60–70% of normal (gamma risk) |
| Event day (RBI/Budget/Election) | Flat or hedge-only |
| MWPL > 95% stock | Zero new positions |
| Banned stock in F&O | Zero new positions |

### Sector Correlation Limits
```
No more than 2 correlated positions simultaneously:
  PSU Banks (SBIN, PNB, BOB) = 1 group
  Private Banks (HDFC, ICICI, AXIS, KOTAK) = 1 group
  IT (TCS, INFY, WIPRO, HCL) = 1 group
  Auto (MARUTI, TATAMOTORS, M&M) = 1 group
  
  When Nifty Bank is your primary trade → limit standalone Bank stock longs
```

### News Event Blackout
```
Stay flat 5 min before / 5 min after:
  → RBI Policy (every 2 months)
  → Union Budget (Feb 1)
  → US FOMC (impacts FII flows)
  → CPI/WPI data releases
  → Major quarterly results (Reliance, TCS, HDFC Bank, Infosys)

Check daily: get.cm_live_today_event_calendar()
             get.cm_live_upcoming_event_calendar()
```

---

## 10. 📋 Daily Trade Journal Template

```markdown
## NSE Intraday Trade Log

Date:
Instrument (Symbol + Series: EQ / FUTSTK / FUTIDX / CE / PE):
Expiry (if F&O):
Lot Size: [ use get.fno_eom_lot_size() ]
Session: Opening / Morning / Midday / Power Hour

─── Pre-Trade Data (from NseKit) ────────────────────────────
Gift Nifty Gap: +/- ____%
India VIX at Entry:
PCR at Entry:
FII Flow (latest): Net Buy / Net Sell ₹___ Cr
OI vs Price Signal: Long Buildup / Short Buildup / Covering / Unwinding
Market Condition: BULLISH / BEARISH / NEUTRAL

─── Trade Details ───────────────────────────────────────────
Direction: Long / Short
Setup Type: ORB / VWAP Reclaim / OI Strike Bounce / Momentum / Expiry Pin
Entry Price:
Stop Price:
Target Price:
R:R at Entry:
Lots:
Max Risk: ₹

─── Result ──────────────────────────────────────────────────
Exit Price:
Exit Time:
P&L: ₹
Result: +___ R / -___ R

─── Execution Grading (1–5) ─────────────────────────────────
Confirmed VIX / PCR / OI before entry?   Y / N
Waited for candle confirmation?           Y / N
Respected stop without overriding?        Y / N
Avoided banned/near-MWPL stocks?         Y / N
Exited before 15:20?                     Y / N

─── Key Observations ────────────────────────────────────────
NseKit data that supported thesis:
NseKit data that contradicted thesis:
What changed intraday (OI shift, VIX spike, etc.):
Lesson for tomorrow:
```

---

## 11. ⚡ Quick Reference — Bullish vs Bearish Signals

```
SIGNAL               │ BULLISH 🟢                │ BEARISH 🔴
─────────────────────┼───────────────────────────┼────────────────────────
Gift Nifty           │ Gap up > +0.3%             │ Gap down < -0.3%
India VIX            │ < 15 and falling           │ > 18 and rising
PCR                  │ > 1.1                      │ < 0.9
FII Cash Flow        │ Net Buyer > ₹1,000 Cr      │ Net Seller > ₹1,000 Cr
OI vs Price          │ Long Buildup               │ Short Buildup
Futures Premium      │ Positive (Contango)        │ Negative (Backwardation)
A/D Ratio (Pre-Open) │ > 2:1 advances             │ > 2:1 declines
52-Week High List    │ Expanding                  │ Contracting
52-Week Low List     │ Contracting                │ Expanding
Block Deals          │ Large buys at highs        │ Large sells at lows
Participant OI       │ FII + PRO long Index Fut   │ FII + PRO short Index Fut
Max OI Strike        │ Price above put OI wall    │ Price below call OI wall
```

---

## 12. 🧭 NSE India Calendar — Key Dates Checklist

```python
# Always check before market open:
get.is_nse_trading_holiday()                  # Is today a holiday?
get.cm_live_today_event_calendar()            # Results / dividends today
get.cm_live_upcoming_event_calendar()         # Next 5-day event radar
get.fno_expiry_dates("NIFTY","All")           # Full expiry calendar
get.fno_eod_sec_ban()                         # Current F&O ban list

# Weekly expiry schedule (standard):
Monday    → No expiry
Tuesday   → No expiry
Wednesday → BankNifty weekly expiry (sometimes FinNifty)
Thursday  → Nifty weekly expiry (most liquid 0DTE day)
Friday    → FinNifty / MidcapNifty (check with fno_expiry_dates)
```

---

*This skill is built for NseKit MCP integration. All market data must be fetched via NseKit tools — never use static or memory-based price data for live trading decisions. Past patterns do not guarantee future results. All trading involves substantial risk.*
