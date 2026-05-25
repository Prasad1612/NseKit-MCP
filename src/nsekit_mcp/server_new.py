import json
import time
from threading import Lock
from typing import Optional, Literal, Annotated

import pandas as pd
from mcp.server.fastmcp import FastMCP
from NseKit import NseKit, Moneycontrol

# ================================================================
#                   RATE LIMIT CONTROL (NSE Safe)
# ================================================================

RATE_LIMIT_SECONDS  = 0.35   # NSE safe: ~3 requests/sec
_last_call_time     = 0
_lock               = Lock()

def rate_limit():
    """Ensures minimum delay between NSE API calls."""
    global _last_call_time
    with _lock:
        now = time.time()
        elapsed = now - _last_call_time
        if elapsed < RATE_LIMIT_SECONDS:
            time.sleep(RATE_LIMIT_SECONDS - elapsed)
        _last_call_time = time.time()

# ================================================================
#                   MCP + NseKit Initialization
# ================================================================

mcp = FastMCP("NseKit-MCP", json_response=True)

get = NseKit.Nse()
mc = Moneycontrol.MC()

# ================================================================
#                   Helper: DF → JSON
# ================================================================

def df_to_json(data):
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")
    return data

def compact_args(*args):
    return [a for a in args if a is not None]

def compact_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

# =====================================================================
# MARKET STATUS & TRADING INFO
# =====================================================================

@mcp.tool()
def market_live_status(
    mode: Literal["Market Status", "Nifty50", "Mcap", "Gift Nifty"] = "Market Status"
):
    """
    Get current market status, Nifty50, total mcap, or Gift Nifty value.
    """
    rate_limit()
    return df_to_json(get.nse_market_status(mode))

@mcp.tool()
def market_is_open(
    segment: Literal["Capital Market", "Currency", "Commodity", "Debt", "currencyfuture"] = "Capital Market"
):
    """
    Check if Capital Market, Currency, Commodity or Debt segment is open.
    """
    rate_limit()
    return get.nse_is_market_open(segment)

@mcp.tool()
def market_trading_holidays_list(
    list_only: Annotated[bool, "Return only date list if True"] = False
):
    """
    Get all NSE trading holidays for current year.
    """
    rate_limit()
    return df_to_json(get.nse_trading_holidays(list_only=list_only))

@mcp.tool()
def market_clearing_holidays_list(
    list_only: Annotated[bool, "Return only dates if True"] = False
):
    """
    Get all NSE clearing/settlement holidays.
    """
    rate_limit()
    return df_to_json(get.nse_clearing_holidays(list_only=list_only))

@mcp.tool()
def market_is_trading_holiday(
    date: Annotated[str, 'Optional "DD-MM-YYYY"'] = None
):
    """
    Check if today or given date is trading holiday.
    """
    rate_limit()
    return get.is_nse_trading_holiday(date)

@mcp.tool()
def market_is_clearing_holiday(
    date: Annotated[str, 'Optional "DD-MM-YYYY"'] = None
):
    """
    Check if today or given date is clearing holiday.
    """
    rate_limit()
    return get.is_nse_clearing_holiday(date)


# =====================================================================
# LIVE MARKET & REFERENCE DATA
# =====================================================================

@mcp.tool()
def market_live_turnover():
    """Real-time turnover across Equity, F&O, Currency, Commodity segments."""
    rate_limit()
    return df_to_json(get.nse_live_market_turnover())

@mcp.tool()
def currency_reference_rates():
    """Official NSE USD, EUR, GBP, JPY reference rates."""
    rate_limit()
    return df_to_json(get.nse_reference_rates())

@mcp.tool()
def gift_nifty_live():
    """Current Gift Nifty futures price and USDINR rate."""
    rate_limit()
    return df_to_json(get.cm_live_gifty_nifty())

@mcp.tool()
def market_live_statistics():
    """
    Live capital market stats: Count of Advances, Declines, Unchanged, 
    52W High, 52W Low, Upper Circuit, Lower Circuit, Market Cap ₹ Lac Crs, 
    Market Cap Tn $, Registered Investors (Raw), Registered Investors (Cr).
    """
    rate_limit()
    return df_to_json(get.cm_live_market_statistics())

@mcp.tool()
def avg_order_ack_latency():
    """NSE's current average order acknowledgement latency in nanoseconds."""
    rate_limit()
    return df_to_json(get.latency_nanosec())


# =====================================================================
# PRE-OPEN & INDEX LIVE
# =====================================================================

@mcp.tool()
def preopen_index_summary(
    index_name: Literal["NIFTY 50", "Nifty Bank", "Emerge", "Securities in F&O", "Others", "All"] = "NIFTY 50"
):
    """
    Pre-open advance/decline for Nifty 50, Bank, Emerge, F&O, Others.
    """
    rate_limit()
    return df_to_json(get.pre_market_nifty_info(index_name))

@mcp.tool()
def preopen_market_breadth():
    """Full NSE pre-open advance/decline across all segments."""
    rate_limit()
    return df_to_json(get.pre_market_all_nse_adv_dec_info())

@mcp.tool()
def preopen_stocks_data(
    category: Literal["All", "NIFTY 50", "Nifty Bank", "Emerge", "Securities in F&O"] = "NIFTY 50"
):
    """
    All stocks in pre-open with final price, change %.
    """
    rate_limit()
    return df_to_json(get.pre_market_info(category))


@mcp.tool()
def preopen_futures_data(
    category: Literal["Index Futures", "Stock Futures"] = "Index Futures"
):
    """
    Index Futures or Stock Futures in pre-open with final price, change %.
    """
    rate_limit()
    return df_to_json(get.pre_market_derivatives_info(category))

@mcp.tool()
def list_of_indices():
    """
    All 150+ NSE indices. 
    ("Indices Eligible In Derivatives", "Broad Market Indices", 
    "Sectoral Market Indices", "Thematic Market Indices", 
    "Strategy Market Indices", "Others")
    """
    rate_limit()
    return get.list_of_indices()

@mcp.tool()
def indices_live_data():
    """
    Live values (open, high, low, close(last), variation, percentChange, 
    yearHigh, yearLow, pe, pb, dy, declines, advances, unchanged) 
    of all 150+ NSE indices.
    """
    rate_limit()
    return df_to_json(get.index_live_all_indices_data())

@mcp.tool()
def index_live_constituents(
    index_name: Annotated[str, 'e.g. "NIFTY 50", "SECURITIES IN F&O", "NIFTY BANK"'],
    list_only: Annotated[bool, "Return only symbols if True"] = False
):
    """
    Get stocks in any NSE index with live or current data.
    """
    rate_limit()
    return df_to_json(get.index_live_indices_stocks_data(index_name, list_only=list_only))


# =====================================================================
# LISTS & MASTER DATA
# =====================================================================

@mcp.tool()
def list_of_nifty50_stocks(
    list_only: Annotated[bool, "Only symbols if True"] = False
):
    """
    Latest Nifty 50 stocks with sector & weight.
    """
    rate_limit()

    data = get.nse_6m_nifty_50(list_only=list_only)

    if list_only:
        return {
            "index": "NIFTY 50",
            "count": len(data),
            "symbols": list(data)
        }

    return df_to_json(data)


@mcp.tool()
def list_of_nifty500_stocks(
    list_only: Annotated[bool, "Only symbols if True"] = False
):
    """
    Full Nifty 500 stock list.
    """
    rate_limit()
    
    data = get.nse_6m_nifty_500(list_only=list_only)

    if list_only:
        return {
            "index": "NIFTY 500",
            "count": len(data),
            "symbols": list(data)
        }
    return df_to_json(data)

@mcp.tool()
def list_of_fno_stocks(
    mode: Literal["stocks", "index"] = "stocks", 
    list_only: Annotated[bool, "Only symbols if True"] = False
):
    """
    All F&O eligible stocks or indices.
    """
    rate_limit()
    data = get.nse_eom_fno_full_list(mode=mode, list_only=list_only)

    if list_only:
        return {
            "name": f"F&O {mode.upper()}",
            "count": len(data),
            "symbols": list(data)
        }
    return df_to_json(data)

@mcp.tool()
def list_of_All_NSE_stocks(
    list_only: Annotated[bool, "Only symbols if True"] = False
):
    """
    Complete list of all NSE listed equities.
    """
    rate_limit()
    data = get.nse_eod_equity_full_list(list_only=list_only)

    if list_only:
        return json.dumps(list(data))
    return df_to_json(data)


# =====================================================================
# OPTION CHAIN & F&O LIVE
# =====================================================================

@mcp.tool()
def fno_live_option_chain(
    symbol: Annotated[str, "'RELIANCE', 'NIFTY', 'BANKNIFTY'. Must be uppercase."], 
    expiry: Annotated[str, 'Optional "DD-MMM-YYYY"'] = None, 
    compact: Annotated[bool, "Compact OI view"] = False
):
    """
    Full live option chain with OI, volume, IV, PCR, Max Pain.
    """
    rate_limit()
    mode = "compact" if compact else None
    return df_to_json(get.fno_live_option_chain(symbol, expiry_date=expiry, oi_mode=mode))

@mcp.tool()
def fno_expiry_dates(
    symbol: Annotated[str, "Stock or index. e.g., NIFTY, RELIANCE. Must be uppercase."] = "NIFTY", 
    filter_type: Literal['Current', 'Next Week', 'Month', 'All'] = None
):
    """
    Get All expiry dates or find particularly current, weekly, monthly expiry dates.
    """
    rate_limit()
    return df_to_json(get.fno_expiry_dates(symbol, filter_type))

@mcp.tool()
def fno_expiry_dates_and_strikePrice(
    symbol: Annotated[str, "Stock or index"] = "NIFTY"
):
    """
    Get All expiry dates & strikePrice for given symbol
    """
    rate_limit()
    return df_to_json(get.fno_expiry_dates_raw(symbol))

@mcp.tool()
def most_active_options(
    contract_type: Literal["Stock", "Index"] = "Stock", 
    option_type: Literal['Call', 'Put'] = "Call", 
    sort_by: Literal['Volume', 'Value'] = "Volume"
):
    """
    Most active Call/Put by volume or value.
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active(contract_type, option_type, sort_by))


# =====================================================================
# EQUITY LIVE DATA
# =====================================================================

@mcp.tool()
def most_active_equities(by: Literal["value", "volume"] = "value"):
    """
    Top stocks by traded value or volume.
    """
    rate_limit()
    func = get.cm_live_most_active_equity_by_value if by == "value" else get.cm_live_most_active_equity_by_vol
    return df_to_json(func())

@mcp.tool()
def equity_volume_surge():
    """
    Stocks with sudden volume surge or spurts vs average.
    """
    rate_limit()
    return df_to_json(get.cm_live_volume_spurts())

@mcp.tool()
def equity_52week_high_live():
    """
    Live market stocks hitting 52-week high today.
    """
    rate_limit()
    return df_to_json(get.cm_live_52week_high())

@mcp.tool()
def equity_52week_low_live():
    """
    Live market stocks hitting 52-week low today.
    """
    rate_limit()
    return df_to_json(get.cm_live_52week_low())


# =====================================================================
# CORPORATE ACTIONS & EVENTS
# =====================================================================

@mcp.tool()
def corporate_insider_trading(
    symbol: Annotated[Optional[str], "The NSE stock or index symbol (e.g., RELIANCE). Optional."] = None,
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y"]] = None,
    start_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    end_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Latest insider buying/selling (SAST).
    """
    rate_limit()
    args = compact_args(symbol, period, start_date, end_date)
    return df_to_json(get.cm_live_hist_insider_trading(*args))

@mcp.tool()
def corporate_actions(
    symbol: Annotated[Optional[str], "The NSE stock or index symbol (e.g., RELIANCE). Optional filter."] = None,
    period: Optional[Literal["1M", "3M", "6M", "1Y"]] = None,
    start_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    end_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    purpose: Annotated[Optional[str], "Optional filter"] = None,
):
    """
    Dividends, bonus, splits, rights, buyback.
    """
    rate_limit()
    args = compact_args(symbol, period, start_date, end_date, purpose)
    return df_to_json(get.cm_live_hist_corporate_action(*args))

@mcp.tool()
def corporate_board_meetings(
    symbol: Annotated[str, "Optional filter. Must be uppercase."] = None, 
    start_date: Annotated[str, "DD-MM-YYYY"] = None, 
    end_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Upcoming & past board meetings.
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_board_meetings(symbol, start_date, end_date))


# =====================================================================
# IPO & LISTINGS
# =====================================================================

@mcp.tool()
def ipo_current_list():
    """
    All open Mainboard & SME IPOs with subscription status.
    """
    rate_limit()
    return df_to_json(get.ipo_current())

@mcp.tool()
def ipo_preopen_today():
    """
    Newly listed IPOs in special pre-open session.
    """
    rate_limit()
    return df_to_json(get.ipo_preopen())

@mcp.tool()
def ipo_performance_tracker(
    board: Literal["Mainboard", "SME"] | None = "Mainboard"
):
    """
    YTD IPO listing performance & gains.
    """
    rate_limit()
    return df_to_json(get.ipo_tracker_summary(board))


# =====================================================================
# HISTORICAL & EOD DATA
# =====================================================================

@mcp.tool()
def index_price_history(
    index: Annotated[str, 'Name of the index (e.g., "NIFTY 50", "NIFTY BANK")'],
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "YTD", "MAX"]] = None,
    from_date: Annotated[Optional[str], "Start date DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "End date DD-MM-YYYY"] = None,
):
    """
    Fetch historical OHLC + turnover for any index.
    """
    rate_limit()
    kwargs = compact_kwargs(index=index, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.index_historical_data(**kwargs))


@mcp.tool()
def equity_price_history(
    symbol: Annotated[str, 'Name of the stock (e.g., "TCS", "ITC"). Must be uppercase.'],
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "YTD", "MAX"]] = None,
    from_date: Annotated[Optional[str], "Start date DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "End date DD-MM-YYYY"] = None,
):
    """
    Fetch historical price OHLC + turnover + delivery data for any stock.
    """
    rate_limit()
    kwargs = compact_kwargs(symbol=symbol, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.cm_hist_security_wise_data(**kwargs))


# =====================================================================
#                          NSE Data - Historical
# =====================================================================

@mcp.tool()
def nse_circulars(
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None, 
    department: Annotated[str, 'Optional filter, e.g., "NSE Listing"'] = None
):
    """
    Historical NSE circulars (default: yesterday → today)
    """
    rate_limit()
    return df_to_json(get.nse_live_hist_circulars(from_date, to_date, department))


@mcp.tool()
def nse_press_releases(
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None, 
    department: Annotated[str, 'e.g. Corporate Communications, Investor Services Cell, Member Compliance, NSE Clearing, etc.'] = None
):
    """
    Historical NSE press releases
    """
    rate_limit()
    return df_to_json(get.nse_live_hist_press_releases(from_date, to_date, department))


# =====================================================================
#                          Index Live Data
# =====================================================================

@mcp.tool()
def nifty50_past_returns():
    """
    Nifty 50 returns summary (1W to 5Y)
    """
    rate_limit()
    return df_to_json(get.index_live_nifty_50_returns())


@mcp.tool()
def index_live_contribution(
    Index: Annotated[str, 'e.g., "NIFTY 50", "NIFTY BANK"'] = None, 
    Mode: Literal['First Five', 'Full'] = None
):
    """
    Stock-wise how many points(changePoints) contribution to NIFTY 50 or Given index movement
    """
    rate_limit()
    return df_to_json(get.index_live_contribution(Index, Mode))


# =====================================================================
#                          Index EOD & Historical
# =====================================================================

@mcp.tool()
def index_eod_bhavcopy(date: Annotated[str, "DD-MM-YYYY"]):
    """
    All indices EOD bhavcopy for a specific date (uses last trading date if none given)
    """
    rate_limit()
    return df_to_json(get.index_eod_bhav_copy(date))


@mcp.tool()
def index_pe_pb_div_historical_data(
    index: Annotated[str, 'e.g., "NIFTY 50", "NIFTY BANK"'],
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "YTD", "MAX"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Historical P/E, P/B, Dividend Yield for any index
    """
    rate_limit()
    kwargs = compact_kwargs(index=index, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.index_pe_pb_div_historical_data(**kwargs))


@mcp.tool()
def india_vix(
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "5Y", "10Y", "YTD", "MAX"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Historical India VIX data
    """
    rate_limit()
    kwargs = compact_kwargs(period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.india_vix_historical_data(**kwargs))


# =====================================================================
#                       Capital Market Live Data
# =====================================================================

@mcp.tool()
def equity_live_stock_info(
    symbol: Annotated[str, "The NSE stock or index symbol (e.g., RELIANCE). Must be uppercase."]
):
    """
    Full live quote: Meta Data, Trade Information, Price Information, 
    Securities Information, Order Book, etc.
    """
    rate_limit()
    return get.cm_live_equity_info(symbol)


@mcp.tool()
def equity_block_deals_live():
    """
    Latest block deals (live)
    """
    rate_limit()
    return df_to_json(get.cm_live_block_deal())


@mcp.tool()
def corporate_announcement(
    symbol: Annotated[str, "Optional filter. Must be uppercase."] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Corporate announcements (all or symbol-specific)
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_corporate_announcement(symbol, from_date, to_date))


@mcp.tool()
def corporate_today_event_calendar(
    date_from: Annotated[str, "DD-MM-YYYY"] = None, 
    date_to: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Today's or date-range corporate events (AGM, results etc.)
    """
    rate_limit()
    return df_to_json(get.cm_live_today_event_calendar(date_from, date_to))


@mcp.tool()
def corporate_upcoming_event_calendar():
    """
    Upcoming corporate events
    """
    rate_limit()
    return df_to_json(get.cm_live_upcoming_event_calendar())


@mcp.tool()
def corporate_shareholder_meetings(
    symbol: Annotated[str, "Optional filter. Must be uppercase."] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Shareholder meetings (AGM/EGM) history
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_Shareholder_meetings(symbol, from_date, to_date))


@mcp.tool()
def equity_QIP_history(
    stage: Literal["In-Principle", "Listing Stage"] = None, 
    period_or_symbol: Annotated[str, '"1Y", "RELIANCE" etc.'] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Qualified Institutional Placement (QIP) data by stage, period, symbol
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_qualified_institutional_placement(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def equity_preferential_issues(
    stage: Literal["In-Principle", "Listing Stage"] = None, 
    period_or_symbol: Annotated[str, '"1Y", "RELIANCE" etc.'] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Preferential issue data
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_preferential_issue(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def equity_rights_issues(
    stage: Literal["In-Principle", "Listing Stage"] = None, 
    period_or_symbol: Annotated[str, '"1Y", "RELIANCE" etc.'] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Rights issue data
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_right_issue(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def corporate_voting_results():
    """
    Latest voting results
    """
    rate_limit()
    return df_to_json(get.cm_live_voting_results())


@mcp.tool()
def corporate_qtly_shareholding_patterns():
    """
    Latest quarterly shareholding patterns
    """
    rate_limit()
    return df_to_json(get.cm_live_qtly_shareholding_patterns())

@mcp.tool()
def corporate_annual_reports():
    """
    Latest 20 Annual reports with pdf links
    """
    rate_limit()
    return df_to_json(get.recent_annual_reports())

@mcp.tool()
def corporate_bsr_reports(
    symbol: Annotated[str, "Optional filter. Must be uppercase."] = None, 
    from_date: Annotated[str, "DD-MM-YYYY"] = None, 
    to_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Business Responsibility and Sustainability Reports (all or symbol-specific)
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_br_sr(symbol, from_date, to_date))

# =====================================================================
#                          FnO Live Data
# =====================================================================

@mcp.tool()
def fno_live_futures_data(
    symbol: Annotated[str, "The NSE stock or index symbol (e.g., RELIANCE, NIFTY). Must be uppercase."]
):
    """
    Live futures data for stock or index
    """
    rate_limit()
    return df_to_json(get.fno_live_futures_data(symbol))

@mcp.tool()
def fno_live_top_20_stocks_contracts(
    category: Literal["Stock Futures", "Stock Options"]
):
    """
    Live Top 20 Stocks Futures or Stocks Options data
    """
    rate_limit()
    return df_to_json(get.fno_live_top_20_derivatives_contracts(category))


@mcp.tool()
def fno_live_most_active_futures_contracts(
    by: Literal["Volume", "Value"] = "Volume"
):
    """
    Most active futures by Volume or Value
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_futures_contracts(by))


@mcp.tool()
def fno_live_most_active_contracts_by_oi():
    """
    Most active contracts by Open Interest
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_contracts_by_oi())


@mcp.tool()
def fno_live_most_active_contracts_by_volume():
    """
    Most active by volume
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_contracts_by_volume())


@mcp.tool()
def fno_live_most_active_options_contracts_by_volume():
    """
    Top options contracts by volume
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_options_contracts_by_volume())


@mcp.tool()
def fno_live_most_active_underlying():
    """
    Most active underlying stocks/indices
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_underlying())


@mcp.tool()
def fno_live_change_in_oi():
    """
    Change in Open Interest across contracts
    """
    rate_limit()
    return df_to_json(get.fno_live_change_in_oi())

@mcp.tool()
def fno_live_oi_vs_price():
    """
    Open Interest Vs Price across contracts
    """
    rate_limit()
    return df_to_json(get.fno_live_oi_vs_price())

@mcp.tool()
def fno_live_active_contracts(
    symbol: Annotated[str, "e.g., NIFTY, BANKNIFTY, RELIANCE. Must be uppercase."] = "NIFTY", 
    expiry_date: Annotated[str, "DD-MM-YYYY"] = None
):
    """
    Active NIFTY/BANKNIFTY & stock option contracts
    """
    rate_limit()
    return df_to_json(get.fno_live_active_contracts(symbol, expiry_date=expiry_date))


# =====================================================================
#                         EQUITY EOD DATA
# =====================================================================

@mcp.tool()
def fii_dii_activity(
    exchange: Annotated[str, "None for All exchange (NSE+BSE). 'Nse' for NSE only."] = None
):
    """
    Latest FII/DII net buying/selling activity.
    """
    rate_limit()
    return df_to_json(get.cm_eod_fii_dii_activity(exchange))


@mcp.tool()
def market_eod_activity_report(
    date: Annotated[str, "Trade date in DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Daily market turnover, advances/declines, top gainers/losers.
    """
    rate_limit()
    return df_to_json(get.cm_eod_market_activity_report(date))

@mcp.tool()
def equity_eod_bhavcopy_delivery(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Full NSE equity bhavcopy including delivery percentage & value.
    """
    rate_limit()
    return df_to_json(get.cm_eod_bhavcopy_with_delivery(date))


@mcp.tool()
def equity_eod_bhavcopy(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Standard equity closing prices, volume, trades (without delivery).
    """
    rate_limit()
    return df_to_json(get.cm_eod_equity_bhavcopy(date))


@mcp.tool()
def equity_52week_high_low_eod(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Stocks hitting 52-week high or low on given date.
    """
    rate_limit()
    return df_to_json(get.cm_eod_52_week_high_low(date))


@mcp.tool()
def equity_bulk_deals_eod():
    """
    End of day based bulk deals across NSE/BSE (client-level).
    """
    rate_limit()
    return df_to_json(get.cm_eod_bulk_deal())


@mcp.tool()
def equity_block_deals_eod():
    """
    End of day based block deals (large negotiated trades).
    """
    rate_limit()
    return df_to_json(get.cm_eod_block_deal())


@mcp.tool()
def equity_short_selling(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Stocks disclosed for short selling.
    """
    rate_limit()
    return df_to_json(get.cm_eod_shortselling(date))


@mcp.tool()
def surveillance_indicator(
    date: Annotated[str, "DD-MM-YY (2-digit year). Uses last trading date if None given."]
):
    """
    Stocks under ASM/GSM/Z-category surveillance.
    """
    rate_limit()
    return df_to_json(get.cm_eod_surveillance_indicator(date))


@mcp.tool()
def equity_series_changes():
    """
    Recent changes in trading series (EQ → BE, BE → BZ etc.).
    """
    rate_limit()
    return df_to_json(get.cm_eod_series_change())


@mcp.tool()
def equity_price_band_changes(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Stocks moved to/from price bands (2%, 5%, 10%, 20%).
    """
    rate_limit()
    return df_to_json(get.cm_eod_eq_band_changes(date))


@mcp.tool()
def equity_price_bands(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Applicable price bands for all stocks on a given EOD.
    """
    rate_limit()
    return df_to_json(get.cm_eod_eq_price_band(date))


@mcp.tool()
def equity_price_band_history(
    symbol: Annotated[Optional[str], "Optional filter. Must be uppercase."] = None,
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Historical price band changes for a stock or all stocks.
    """
    rate_limit()
    kwargs = compact_kwargs(symbol=symbol, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.cm_hist_eq_price_band(**kwargs))


@mcp.tool()
def equity_pe_ratio(
    date: Annotated[str, "DD-MM-YY. Uses last trading date if None given."]
):
    """
    PE, PB, Dividend Yield for all listed companies.
    """
    rate_limit()
    return df_to_json(get.cm_eod_pe_ratio(date))


@mcp.tool()
def market_cap(
    date: Annotated[str, "DD-MM-YY. Uses last trading date if None given."]
):
    """
    "Market capitalization" (Market Cap(Rs.)), "Total No of Shares Issued" 
    (Issue Size) of all companies.
    """
    rate_limit()
    return df_to_json(get.cm_eod_mcap(date))


@mcp.tool()
def equity_name_changes():
    """
    Recent corporate name changes.
    """
    rate_limit()
    return df_to_json(get.cm_eod_eq_name_change())


@mcp.tool()
def equity_symbol_changes():
    """
    Recent symbol changes (e.g., INFY → INFY).
    """
    rate_limit()
    return df_to_json(get.cm_eod_eq_symbol_change())


@mcp.tool()
def equity_bulk_deals_history(
    symbol: Annotated[Optional[str], "Optional filter. Must be uppercase."] = None,
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Bulk deals history – by symbol, date range or period.
    """
    rate_limit()
    kwargs = compact_kwargs(symbol=symbol, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.cm_hist_bulk_deals(**kwargs))


@mcp.tool()
def equity_block_deals_history(
    symbol: Annotated[Optional[str], "Optional filter. Must be uppercase."] = None,
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Block deals history – by symbol or date range.
    """
    rate_limit()
    kwargs = compact_kwargs(symbol=symbol, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.cm_hist_block_deals(**kwargs))


@mcp.tool()
def equity_short_selling_history(
    symbol: Annotated[Optional[str], "Optional filter. Must be uppercase."] = None,
    period: Optional[Literal["1D", "1W", "1M", "3M", "6M", "1Y"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
):
    """
    Historical short selling disclosures.
    """
    rate_limit()
    kwargs = compact_kwargs(symbol=symbol, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.cm_hist_short_selling(**kwargs))


@mcp.tool()
def equity_market_business_growth(
    mode: Literal["daily", "monthly", "yearly"] = "daily",
    month: Optional[Literal["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]] = None,
    year: Annotated[Optional[int], "FY year, e.g. 2025"] = None,
):
    """
    NSE daily/monthly/yearly business growth (cash segment).
    """
    rate_limit()
    args = compact_args(mode, month, year)
    return df_to_json(get.cm_dmy_biz_growth(*args))


@mcp.tool()
def equity_market_monthly_settlement(
    period: Optional[Literal["1Y","2M", "3Y"]] = None,
    from_year: Annotated[Optional[int], "e.g., 2024"] = None,
    to_year: Annotated[Optional[int], "e.g., 2026"] = None,
):
    """
    Fetch NSE Monthly Settlement Statistics (Cash Market) for multiple financial years (Apr–Mar)
    """
    rate_limit()
    kwargs = compact_kwargs(period=period, from_year=from_year, to_year=to_year)
    return df_to_json(get.cm_monthly_settlement_report(**kwargs))


@mcp.tool()
def monthly_most_active_equity():
    """
    Most active stocks by volume/value in latest month.
    """
    rate_limit()
    return df_to_json(get.cm_monthly_most_active_equity())


@mcp.tool()
def market_advances_declines(
    mode: Literal["Day_wise", "Month_wise"] = "Month_wise",
    month: Optional[Literal["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]] = None,
    year: Annotated[Optional[int], "e.g., 2025"] = None,
):
    """
    Historical advances vs declines (daily or monthly).
    """
    rate_limit()
    args = compact_args(mode, month, year)
    return df_to_json(get.historical_advances_decline(*args))


# =====================================================================
#                         F&O EOD & HISTORICAL DATA
# =====================================================================

@mcp.tool()
def fno_bhavcopy(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Full F&O bhavcopy (futures + options).
    """
    rate_limit()
    return df_to_json(get.fno_eod_bhav_copy(date))


@mcp.tool()
def fno_fii_stats(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    FII activity in F&O segment (Index/Stock, Long/Short).
    """
    rate_limit()
    return df_to_json(get.fno_eod_fii_stats(date))


@mcp.tool()
def fno_eod_top10_futures(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Top 10 most active futures contracts by volume/OI.
    """
    rate_limit()
    return df_to_json(get.fno_eod_top10_fut(date))


@mcp.tool()
def fno_eod_top20_options(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Top 20 most active options contracts.
    """
    rate_limit()
    return df_to_json(get.fno_eod_top20_opt(date))


@mcp.tool()
def fno_ban_list(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."] = None
):
    """
    Stocks under F&O ban period.
    """
    rate_limit()
    return df_to_json(get.fno_eod_sec_ban(date))


# @mcp.tool()
# def fno_mwpl_data(
#     date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
# ):
#     """
#     Market Wide Position Limits (MWPL) and usage %.
#     """
#     rate_limit()
#     return df_to_json(get.fno_eod_mwpl_3(date))


@mcp.tool()
def fno_mwpl_data(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """Market Wide Position Limits (MWPL) and usage %."""
    rate_limit()
    df = (get.fno_eod_mwpl_3, date)

    df = df.dropna(axis=1, how="all")

    records = []
    for row in df.to_dict(orient="records"):
        meta = {
            k: v for k, v in row.items()
            if not k.startswith("Client") and k != "Sr No."  # ← exclude Sr No.
        }
        clients = {
            k: v for k, v in row.items()
            if k.startswith("Client") and pd.notna(v)
        }
        sorted_vals = sorted(clients.values(), reverse=True)
        sorted_clients = {f"Client {i+1}": v for i, v in enumerate(sorted_vals)}

        records.append({**meta, **sorted_clients})

    return json.dumps(records, ensure_ascii=False)


@mcp.tool()
def fno_combined_oi(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    Combined futures & options open interest.
    """
    rate_limit()
    return df_to_json(get.fno_eod_combine_oi(date))


@mcp.tool()
def fno_participant_wise_oi(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    FII, DII, Pro, Client wise open interest.
    """
    rate_limit()
    return df_to_json(get.fno_eod_participant_wise_oi(date))


@mcp.tool()
def fno_participant_wise_volume(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."]
):
    """
    FII, DII, Pro, Client wise trading volume in F&O.
    """
    rate_limit()
    return df_to_json(get.fno_eod_participant_wise_vol(date))


@mcp.tool()
def futures_price_history(
    symbol: Annotated[str, "Symbol e.g., RELIANCE, NIFTY. Must be uppercase."],
    instrument: Literal["Index Futures", "Stock Futures"],
    expiry: Annotated[Optional[str], "DD-MMM-YYYY format (e.g. 28-OCT-2025)"] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    period: Optional[Literal["1M", "3M", "1Y"]] = None,
):
    """
    Historical futures price, volume, OI.
    """
    rate_limit()
    kwargs = compact_kwargs(expiry=expiry, period=period, from_date=from_date, to_date=to_date)
    return df_to_json(get.future_price_volume_data(symbol, instrument, **kwargs))


@mcp.tool()
def options_price_history(
    symbol: Annotated[str, "Symbol e.g., RELIANCE, NIFTY. Must be uppercase."],
    instrument: Literal["Index Options", "Stock Options"],
    strike: Annotated[Optional[int], "e.g. 47000"] = None,
    option_type: Optional[Literal["CE", "PE"]] = None,
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    expiry: Annotated[Optional[str], "DD-MMM-YYYY"] = None,
    period: Optional[Literal["3M", "1Y"]] = None,
):
    """
    Historical options price, volume, OI, IV.
    """
    rate_limit()
    kwargs = compact_kwargs(strike=strike, option_type=option_type, period=period, from_date=from_date, to_date=to_date, expiry=expiry)
    return df_to_json(get.option_price_volume_data(symbol, instrument, **kwargs))


@mcp.tool()
def fno_lot_sizes(
    symbol: Annotated[str, "Optional filter. Must be uppercase."] = None
):
    """
    Current F&O lot sizes (all or specific symbol).
    """
    rate_limit()
    return df_to_json(get.fno_eom_lot_size(symbol))


@mcp.tool()
def fno_business_growth(
    mode: Literal["daily", "monthly", "yearly"] = "daily",
    month: Optional[Literal["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]] = None,
    year: Annotated[Optional[int], "FY year, e.g. 2025"] = None,
):
    """
    F&O segment daily/monthly/yearly turnover growth.
    """
    rate_limit()
    args = compact_args(mode, month, year)
    return df_to_json(get.fno_dmy_biz_growth(*args))


@mcp.tool()
def fno_settlement_report(
    period: Optional[Literal["1Y","2Y" "3Y"]] = None,
    from_year: Annotated[Optional[int], "e.g., 2024"] = None,
    to_year: Annotated[Optional[int], "e.g., 2026"] = None,
):
    """
    NSE Monthly Settlement Statistics (F&O) for given financial years or period.
    """
    rate_limit()
    kwargs = compact_kwargs(period=period, from_year=from_year, to_year=to_year)
    return df_to_json(get.fno_monthly_settlement_report(**kwargs))


@mcp.tool()
def fno_top_10_clearing_members(
    date: Annotated[str, "DD-MM-YYYY. Uses last trading date if None given."] = None
):
    """Volume and Turnover data of top 10 Clearing Members (no. of contracts) in Equity Derivatives."""
    rate_limit()
    return df_to_json(get.fno_eod_top_10_clearing_members(date))

@mcp.tool()
def fno_client_category_wise_turnover(
    date: Annotated[str, "Date in DD-MM-YYYY format. Uses last trading date if None is given."],
    raw_data: Annotated[bool, "Return raw NSE response if True."] = False,
):
    """Client Category Wise Turnover(Mutual Funds, AIF, PMS, FPI, Retail, Insurance Companies, Others)."""
    rate_limit()
    return df_to_json(get.fno_eod_client_wise_turnover (date, raw_data=raw_data))


# =====================================================================
#                         SEBI DATA
# =====================================================================

@mcp.tool()
def sebi_circulars(
    from_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    to_date: Annotated[Optional[str], "DD-MM-YYYY"] = None,
    period: Optional[Literal["1W", "1M", "3M", "1Y"]] = None,
):
    """
    Latest or historical SEBI circulars.
    """
    rate_limit()
    args = compact_args(from_date, to_date, period)
    return df_to_json(get.sebi_circulars(*args))


@mcp.tool()
def sebi_data_pages(page: Annotated[int, "Page number"] = 1):
    """
    Paginated SEBI circulars and orders.
    """
    rate_limit()
    return df_to_json(get.sebi_data(page))


@mcp.tool()
def price_chart_index(
    index: Annotated[str, "e.g., NIFTY 50, SECURITIES IN F&O"] = "NIFTY 50", 
    timeframe: Literal["1D", "1M", "3M", "6M", "1Y"] = "1D"
):
    """
    Retrieves intraday or historical price chart data for the NIFTY Indices
    """
    rate_limit()
    return df_to_json(get.index_chart(index, timeframe))


@mcp.tool()
def price_chart_stock(
    symbol: Annotated[str, "Symbol e.g., RELIANCE. Must be uppercase."], 
    timeframe: Literal["1D", "1W", "1M", "1Y"] = "1D"
):
    """
    Retrieves intraday or historical price chart data for the stock
    """
    rate_limit()
    return df_to_json(get.stock_chart(symbol, timeframe))


@mcp.tool()
def fno_intraday_chart(
    symbol: Annotated[str, "Symbol e.g., RELIANCE, NIFTY. Must be uppercase."],
    inst_type: Literal["FUTSTK", "OPTSTK", "FUTIDX", "OPTIDX"],
    expiry: Annotated[str, "DD-MM-YYYY format"],
    strike: Annotated[Optional[str], "CE/PE + price (options need CE/PE)"] = None,
):
    """
    Retrieves intraday chart data for the futures/options contracts (Stock + Index).
    """
    rate_limit()
    args = compact_args(symbol, inst_type, expiry, strike)
    return df_to_json(get.fno_chart(*args))


@mcp.tool()
def price_chart_india_vix():
    """
    Retrieves intraday chart data for the India VIX Index.
    """
    rate_limit()
    return df_to_json(get.india_vix_chart())


@mcp.tool()
def symbol_full_fno_live_data(
    symbol: Annotated[str, "e.g., NIFTY, BANKNIFTY, RELIANCE, TCS. Must be uppercase."]
):
    """
    Fetches complete live FnO data for the specified stock or index.
    """
    rate_limit()
    return get.symbol_full_fno_live_data(symbol)


@mcp.tool()
def symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI(
    symbol: Annotated[str, "Symbol e.g., NIFTY, RELIANCE. Must be uppercase."], 
    type_mode: Literal["CALLS", "PUTS", "CONTRACTS"]
):
    """
    Fetches the Top 5 Most Active CALLS, PUTS, or CONTRACTS based on Open Interest
    """
    rate_limit()
    return get.symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI(symbol, type_mode)


@mcp.tool()
def price_chart_fno_contracts(
    identifier: Annotated[str, 'Examples: "OPTSTKTCS30-12-2025CE3300.00"']
):
    """
    Fetches intraday price chart data (timestamp, price, flag)
    """
    rate_limit()
    return get.identifier_based_fno_contracts_live_chart_data(identifier)


@mcp.tool()
def investors_statewise():
    """
    Fetches NSE Registered Investors by State.
    """
    rate_limit()
    return get.state_wise_registered_investors()


@mcp.tool()
def quarterly_financial_results(
    symbol: Annotated[str, "The NSE stock symbol (e.g., TCS). Must be uppercase."]
):
    """
    Quarterly Results (Amount in Lakhs).
    """
    rate_limit()
    return get.quarterly_financial_results(symbol)


@mcp.tool()
def quarterly_financial_results_full_data(
    url: Annotated[str, "NSE HTML URL"]
):
    """
    Quarterly Results from URL.
    """
    rate_limit()
    return get.html_tables(url)



@mcp.tool()
def equity_peer_comparison(
    symbol: Annotated[str, "NSE equity symbol, e.g. 'TCS', 'RELIANCE'. Must be uppercase."],
    quarter: Annotated[str, 'Quarter end-month. e.g. "Mar 2026", "Dec 2025", or "2025-09".'],
    report_type: Annotated[
        Literal["Consolidated", "Standalone"],
        '"Consolidated" (default) or "Standalone".'
    ] = "Consolidated",
):
    """
    Fetch peer-comparison data for a stock from the NSE.
    Returns one row per peer company with columns: Symbol, LTP (₹), % Chng,
    Volume (Lakhs), Value (₹ Cr.), Mkt Cap (₹ Cr.), P/E, Total Income (₹ Cr.),
    Net Profit (₹ Cr.), EPS (₹), Debt/Equity, Promoter %.
    Common quarter-end months: Mar, Jun, Sep, Dec.
    """
    rate_limit()
    return df_to_json(get.peer_comparison, symbol, quarter, report_type)




#-------------------------   Prompt   ----------------------------------

@mcp.prompt()
def pre_market_analysis() -> str:
    """
    Generate NSE pre-market analysis prompt
    """
    return (
        "Generate an NSE PRE-MARKET ANALYSIS.\n\n"
        "Steps:\n"
        "1. Check whether today is a trading holiday.\n"
        "2. Analyze Gift Nifty trend and global cues.\n"
        "3. Review pre-open advance and decline data.\n"
        "4. Identify major gap-up and gap-down stocks.\n"
        "5. Summarize NIFTY 50 and BANKNIFTY directional bias.\n\n"
        "Output Format:\n"
        "- Market Status\n"
        "- Gift Nifty / Global Cues\n"
        "- Market Breadth\n"
        "- Key Movers\n"
        "- Intraday Bias\n"
        "- Risk Notes\n\n"
        "Rules:\n"
        "- Use only NseKit-MCP tools\n"
        "- Do not assume prices or direction"
    )


@mcp.prompt()
def market_overview() -> str:
    """
    Get comprehensive market overview
    """
    return (
        "Provide a comprehensive NSE market overview:\n\n"
        "1. Current market status and time\n"
        "2. Nifty 50 and Bank Nifty levels\n"
        "3. Market statistics (advances, declines, 52W highs/lows)\n"
        "4. Top gainers and losers\n"
        "5. Most active stocks by value\n"
        "6. FII/DII activity\n"
        "7. India VIX level\n\n"
        "Present in a clean, organized format."
    )


@mcp.prompt()
def analyze_option_chain() -> str:
    """
    Analyze option chain for given symbol
    """
    return (
        "Analyze the option chain for a given stock/index:\n\n"
        "Steps:\n"
        "1. Get the current expiry dates\n"
        "2. Fetch the option chain for current expiry\n"
        "3. Calculate Put-Call Ratio (PCR)\n"
        "4. Identify max pain level\n"
        "5. Find highest OI strikes for calls and puts\n"
        "6. Analyze OI changes\n"
        "7. Provide directional bias\n\n"
        "Symbol will be provided by user (e.g., NIFTY, RELIANCE)\n"
        "Present in a clean, organized format."
    )


@mcp.prompt()
def stock_deep_dive() -> str:
    """
    Perform deep analysis of a stock
    """
    return (
        "Perform comprehensive stock analysis:\n\n"
        "1. Live Quote (price, volume, circuit limits)\n"
        "2. Historical performance (1W, 1M, 3M, 1Y)\n"
        "3. Delivery percentage analysis\n"
        "4. Bulk/Block deals (if any)\n"
        "5. F&O data (if applicable)\n"
        "6. Corporate actions/announcements\n"
        "7. Insider trading activity\n"
        "8. Valuation metrics (PE, PB, Div Yield)\n\n"
        "Stock symbol will be provided by user.\n"
        "Present in a clean, organized format."
    )


@mcp.prompt()
def fno_expiry_analysis() -> str:
    """
    Analyze F&O positions before expiry
    """
    return (
        "Generate F&O EXPIRY DAY analysis:\n\n"
        "1. Check if today is an expiry day\n"
        "2. Get most active options by OI and volume\n"
        "3. Analyze max pain levels for Nifty and BankNifty\n"
        "4. Review F&O ban stocks\n"
        "5. Check participant-wise OI (FII/DII positioning)\n"
        "6. Identify key support and resistance from OI\n"
        "7. Provide expiry day strategy notes\n\n"
        "Focus on: NIFTY, BANKNIFTY, and top F&O stocks\n"
        "Present in a clean, organized format."
    )


@mcp.prompt()
def market_sentiment() -> str:
    """
    Gauge overall market sentiment
    """
    return (
        "Analyze current market sentiment:\n\n"
        "Data to collect:\n"
        "1. Advance/Decline ratio\n"
        "2. India VIX trend\n"
        "3. FII/DII net positions\n"
        "4. Put-Call Ratio for indices\n"
        "5. Stocks hitting circuits\n"
        "6. Volume analysis\n"
        "7. Sector performance\n\n"
        "Provide sentiment as: Bullish/Bearish/Neutral\n"
        "Include confidence level and key factors.\n"
        "Present in a clean, organized format."
    )


@mcp.prompt()
def daily_market_wrap() -> str:
    """
    Generate end-of-day market summary
    """
    return (
        "Generate DAILY MARKET WRAP for NSE:\n\n"
        "1. Closing levels of major indices\n"
        "2. Day's high/low ranges\n"
        "3. Top performers and losers\n"
        "4. Sectoral performance\n"
        "5. Bulk and block deals\n"
        "6. FII/DII net trading\n"
        "7. Notable corporate actions\n"
        "8. F&O highlights (OI changes, rollovers)\n\n"
        "Use today's date for EOD data.\n"
        "Format as a professional market report."
    )


@mcp.prompt()
def intraday_scanner_fno_only() -> str:
    """
    Primary MCP scanner to identify high-probability NSE intraday trade setups
    STRICTLY within F&O stocks using liquidity, volume, institutional activity,
    price structure, derivatives confirmation, and risk control.
    """
    return (
        "You are a professional Indian stock market analyst running an intraday trading desk. "
        "Your task is to identify high-probability intraday trade setups using ONLY F&O stocks "
        "and ONLY NseKit-MCP tools, without assumptions or discretionary bias.\n\n"

        "=============================\n"
        "UNIVERSE DEFINITION (MANDATORY)\n"
        "=============================\n"
        "Use:\n"
        "- index_live_constituents(\"SECURITIES IN F&O\")\n\n"
        "Rule:\n"
        "- From start to end, ALL analysis must be restricted to F&O stocks only.\n"
        "- Non-F&O stocks must be ignored completely.\n\n"

        "=============================\n"
        "PROMPT 1: MARKET REGIME & RISK FILTER\n"
        "=============================\n"
        "Use:\n"
        "- market_live_status\n"
        "- india_vix\n"
        "- gift_nifty_live\n"
        "- market_advances_declines\n\n"
        "Objective:\n"
        "Determine the intraday market regime:\n"
        "1) Trending\n"
        "2) Range-bound\n"
        "3) High-volatility risk-off\n\n"
        "Output:\n"
        "- Market Bias (Bullish / Bearish / Neutral)\n"
        "- Volatility Condition (Low / Normal / High)\n"
        "- Allowed Trading Style (Scalp / Momentum / Avoid)\n\n"
        "Risk Rules:\n"
        "- Rising VIX with skewed advances/declines → reduce position size\n"
        "- Flat GIFT NIFTY with low VIX → prefer range-bound strategies\n\n"

        "=============================\n"
        "PROMPT 2: F&O LIQUIDITY & VOLUME FILTER (PRIMARY)\n"
        "=============================\n"
        "Use:\n"
        "- most_active_equities\n"
        "- equity_volume_surge\n"
        "- market_live_turnover\n\n"
        "Objective:\n"
        "From the F&O universe, identify intraday candidates where:\n"
        "- Stocks appear in most active equities\n"
        "- Volume surge is significantly higher than recent averages\n"
        "- Turnover concentration supports intraday execution\n\n"
        "Output:\n"
        "- Ranked list of F&O stocks based on:\n"
        "  1) Volume Surge\n"
        "  2) Turnover\n"
        "  3) Liquidity Quality\n\n"

        "Fallback Rule:\n"
        "- If no suitable F&O stocks are found using volume and activity filters:\n"
        "  → Select best candidates directly from index_live_constituents(\"SECURITIES IN F&O\")\n"
        "  → Prioritize index heavyweights and consistently liquid names\n\n"

        "=============================\n"
        "PROMPT 3: INSTITUTIONAL FOOTPRINT (CASH MARKET)\n"
        "=============================\n"
        "Use:\n"
        "- equity_block_deals_live\n"
        "- equity_bulk_deals_live\n"
        "- fii_dii_activity\n\n"
        "Objective:\n"
        "Detect institutional participation in selected F&O stocks:\n"
        "- Same-day block or bulk deals\n"
        "- Alignment with overall FII directional activity\n\n"
        "Output:\n"
        "- Institutional Tag:\n"
        "  • Accumulation\n"
        "  • Distribution\n"
        "  • Noise\n\n"
        "Rule:\n"
        "- Avoid retail-only volume spikes without institutional confirmation\n\n"

        "=============================\n"
        "PROMPT 4: PRICE STRUCTURE & INTRADAY LEVELS\n"
        "=============================\n"
        "Use:\n"
        "- equity_live_stock_quote\n"
        "- price_chart_stock\n"
        "- equity_52week_high_live\n"
        "- equity_52week_low_live\n\n"
        "Objective:\n"
        "Evaluate intraday price structure for F&O stocks:\n"
        "- Opening range breakout or breakdown\n"
        "- VWAP hold or rejection\n"
        "- Strength or weakness near day high / day low\n\n"
        "Output:\n"
        "- Trend Bias (Up / Down / Range)\n"
        "- Key Levels (VWAP, Day High, Day Low)\n\n"

        "=============================\n"
        "PROMPT 5: FUTURES STRENGTH CONFIRMATION\n"
        "=============================\n"
        "Use:\n"
        "- fno_live_futures_data\n"
        "- fno_live_change_in_oi\n"
        "- fno_participant_wise_oi\n\n"
        "Objective:\n"
        "Confirm futures market participation:\n"
        "- Price ↑ + OI ↑ → Long buildup\n"
        "- Price ↓ + OI ↑ → Short buildup\n\n"
        "Output:\n"
        "- Directional Conviction Score (0–10)\n\n"

        "=============================\n"
        "PROMPT 6: OPTION CHAIN BIAS (ATM FOCUS)\n"
        "=============================\n"
        "Use:\n"
        "- fno_live_option_chain\n"
        "- fno_live_most_active_contracts_by_oi\n"
        "- symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI\n\n"
        "Objective:\n"
        "Assess options market behavior:\n"
        "- ATM Put writing → Bullish bias\n"
        "- ATM Call writing → Bearish bias\n"
        "- Detect long gamma traps via price–OI divergence\n\n"
        "Output:\n"
        "- Option Bias (Bullish / Bearish / Neutral)\n"
        "- Trap Warning (if applicable)\n\n"

        "=============================\n"
        "PROMPT 7: HIGH PROBABILITY TRADE QUALIFIER\n"
        "=============================\n"
        "Input:\n"
        "- Consolidated outputs from Prompts 1–6\n\n"
        "Qualification Conditions:\n"
        "- F&O stock only\n"
        "- Volume expansion confirmed\n"
        "- Institutional alignment present\n"
        "- Price holding above/below VWAP\n"
        "- Futures / options confirmation\n"
        "- Market regime alignment\n\n"
        "Output:\n"
        "- Trade Decision (TRADE / NO TRADE)\n"
        "- Direction (Long / Short)\n"
        "- Confidence Score (%)\n\n"

        "=============================\n"
        "PROMPT 8: EXECUTION & RISK MANAGEMENT\n"
        "=============================\n"
        "Use:\n"
        "- equity_live_stock_quote\n\n"
        "Objective:\n"
        "Create a disciplined intraday execution plan:\n"
        "- Entry trigger based on confirmation\n"
        "- Technical stop-loss\n"
        "- Target with minimum Risk:Reward ≥ 1:1.5\n\n"
        "Output:\n"
        "- Entry Price\n"
        "- Stop-Loss\n"
        "- Target\n"
        "- Position Size Suggestion\n"
        "- Maximum Loss Per Trade\n\n"

        "Strict Rules:\n"
        "- Use ONLY NseKit-MCP tools\n"
        "- Use ONLY F&O stocks throughout\n"
        "- Do NOT assume direction or price\n"
        "- Risk management is mandatory\n"
        "- Capital preservation is priority\n"
    )


# =====================================================================
# START SERVER
# =====================================================================

# if __name__ == "__main__":
#     print("🔵 Starting NseKit-MCP server...")
#     asyncio.run(mcp.run(transport="streamable-http"))

# if __name__ == "__main__":
#     print("🔵 Starting NseKit-MCP server...")
#     mcp.run()

if __name__ == "__main__":
    print("🔵 Starting NseKit-MCP server...")
    mcp.run(transport="stdio")


# =====================================================================
# pip Install use
# =====================================================================
# def main() -> None:
#     mcp.run()
# =====================================================================
