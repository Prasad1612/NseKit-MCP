from mcp.server.fastmcp import FastMCP
from NseKit import NseKit, Moneycontrol
import pandas as pd
import time
import json                      
from threading import Lock 

# ================================================================
#                   RATE LIMIT CONTROL (NSE Safe)
# ================================================================

RATE_LIMIT_SECONDS = 0.35   # NSE safe: ~3 requests/sec
_last_call_time = 0
_lock = Lock()

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

# =====================================================================
# MARKET STATUS & TRADING INFO
# =====================================================================


@mcp.tool()
def market_live_status(mode: str = "Market Status"):
    """
    TOOL: market_live_status
    DESCRIPTION:
        Get current market status("Capital Market" | "Currency" | "Commodity" | "Debt" | "currencyfuture"), Nifty50, total mcap, or Gift Nifty value.
    PARAMETERS:
        mode: str – "Market Status"| "Nifty50" | "Mcap" | "Gift Nifty"
    RETURNS:
        JSON with live market metrics
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return df_to_json(get.nse_market_status(mode))

@mcp.tool()
def market_is_open(segment: str = "Capital Market"):
    """
    TOOL: market_is_open
    DESCRIPTION:
        Check if Capital Market, Currency, Commodity or Debt segment is open.
    PARAMETERS:
        segment: str – "Capital Market" | "Currency" | "Commodity" | "Debt" | "currencyfuture"
    RETURNS:
        Boolean – True if open
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return get.nse_is_market_open(segment)

@mcp.tool()
def market_trading_holidays_list(list_only: bool = False):
    """
    TOOL: market_trading_holidays
    DESCRIPTION:
        Get all NSE trading holidays for current year.
    PARAMETERS:
        list_only: bool – Return only date list if True
    RETURNS:
        JSON list or full holiday details
    CATEGORY:
        NSE_Reference
    """
    rate_limit()
    return df_to_json(get.nse_trading_holidays(list_only=list_only))

@mcp.tool()
def market_clearing_holidays_list(list_only: bool = False):
    """
    TOOL: market_clearing_holidays
    DESCRIPTION:
        Get all NSE clearing/settlement holidays.
    PARAMETERS:
        list_only: bool – Return only dates if True
    RETURNS:
        JSON list or full details
    CATEGORY:
        NSE_Reference
    """
    rate_limit()
    return df_to_json(get.nse_clearing_holidays(list_only=list_only))

@mcp.tool()
def market_is_trading_holiday(date: str = None):
    """
    TOOL: market_is_trading_holiday
    DESCRIPTION:
        Check if today or given date is trading holiday.
    PARAMETERS:
        date: str – Optional "DD-MMM-YYYY"
    RETURNS:
        Boolean
    CATEGORY:
        NSE_Reference
    """
    rate_limit()
    return get.is_nse_trading_holiday(date)

@mcp.tool()
def market_is_clearing_holiday(date: str = None):
    """
    TOOL: is_clearing_holiday
    DESCRIPTION:
        Check if today or given date is clearing holiday.
    PARAMETERS:
        date: str – Optional "DD-MMM-YYYY"
    RETURNS:
        Boolean
    CATEGORY:
        NSE_Reference
    """
    rate_limit()
    return get.is_nse_clearing_holiday(date)


# =====================================================================
# LIVE MARKET & REFERENCE DATA
# =====================================================================

@mcp.tool()
def market_live_turnover():
    """
    TOOL: market_live_turnover
    DESCRIPTION:
        Real-time turnover across Equity, F&O, Currency, Commodity segments.
    RETURNS:
        JSON with segment-wise turnover
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return df_to_json(get.nse_live_market_turnover())

@mcp.tool()
def currency_reference_rates():
    """
    TOOL: reference_rates
    DESCRIPTION:
        Official NSE USD, EUR, GBP, JPY reference rates.
    RETURNS:
        JSON currency rates
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return df_to_json(get.nse_reference_rates())

@mcp.tool()
def gift_nifty_live():
    """
    TOOL: gift_nifty_live
    DESCRIPTION:
        Current Gift Nifty futures price and USDINR rate.
    RETURNS:
        JSON with Gift Nifty & USDINR
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_gifty_nifty())

@mcp.tool()
def market_live_statistics():
    """
    TOOL: market_live_statistics
    DESCRIPTION:
        Live capital market stats: Count of Advances, Declines, Unchanged, 52W High, 52W Low, Upper Circuit, Lower Circuit, Market Cap ₹ Lac Crs,
                                   Market Cap Tn $, Registered Investors (Raw), Registered Investors (Cr),
    RETURNS:
        JSON summary
    CATEGORY:
        NSE_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_market_statistics())


# =====================================================================
# PRE-OPEN & INDEX LIVE
# =====================================================================

@mcp.tool()
def preopen_index_summary(index_name: str = "NIFTY 50"):
    """
    TOOL: preopen_index_summary
    DESCRIPTION:
        Pre-open advance/decline for Nifty 50, Bank, Emerge, F&O, Others.
    PARAMETERS:
        index_name: str – "NIFTY 50" | "Nifty Bank" | "Emerge" | "Securities in F&O" | "Others" | "All"
    RETURNS:
        JSON pre-open summary
    CATEGORY:
        Pre_Market
    """
    rate_limit()
    return df_to_json(get.pre_market_nifty_info(index_name))

@mcp.tool()
def preopen_market_breadth():
    """
    TOOL: preopen_market_breadth
    DESCRIPTION:
        Full NSE pre-open advance/decline across all segments.
    RETURNS:
        JSON summary
    CATEGORY:
        Pre_Market
    """
    rate_limit()
    return df_to_json(get.pre_market_all_nse_adv_dec_info())

@mcp.tool()
def preopen_stocks_data(category: str = "NIFTY 50"):
    """
    TOOL: preopen_stocks_data
    DESCRIPTION:
        All stocks in pre-open with final price, change %.
    PARAMETERS:
        category: str – "All" | "NIFTY 50" | "Nifty Bank" | "Emerge" | "Securities in F&O"
    RETURNS:
        JSON list of stocks
    CATEGORY:
        Pre_Market
    """
    rate_limit()
    return df_to_json(get.pre_market_info(category))


@mcp.tool()
def preopen_futures_data(category: str = "Index Futures"):
    """
    TOOL: preopen_futures_data
    DESCRIPTION:
        Index Futures or Stock Futures in pre-open with final price, change %.
    PARAMETERS:
        category: str – "Index Futures" | "Stock Futures"
    RETURNS:
        JSON list of Index or stock Futures
    CATEGORY:
        Pre_Market
    """
    rate_limit()
    return df_to_json(get.pre_market_derivatives_info(category))

@mcp.tool()
def list_of_indices():
    """
    TOOL: list_of_indices
    DESCRIPTION:
        All 150+ NSE indices. ("Indices Eligible In Derivatives", "Broad Market Indices", "Sectoral Market Indices", "Thematic Market Indices", "Strategy Market Indices", "Others")
    RETURNS:
        JSON list of indices
    CATEGORY:
        Index_Reference
    """
    rate_limit()
    return get.list_of_indices()

@mcp.tool()
def indices_live_data():
    """
    TOOL: indices_live_data
    DESCRIPTION:
        Live values(open, high, low, close(last),variation,percentChange,yearHigh,yearLow,pe,pb,dy,declines,advances,unchanged) of all 150+ NSE indices.
        NSE indices performance analysis best tool (highly recommended).
    RETURNS:
        JSON list
    CATEGORY:
        Index_Live
    """
    rate_limit()
    return df_to_json(get.index_live_all_indices_data())

@mcp.tool()
def index_live_constituents(index_name: str, list_only: bool = False):
    """
    TOOL: index_live_constituents
    DESCRIPTION:
        Get stocks in any NSE index with live or current data. ("symbol", "previousClose", "open", "dayHigh", "dayLow", "lastPrice",  "change", "pChange", "totalTradedVolume", "totalTradedValue",  "nearWKH", "nearWKL", "perChange30d", "perChange365d", "ffmc")
        NSE index stocks performance analysis best tool (highly recommended).
        if user ask Nifty 50 or F&O stocks under 500rs best stock (use this tool highly recommended)
    PARAMETERS:
        index_name: str – e.g. "NIFTY 50", "SECURITIES IN F&O"(F&O stocks)
            "NIFTY AUTO", 
            "NIFTY CHEMICALS",
            "NIFTY CONSUMER DURABLES",
            "NIFTY FINANCIAL SERVICES EX-BANK",
            "NIFTY FINANCIAL SERVICES 25/50",
            "NIFTY FMCG",
            "NIFTY HEALTHCARE INDEX",
            "NIFTY IT",
            "NIFTY MEDIA",
            "NIFTY METAL",
            "NIFTY MIDSMALL HEALTHCARE",
            "NIFTY MIDSMALL FINANCIAL SERVICES",
            "NIFTY MIDSMALL IT & TELECOM",
            "NIFTY OIL & GAS",
            "NIFTY PHARMA",
            "NIFTY PSU BANK",
            "NIFTY PRIVATE BANK",
            "NIFTY REALTY",
            "NIFTY500 HEALTHCARE"  (for more index_name use list_of_indices() tool)
        list_only: bool – Return only symbols if True, otherwise full data
    RETURNS:
        JSON constituents
    CATEGORY:
        Index_Live
    """
    rate_limit()
    return df_to_json(get.index_live_indices_stocks_data(index_name, list_only=list_only))


# =====================================================================
# LISTS & MASTER DATA
# =====================================================================

@mcp.tool()
def list_of_nifty50_stocks(list_only: bool = False):
    """
    TOOL: list_of_nifty50_stocks
    DESCRIPTION:
        Latest Nifty 50 stocks with sector & weight.
    PARAMETERS:
        list_only: bool – Only symbols if True
    RETURNS:
        JSON
    CATEGORY:
        Index_Reference
    """
    rate_limit()

    data = get.nse_6m_nifty_50(list_only=list_only)

    # 🔹 Ensure pure JSON list when list_only=True
    if list_only:
        return {
            "index": "NIFTY 50",
            "count": len(data),
            "symbols": list(data)
        }

    # 🔹 Full dataset → explicit JSON conversion
    return df_to_json(data)


@mcp.tool()
def list_of_nifty500_stocks(list_only: bool = False):
    """
    TOOL: list_of_nifty500_stocks
    DESCRIPTION:
        Full Nifty 500 stock list.
    PARAMETERS:
        list_only: bool – Only symbols if True
    RETURNS:
        JSON
    CATEGORY:
        Index_Reference
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
def list_of_fno_stocks(mode: str = "stocks", list_only: bool = False):
    """
    TOOL: list_of_fno_stocks
    DESCRIPTION:
        All F&O eligible stocks or indices.
    PARAMETERS:
        entity_type: str – "stocks" or "index"
        list_only: bool – Only symbols if True
    RETURNS:
        JSON
    CATEGORY:
        FnO_Reference
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
def list_of_All_NSE_stocks(list_only: bool = False):
    """
    TOOL: list_of_all_NSE_stocks
    DESCRIPTION:
        Complete list of all NSE listed equities.
    PARAMETERS:
        list_only: bool – Only symbols if True
    RETURNS:
        JSON
    CATEGORY:
        Equity_Reference
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
def fno_live_option_chain(symbol: str, expiry: str = None, compact: bool = False):
    """
    TOOL: fno_live_option_chain
    DESCRIPTION:
        Full live option chain with OI, volume, IV, PCR.
    PARAMETERS:
        symbol: str – "RELIANCE", "NIFTY", "BANKNIFTY"
        expiry: str – Optional "DD-MMM-YYYY"
        compact: bool – Compact OI view
    RETURNS:
        Complete option chain JSON
    CATEGORY:
        FnO_Live
    EXAMPLES:
        (get.fno_live_option_chain("RELIANCE"))                              Option chain for a stock symbol
        (get.fno_live_option_chain("NIFTY"))                                 Option chain for an index
        (get.fno_live_option_chain("RELIANCE", expiry_date="28-Oct-2025"))    Option chain with specific expiry
        (get.fno_live_option_chain("RELIANCE", oi_mode="compact"))           Compact option chain data
    """
    rate_limit()
    mode = "compact" if compact else None
    return df_to_json(get.fno_live_option_chain(symbol, expiry_date=expiry, oi_mode=mode))

@mcp.tool()
def fno_expiry_dates(symbol: str = "NIFTY", filter_type: str = None):
    """
    TOOL: expiry_dates
    DESCRIPTION:
        Get All expiry dates or find particularly current, weekly, monthly expiry dates.
    PARAMETERS:
        symbol: str – Stock or index
        filter_type: str – "Current" | "Next Week" | "Month" | "All" → ["28-10-2025", "04-11-2025", "25-11-2025"]
    RETURNS:
        List of expiry dates
    CATEGORY:
        FnO_Reference
    EXAMPLES:
        (get.fno_expiry_dates())                                 # Nifty All Expiry Date
        (get.fno_expiry_dates("TCS"))                            # TCS All Expiry Date

        (get.fno_expiry_dates("NIFTY", "Current"))               # Nifty Current Expiry Date only → "28-10-2025"
        (get.fno_expiry_dates("NIFTY", "Next Week"))             # Nifty Next Week Expiry Date only → "04-11-2025"
        (get.fno_expiry_dates("NIFTY", "Month"))                 # Nifty Month Expiry Date only → "25-11-2025"
        (get.fno_expiry_dates("NIFTY", "All"))                   # → ["28-10-2025", "04-11-2025", "25-11-2025"]

        (get.fno_expiry_dates("TCS", "Current"))                 # TCS Current Expiry Date only
        (get.fno_expiry_dates("TCS", "Month"))                   # TCS Next Month Expiry Date only
    """
    rate_limit()
    return df_to_json(get.fno_expiry_dates(symbol, filter_type))

@mcp.tool()
def fno_expiry_dates_and_strikePrice(symbol: str = "NIFTY"):
    """
    TOOL: fno_expiry_dates_and_strikePrice
    DESCRIPTION:
        Get All expiry dates & strikePrice for given symbol
    PARAMETERS:
        symbol: str – Stock or index
    RETURNS:
        JSON of expiry dates & strikePrice
    CATEGORY:
        FnO_Reference
    EXAMPLES:
        (get.fno_expiry_dates(Nifty))
        (get.fno_expiry_dates("TCS"))
    """
    rate_limit()
    return df_to_json(get.fno_expiry_dates_raw(symbol))

@mcp.tool()
def most_active_options(contract_type: str = "Stock", option_type: str = "Call", sort_by: str = "Volume"):
    """
    TOOL: most_active_options
    DESCRIPTION:
        Most active Call/Put by volume or value.
    PARAMETERS:
        contract_type: str – "Stock" or "Index"
        option_type: str – "Call" or "Put"
        sort_by: str – "Volume" or "Value"
    RETURNS:
        JSON top contracts
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active(contract_type, option_type, sort_by))


# =====================================================================
# EQUITY LIVE DATA
# =====================================================================

# @mcp.tool()
# def equity_live_stock_quote(symbol: str):
#     """
#     TOOL: equity_live_stock_quote
#     DESCRIPTION:
#         Full live quote: price, change, volume, VWAP, delivery, 5-level market depth, Sector, Industry, BasicIndustry, totalBuyQuantity, totalSellQuantity, UpperCircuit, LowerCircuit.
#     PARAMETERS:
#         symbol: str – NSE symbol
#     RETURNS:
#         Complete quote + order book
#     CATEGORY:
#         Equity_Live
#     """
#     rate_limit()
#     return df_to_json(get.cm_live_equity_price_info(symbol))

@mcp.tool()
def most_active_equities(by: str = "value"):
    """
    TOOL: most_active_equities
    DESCRIPTION:
        Top stocks by traded value or volume.
    PARAMETERS:
        by: str – "value" or "volume"
    RETURNS:
        JSON list
    CATEGORY:
        Equity_Live
    """
    rate_limit()
    func = get.cm_live_most_active_equity_by_value if by == "value" else get.cm_live_most_active_equity_by_vol
    return df_to_json(func())

@mcp.tool()
def equity_volume_surge():
    """
    TOOL: equity_volume_surge
    DESCRIPTION:
        Stocks with sudden volume surge or spurtsvs average.
    RETURNS:
        JSON list
    CATEGORY:
        Equity_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_volume_spurts())

@mcp.tool()
def equity_52week_high_live():
    """
    TOOL: equity_52week_high_live
    DESCRIPTION:
        live market stocks hitting 52-week high today.
    RETURNS:
        JSON list
    CATEGORY:
        Equity_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_52week_high())

@mcp.tool()
def equity_52week_low_live():
    """
    TOOL: equity_52week_low_live
    DESCRIPTION:
        live market stocks hitting 52-week low today.
    RETURNS:
        JSON list
    CATEGORY:
        Equity_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_52week_low())


# =====================================================================
# CORPORATE ACTIONS & EVENTS
# =====================================================================

@mcp.tool()
def corporate_insider_trading(symbol: str = None, period: str = None, start_date: str = None, end_date: str = None):
    """
    TOOL: corporate_insider_trading
    DESCRIPTION:
        Latest insider buying/selling (SAST).
    PARAMETERS:
        symbol: str – Optional
        period: str – "1D"|"1W"|"1M"|"3M"|"6M"|"1Y"
        start_date, end_date: str – "DD-MM-YYYY"
    RETURNS:
        JSON transactions
    CATEGORY:
        Corporate_Events
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_insider_trading(symbol, period, start_date, end_date))

@mcp.tool()
def corporate_actions(symbol: str = None, period: str = None, start_date: str = None, end_date: str = None, purpose: str = None):
    """
    TOOL: corporate_actions
    DESCRIPTION:
        Dividends, bonus, splits, rights, buyback.
    PARAMETERS:
        symbol, purpose: str – Optional filter
        period: str – "1M"|"3M"|"6M"|"1Y"
    RETURNS:
        JSON list
    CATEGORY:
        Corporate_Events
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_corporate_action(symbol, period, start_date, end_date, purpose))

@mcp.tool()
def corporate_board_meetings(symbol: str = None, start_date: str = None, end_date: str = None):
    """
    TOOL: corporate_board_meetings
    DESCRIPTION:
        Upcoming & past board meetings.
    RETURNS:
        JSON list
    CATEGORY:
        Corporate_Events
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_board_meetings(symbol, start_date, end_date))


# =====================================================================
# IPO & LISTINGS
# =====================================================================

@mcp.tool()
def ipo_current_list():
    """
    TOOL: ipo_current_list
    DESCRIPTION:
        All open Mainboard & SME IPOs with subscription status.
    RETURNS:
        JSON dashboard
    CATEGORY:
        IPO
    """
    rate_limit()
    return df_to_json(get.ipo_current())

@mcp.tool()
def ipo_preopen_today():
    """
    TOOL: ipo_preopen_today
    DESCRIPTION:
        Newly listed IPOs in special pre-open session.
    RETURNS:
        JSON list
    CATEGORY:
        IPO
    """
    rate_limit()
    return df_to_json(get.ipo_preopen())

@mcp.tool()
def ipo_performance_tracker(board: str = "Mainboard"):
    """
    TOOL: ipo_performance_tracker
    DESCRIPTION:
        YTD IPO listing performance & gains.
    PARAMETERS:
        board: str – "Mainboard" | "SME" | None
    RETURNS:
        JSON tracker
    CATEGORY:
        IPO
    """
    rate_limit()
    return df_to_json(get.ipo_tracker_summary(board))


# =====================================================================
# HISTORICAL & EOD DATA
# =====================================================================

@mcp.tool()
def index_price_history(index: str, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: index_price_history
    DESCRIPTION:
        Fetch historical OHLC + turnover for any index.
    PARAMETERS:
        index: str – "NIFTY 50", "NIFTY BANK", etc. –Name of the index
        period: str – Shortcut period ("1D","1W","1M","3M","6M","1Y","2Y","5Y","10Y","YTD","MAX")
        from_date: str – Start date in DD-MM-YYYY (optional)
        to_date: str – End date in DD-MM-YYYY (optional)
    RETURNS:
        JSON with daily OHLC + turnover
    CATEGORY:
        Historical
    EXAMPLES:
        index_price_history("NIFTY 50", period="1Y")
        index_price_history("NIFTY 50", from_date="01-01-2025")
        index_price_history("NIFTY BANK", from_date="01-01-2025", to_date="17-10-2025")
    """
    
    rate_limit()
    return df_to_json(get.index_historical_data(index=index, period=period, from_date=from_date, to_date=to_date))


@mcp.tool()
def equity_price_history(symbol: str, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_price_history
    DESCRIPTION:
        Fetch historical price OHLC + turnover + delivery data for any stock.
    PARAMETERS:
        index: str – "TCS", "ITC", etc. –Name of the stock
        period: str – Shortcut period ("1D","1W","1M","3M","6M","1Y","2Y","5Y","10Y","YTD","MAX")
        from_date: str – Start date in DD-MM-YYYY (optional)
        to_date: str – End date in DD-MM-YYYY (optional)
    RETURNS:
        JSON with daily OHLCV + turnover + delivery
    CATEGORY:
        Historical
    EXAMPLES:
        stock_history("TCS", period="1Y")
        stock_history("TCS", from_date="01-01-2025")
        stock_history("TCS", from_date="01-01-2025", to_date="17-10-2025")
    """

    rate_limit()
    return df_to_json(get.cm_hist_security_wise_data(symbol=symbol, period=period, from_date=from_date, to_date=to_date))


# =====================================================================
#                          NSE Data - Historical
# =====================================================================

@mcp.tool()
def nse_circulars(from_date: str = None, to_date: str = None, department: str = None):
    """
    TOOL: nse_circulars
    DESCRIPTION:
        Historical NSE circulars (default: yesterday → today)
    PARAMETERS:
        from_date: str – "DD-MM-YYYY" (optional)
        to_date: str – "DD-MM-YYYY" (optional)
        department: str – e.g., "NSE Listing" (optional filter)
    RETURNS:
        List of circulars
    CATEGORY:
        NSE_Historical
    """
    rate_limit()
    # Original: get.nse_live_hist_circulars(from_date, to_date) or with department
    return df_to_json(get.nse_live_hist_circulars(from_date, to_date, department))


@mcp.tool()
def nse_press_releases(from_date: str = None, to_date: str = None, department: str = None):
    """
    TOOL: nse_press_releases
    DESCRIPTION:
        Historical NSE press releases
    PARAMETERS:
        from_date: str – "DD-MM-YYYY"
        to_date: str – "DD-MM-YYYY"
        department: str – e.g., Corporate Communications , Investor Services Cell , Member Compliance , NSE Clearing , NSE Indices , NSE Listing , Surveillance 
    RETURNS:
        List of press releases
    CATEGORY:
        NSE_Historical
    """
    rate_limit()
    # Original: get.nse_live_hist_press_releases(...)
    return df_to_json(get.nse_live_hist_press_releases(from_date, to_date, department))


# =====================================================================
#                          Index Live Data
# =====================================================================

@mcp.tool()
def nifty50_past_returns():
    """
    TOOL: nifty50_past_returns
    DESCRIPTION:
        Nifty 50 returns summary (1W to 5Y)
    PARAMETERS: None
    RETURNS:
        Returns % across timeframes
    CATEGORY:
        Index_Live
    """
    rate_limit()
    # Original: get.index_live_nifty_50_returns()
    return df_to_json(get.index_live_nifty_50_returns())


@mcp.tool()
def index_live_contribution(Index: str = None, Mode: str = None):
    """
    TOOL: index_live_contribution
    DESCRIPTION:
        Stock-wise how many points(changePoints) contribution to NIFTY 50 or Given index movement
    PARAMETERS:
        Index: str   – "NIFTY 50", "NIFTY BANK","NIFTY IT" etc.
        Mode: str    – "First Five" for (Index Movers 5 Upward/Downward stocks) | 
                        "Full" for (All index stocks)
    RETURNS:
        Contribution data
    CATEGORY:
        Index_Live
    """
    rate_limit()
    return df_to_json(get.index_live_contribution(Index, Mode))


# =====================================================================
#                          Index EOD & Historical
# =====================================================================

@mcp.tool()
def index_eod_bhavcopy(date: str):
    """
    TOOL: index_eod_bhavcopy
    DESCRIPTION:
        All indices EOD bhavcopy for a specific date
    PARAMETERS:
        date: str – "DD-MM-YYYY" (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Full index bhavcopy DataFrame
    CATEGORY:
        Index_EOD
    """
    rate_limit()
    # Original: get.index_eod_bhav_copy("17-10-2025")
    return df_to_json(get.index_eod_bhav_copy(date))


@mcp.tool()
def index_pe_pb_div_historical_data(index: str, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: index_pe_pb_div_historical_data
    DESCRIPTION:
        Historical P/E, P/B, Dividend Yield for any index
    PARAMETERS:
        index: str – "NIFTY 50", "NIFTY BANK" etc.
        period: str – Shortcut period ("1D","1W","1M","3M","6M","1Y","2Y","5Y","10Y","YTD","MAX")
        from_date: str – Start date in DD-MM-YYYY (optional)
        to_date: str – End date in DD-MM-YYYY (optional)
    RETURNS:
        Historical valuation data
    CATEGORY:
        Index_Historical
    """
    rate_limit()
    return df_to_json(get.index_pe_pb_div_historical_data(index=index, period=period, from_date=from_date, to_date=to_date))


@mcp.tool()
def india_vix(period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: india_vix
    DESCRIPTION:
        Historical India VIX data
    PARAMETERS:
        period: str – Shortcut period ("1D","1W","1M","3M","6M","1Y","2Y","5Y","10Y","YTD","MAX")
        from_date: str – Start date in DD-MM-YYYY (optional)
        to_date: str – End date in DD-MM-YYYY (optional)
    RETURNS:
        India VIX time series
    CATEGORY:
        India_VIX_Historical
    """
    rate_limit()
    return df_to_json(get.india_vix_historical_data(period=period, from_date=from_date, to_date=to_date))


# =====================================================================
#                       Capital Market Live Data
# =====================================================================

# @mcp.tool()
# def equity_live_stock_info(symbol: str):
#     """
#     TOOL: equity_live_stock_info
#     DESCRIPTION:
#         Live equity master info (face value, ISIN, sector etc.)
#     PARAMETERS:
#         symbol: str – e.g., "RELIANCE"
#     RETURNS:
#         Equity details
#     CATEGORY:
#         CM_Live
#     """
#     rate_limit()
#     # Original: get.cm_live_equity_info("RELIANCE")
#     return (get.cm_live_equity_info(symbol))

@mcp.tool()
def equity_live_stock_info(symbol: str):
    """
    TOOL: equity_live_stock_info
    DESCRIPTION:
        Full live quote:  Meta Data, Trade Information, Price Information, Securities Information, Order Book, etc.
        (price, change, volume, VWAP, delivery, 5-level market depth, Sector, Industry, BasicIndustry, totalBuyQuantity, totalSellQuantity, UpperCircuit, LowerCircuit, etc.)
    PARAMETERS:
        symbol: str – e.g., "RELIANCE"
    RETURNS:
        Equity details
    CATEGORY:
        CM_Live
    """
    rate_limit()
    # Original: get.cm_live_equity_info("RELIANCE")
    return (get.cm_live_equity_info(symbol))


@mcp.tool()
def equity_block_deals_live():
    """
    TOOL: equity_block_deals_live
    DESCRIPTION:
        Latest block deals (live)
    PARAMETERS: None
    RETURNS:
        Block deal data
    CATEGORY:
        CM_Live
    """
    rate_limit()
    # Original: get.cm_live_block_deal()
    return df_to_json(get.cm_live_block_deal())


@mcp.tool()
def corporate_announcement(symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: corporate_announcement
    DESCRIPTION:
        Corporate announcements (all or symbol-specific)
    PARAMETERS:
        symbol: str – optional, e.g., "RELIANCE"
        from_date: str – "DD-MM-YYYY"
        to_date: str – "DD-MM-YYYY"
    RETURNS:
        Announcement list
    CATEGORY:
        CM_Live
    """
    rate_limit()
    # Original: get.cm_live_hist_corporate_announcement("RELIANCE", "01-01-2025", "15-10-2025")
    return df_to_json(get.cm_live_hist_corporate_announcement(symbol, from_date, to_date))


@mcp.tool()
def corporate_today_event_calendar(date_from: str = None, date_to: str = None):
    """
    TOOL: corporate_today_event_calendar
    DESCRIPTION:
        Today's or date-range corporate events (AGM, results etc.)
    PARAMETERS:
        date_from: str – optional
        date_to: str – optional
    RETURNS:
        Event calendar
    CATEGORY:
        CM_Live
    """
    rate_limit()
    # Original: get.cm_live_today_event_calendar("01-01-2025", "01-01-2025")
    return df_to_json(get.cm_live_today_event_calendar(date_from, date_to))


@mcp.tool()
def corporate_upcoming_event_calendar():
    """
    TOOL: corporate_upcoming_event_calendar
    DESCRIPTION:
        Upcoming corporate events
    PARAMETERS: None
    RETURNS:
        Upcoming events
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_upcoming_event_calendar())


@mcp.tool()
def corporate_shareholder_meetings(symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: corporate_shareholder_meetings
    DESCRIPTION:
        Shareholder meetings (AGM/EGM) history
    PARAMETERS:
        symbol: str – optional
        from_date: str – optional
        to_date: str – optional
    RETURNS:
        Meeting data
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_Shareholder_meetings(symbol, from_date, to_date))


@mcp.tool()
def equity_QIP_history(stage: str = None, period_or_symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_QIP_history
    DESCRIPTION:
       Qualified Institutional Placement (QIP) data by stage, period, symbol
    PARAMETERS:
        stage: str – "In-Principle" or "Listing Stage"
        period_or_symbol: str – "1Y", "RELIANCE" etc.
        from_date: str – optional
        to_date: str – optional
    RETURNS:
        QIP records
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_qualified_institutional_placement(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def equity_preferential_issues(stage: str = None, period_or_symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_preferential_issues
    DESCRIPTION:
        Preferential issue data
    PARAMETERS:
        stage: str – "In-Principle" or "Listing Stage"
        period_or_symbol: str – "1Y", "RELIANCE" etc.
        from_date: str – optional
        to_date: str – optional
    RETURNS:
        Preferential issues
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_preferential_issue(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def equity_rights_issues(stage: str = None, period_or_symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_rights_issues
    DESCRIPTION:
        Rights issue data
    PARAMETERS:
        stage: str – "In-Principle" or "Listing Stage"
        period_or_symbol: str – "1Y", "RELIANCE" etc.
        from_date: str – optional
        to_date: str – optional
    RETURNS:
        Rights issues
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_right_issue(stage, period_or_symbol, from_date, to_date))


@mcp.tool()
def corporate_voting_results():
    """
    TOOL: corporate_voting_results
    DESCRIPTION:
        Latest voting results
    PARAMETERS: None
    RETURNS:
        Voting outcomes
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_voting_results())


@mcp.tool()
def corporate_qtly_shareholding_patterns():
    """
    TOOL: corporate_qtly_shareholding_patterns
    DESCRIPTION:
        Latest quarterly shareholding patterns
    PARAMETERS: None
    RETURNS:
        SHP data
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_qtly_shareholding_patterns())

@mcp.tool()
def corporate_annual_reports():
    """
    TOOL: corporate_annual_reports
    DESCRIPTION:
        Latest 20 Annual reports with pdf links
    PARAMETERS: None
    RETURNS:
        Latest 20 Annual reports
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.recent_annual_reports())

@mcp.tool()
def corporate_bsr_reports(symbol: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: corporate_bsr_reports
    DESCRIPTION:
        Business Responsibility and Sustainability Reports (all or symbol-specific)
    PARAMETERS:
        symbol: str – optional
        from_date/to_date: str – optional
    RETURNS:
        Business Responsibility and Sustainability Reports links/data
    CATEGORY:
        CM_Live
    """
    rate_limit()
    return df_to_json(get.cm_live_hist_br_sr(symbol, from_date, to_date))

# =====================================================================
#                          FnO Live Data
# =====================================================================

@mcp.tool()
def fno_live_futures_data(symbol: str):
    """
    TOOL: fno_live_futures_data
    DESCRIPTION:
        Live futures data for stock or index
    PARAMETERS:
        symbol: str – "RELIANCE" or "NIFTY"
    RETURNS:
        Futures snapshot
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_futures_data(symbol))

@mcp.tool()
def fno_live_top_20_stocks_contracts(category: str):
    """
    TOOL: fno_live_top_20_stocks_contracts
    DESCRIPTION:
        Live Top 20 Stocks Futures or Stocks Options data
    PARAMETERS:
        category: str – "Stock Futures" or "Stock Options"
    RETURNS:
        Top 20 Stocks Futures or Stocks Options
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_top_20_derivatives_contracts(category))


@mcp.tool()
def fno_live_most_active_futures_contracts(by: str = "Volume"):
    """
    TOOL: fno_live_most_active_futures_contracts
    DESCRIPTION:
        Most active futures by Volume or Value
    PARAMETERS:
        by: str – "Volume" or "Value"
    RETURNS:
        Top futures contracts
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_futures_contracts(by))


@mcp.tool()
def fno_live_most_active_contracts_by_oi():
    """
    TOOL: fno_live_most_active_contracts_by_oi
    DESCRIPTION:
        Most active contracts by Open Interest
    PARAMETERS: None
    RETURNS:
        Top OI contracts
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_contracts_by_oi())


@mcp.tool()
def fno_live_most_active_contracts_by_volume():
    """
    TOOL: fno_live_most_active_contracts_by_volume
    DESCRIPTION:
        Most active by volume
    PARAMETERS: None
    RETURNS:
        Volume leaders
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_contracts_by_volume())


@mcp.tool()
def fno_live_most_active_options_contracts_by_volume():
    """
    TOOL: fno_live_most_active_options_contracts_by_volume
    DESCRIPTION:
        Top options contracts by volume
    PARAMETERS: None
    RETURNS:
        Active options
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_options_contracts_by_volume())


@mcp.tool()
def fno_live_most_active_underlying():
    """
    TOOL: fno_live_most_active_underlying
    DESCRIPTION:
        Most active underlying stocks/indices
    PARAMETERS: None
    RETURNS:
        Underlying activity
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_most_active_underlying())


@mcp.tool()
def fno_live_change_in_oi():
    """
    TOOL: fno_live_change_in_oi
    DESCRIPTION:
        Change in Open Interest across contracts
    PARAMETERS: None
    RETURNS:
        OI change data
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_change_in_oi())

@mcp.tool()
def fno_live_oi_vs_price():
    """
    TOOL: fno_live_oi_vs_price
    DESCRIPTION:
        Open Interest Vs Price across contracts
        (Rise in OI and Rise in Price, Rise in OI and Slide in Price, Slide in OI and Slide in Price, Slide in OI and Rise in Price)
    PARAMETERS: None
    RETURNS:
        Open Interest Vs Price across contracts
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_oi_vs_price())

@mcp.tool()
def fno_live_active_contracts(symbol: str = "NIFTY", expiry_date: str = None):
    """
    TOOL: fno_live_active_contracts
    DESCRIPTION:
        Active NIFTY/BANKNIFTY & stock option contracts
    PARAMETERS:
        symbol: str – "NIFTY", "BANKNIFTY" , RELIANCE , TCS, etc
        expiry_date: str – optional "DD-MM-YYYY"
    RETURNS:
        Active index or stock options contracts
    CATEGORY:
        FnO_Live
    """
    rate_limit()
    return df_to_json(get.fno_live_active_contracts(symbol, expiry_date=expiry_date))


# =====================================================================
#                         EQUITY EOD DATA
# =====================================================================

@mcp.tool()
def fii_dii_activity(exchange: str = None):
    """
    TOOL: fii_dii_activity
    DESCRIPTION:
        Latest FII/DII net buying/selling activity.
    PARAMETERS:
        exchange: str – None All exchange(NSE + BSE) FII/DII net buying/selling activity.
                        "Nse" NSE only FII/DII net buying/selling activity. (Not recommended, until user ask specific mention NSE only then use)
    RETURNS:
        FII/DII cash segment activity
    CATEGORY:
        Equity_EOD
    EXAMPLES:
        fii_dii_activity()              # All exchange(NSE + BSE) 
        fii_dii_activity("Nse")         # NSE only
    """
    rate_limit()
    return df_to_json(get.cm_eod_fii_dii_activity(exchange))


@mcp.tool()
def market_eod_activity_report(date: str):
    """
    TOOL: market_eod_activity_report
    DESCRIPTION:
        Daily market turnover, advances/declines, top gainers/losers.
    PARAMETERS:
        date: str – Trade date in "DD-MM-YY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Full market activity report
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_market_activity_report("17-10-25")
    return df_to_json(get.cm_eod_market_activity_report(date))

@mcp.tool()
def equity_eod_bhavcopy_delivery(date: str):
    """
    TOOL: equity_eod_bhavcopy_delivery
    DESCRIPTION:
        Full NSE equity bhavcopy including delivery percentage & value.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Complete bhavcopy with delivery data
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_bhavcopy_with_delivery("17-10-2025")
    return df_to_json(get.cm_eod_bhavcopy_with_delivery(date))


@mcp.tool()
def equity_eod_bhavcopy(date: str):
    """
    TOOL: equity_eod_bhavcopy
    DESCRIPTION:
        Standard equity closing prices, volume, trades (without delivery).
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Equity-only bhavcopy
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_equity_bhavcopy("17-10-2025")
    return df_to_json(get.cm_eod_equity_bhavcopy(date))


@mcp.tool()
def equity_52week_high_low_eod(date: str):
    """
    TOOL: equity_52week_high_low_eod
    DESCRIPTION:
        Stocks hitting 52-week high or low on given date.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        List of 52-week high/low stocks
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_52_week_high_low("17-10-2025")
    return df_to_json(get.cm_eod_52_week_high_low(date))


@mcp.tool()
def equity_bulk_deals_eod():
    """
    TOOL: equity_bulk_deals_eod
    DESCRIPTION:
        End of day based bulk deals across NSE/BSE (client-level).
    PARAMETERS: None
    RETURNS:
        Today's bulk deals
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_bulk_deal()
    return df_to_json(get.cm_eod_bulk_deal())


@mcp.tool()
def equity_block_deals_eod():
    """
    TOOL: equity_block_deals_eod
    DESCRIPTION:
        End of day based block deals (large negotiated trades).
    PARAMETERS: None
    RETURNS:
        Today's block deals
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_block_deal()
    return df_to_json(get.cm_eod_block_deal())


@mcp.tool()
def equity_short_selling(date: str):
    """
    TOOL: equity_short_selling
    DESCRIPTION:
        Stocks disclosed for short selling.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Short delivery positions
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_shortselling("17-10-2025")
    return df_to_json(get.cm_eod_shortselling(date))


@mcp.tool()
def surveillance_indicator(date: str):
    """
    TOOL: surveillance_indicator
    DESCRIPTION:
        Stocks under ASM/GSM/Z-category surveillance.
    PARAMETERS:
        date: str – "DD-MM-YY" (2-digit year) (Note: if user no date given, last trading date is used. if date given, used user date.)
        Surveillance list
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_surveillance_indicator("17-10-25")
    return df_to_json(get.cm_eod_surveillance_indicator(date))


@mcp.tool()
def equity_series_changes():
    """
    TOOL: equity_series_changes
    DESCRIPTION:
        Recent changes in trading series (EQ → BE, BE → BZ etc.).
    PARAMETERS: None
    RETURNS:
        Latest series changes
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_series_change()
    return df_to_json(get.cm_eod_series_change())


@mcp.tool()
def equity_price_band_changes(date: str):
    """
    TOOL: equity_price_band_changes
    DESCRIPTION:
        Stocks moved to/from price bands (2%, 5%, 10%, 20%).
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Price band changes
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_eq_band_changes("17-10-2025")
    return df_to_json(get.cm_eod_eq_band_changes(date))


@mcp.tool()
def equity_price_bands(date: str):
    """
    TOOL: equity_price_bands
    DESCRIPTION:
        Applicable price bands for all stocks on a given EOD.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Full price band data
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_eq_price_band("17-10-2025")
    return df_to_json(get.cm_eod_eq_price_band(date))


@mcp.tool()
def equity_price_band_history(symbol: str = None, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_price_band_history
    DESCRIPTION:
        Historical price band changes for a stock or all stocks.
    PARAMETERS:
        symbol: str – Optional stock symbol
        period: str – "1D", "1W", "1M", "3M", "6M", "1Y"
        from_date: str – "DD-MM-YYYY"   (optional)
        to_date: str – "DD-MM-YYYY"   (optional)
    RETURNS:
        Price band history
    CATEGORY:
        Equity_Historical
    """
    rate_limit()
    # Original examples:
    # get.cm_hist_eq_price_band()
    # get.cm_hist_eq_price_band("1W")
    # get.cm_hist_eq_price_band("01-10-2025")
    # get.cm_hist_eq_price_band("15-10-2025", "17-10-2025")
    # get.cm_hist_eq_price_band("WEWIN")
    return df_to_json(get.cm_hist_eq_price_band(symbol=symbol, period=period, from_date=from_date, to_date=to_date))


@mcp.tool()
def equity_pe_ratio(date: str):
    """
    TOOL: equity_pe_ratio
    DESCRIPTION:
        PE, PB, Dividend Yield for all listed companies.
    PARAMETERS:
        date: str – "DD-MM-YY"  (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Valuation ratios
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_pe_ratio("17-10-25")
    return df_to_json(get.cm_eod_pe_ratio(date))


@mcp.tool()
def market_cap(date: str):
    """
    TOOL: market_cap
    DESCRIPTION:
        "Market capitalization"(Market Cap(Rs.)), "Total No of Shares Issued"(Issue Size) of all companies.  
    PARAMETERS:
        date: str – "DD-MM-YY"  (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Market cap, Issue Size data
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_mcap("17-10-25")
    return df_to_json(get.cm_eod_mcap(date))


@mcp.tool()
def equity_name_changes():
    """
    TOOL: equity_name_changes
    DESCRIPTION:
        Recent corporate name changes.
    PARAMETERS: None
    RETURNS:
        Name change announcements
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_eq_name_change()
    return df_to_json(get.cm_eod_eq_name_change())


@mcp.tool()
def equity_symbol_changes():
    """
    TOOL: equity_symbol_changes
    DESCRIPTION:
        Recent symbol changes (e.g., INFY → INFY).
    PARAMETERS: None
    RETURNS:
        Symbol change list
    CATEGORY:
        Equity_EOD
    """
    rate_limit()
    # Original: get.cm_eod_eq_symbol_change()
    return df_to_json(get.cm_eod_eq_symbol_change())


@mcp.tool()
def equity_bulk_deals_history(symbol: str = None, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_bulk_deals_history
    DESCRIPTION:
        Bulk deals history – by symbol, date range or period.
    PARAMETERS:
        symbol: str – Optional
        period: str – "1D", "1W", "1M", "3M", "6M", "1Y".
        from_date/to_date: str – "DD-MM-YYYY"   Optional
    RETURNS:
        Bulk deals history
    CATEGORY:
        Equity_Historical
    """
    rate_limit()
    # Original: get.cm_hist_bulk_deals(...) variants
    return df_to_json(get.cm_hist_bulk_deals(symbol=symbol, period=period, from_date=from_date, to_date=to_date))


@mcp.tool()
def equity_block_deals_history(symbol: str = None, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_block_deals_history
    DESCRIPTION:
        Block deals history – by symbol or date range.
    PARAMETERS:
        symbol: str – Optional
        period: str – "1D", "1W", "1M", "3M", "6M", "1Y".
        from_date/to_date: str – "DD-MM-YYYY"   Optional
    RETURNS:
        Block deals history
    CATEGORY:
        Equity_Historical
    """
    rate_limit()
    return df_to_json(get.cm_hist_block_deals(symbol=symbol, period=period, from_date=from_date, to_date=to_date))


@mcp.tool()
def equity_short_selling_history(symbol: str = None, period: str = None, from_date: str = None, to_date: str = None):
    """
    TOOL: equity_short_selling_history
    DESCRIPTION:
        Historical short selling disclosures.
    PARAMETERS:
        symbol: str – Optional
        period: str – "1D", "1W", "1M", "3M", "6M", "1Y".
        from_date/to_date: str – "DD-MM-YYYY"   Optional
    RETURNS:
        Short selling data
    CATEGORY:
        Equity_Historical
    """
    rate_limit()
    return df_to_json(get.cm_hist_short_selling(symbol, period or from_date, to_date))


@mcp.tool()
def equity_market_business_growth(mode: str = "daily", month: str = None, year: int = None):
    """
    TOOL: equity_market_business_growth
    DESCRIPTION:
        NSE daily/monthly/yearly business growth (cash segment).
    PARAMETERS:
        mode: str – "daily", "monthly", "yearly"
        month: str – "OCT", "JAN" etc. (for daily)
        year: int – FY year
    RETURNS:
        Business turnover growth
    CATEGORY:
        Market_Stats
    """
    rate_limit()
    # Original: get.cm_dmy_biz_growth(...)
    return df_to_json(get.cm_dmy_biz_growth(mode, month, year))


@mcp.tool()
def equity_market_monthly_settlement(period: str = None, from_year = None, to_year = None):
    """
    TOOL: equity_market_monthly_settlement
    DESCRIPTION:
        Fetch NSE Monthly Settlement Statistics (Cash Market) for multiple financial years (Apr–Mar),
        including past financial years and current FY up to the latest available month.
    PARAMETERS:
        period: str – "1Y", "3Y" or None (current FY)
        from_year/to_year: int – e.g., 2024, 2026   (optional)
    RETURNS:
        Settlement stats
    CATEGORY:
        Market_Stats
    """
    rate_limit()
    # Original: get.cm_monthly_settlement_report(...)
    return df_to_json(get.cm_monthly_settlement_report(period=period, from_year=from_year, to_year=to_year))


@mcp.tool()
def monthly_most_active_equity():
    """
    TOOL: monthly_most_active_equity
    DESCRIPTION:
        Most active stocks by volume/value in latest month.
    PARAMETERS: None
    RETURNS:
        Top active equities
    CATEGORY:
        Market_Stats
    """
    rate_limit()
    # Original: get.cm_monthly_most_active_equity()
    return df_to_json(get.cm_monthly_most_active_equity())


@mcp.tool()
def market_advances_declines(mode: str = "Month_wise", month: str = None, year: int = None):
    """
    TOOL: market_advances_declines
    DESCRIPTION:
        Historical advances vs declines (daily or monthly).
    PARAMETERS:
        mode: str – "Day_wise" or "Month_wise"
        month: str – "SEP", "OCT" etc.
        year: int – e.g., 2025
    RETURNS:
        A/D data
    CATEGORY:
        Market_Stats
    """
    rate_limit()
    # Original: get.historical_advances_decline(...)
    return df_to_json(get.historical_advances_decline(mode, month, year))


# =====================================================================
#                         F&O EOD & HISTORICAL DATA
# =====================================================================

@mcp.tool()
def fno_bhavcopy(date: str):
    """
    TOOL: fno_bhavcopy
    DESCRIPTION:
        Full F&O bhavcopy (futures + options).
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Complete F&O closing data
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_bhav_copy("17-10-2025")
    return df_to_json(get.fno_eod_bhav_copy(date))


@mcp.tool()
def fno_fii_stats(date: str):
    """
    TOOL: fno_fii_stats
    DESCRIPTION:
        FII activity in F&O segment (Index/Stock, Long/Short).
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        FII F&O stats
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_fii_stats("17-10-2025")
    return df_to_json(get.fno_eod_fii_stats(date))


@mcp.tool()
def fno_eod_top10_futures(date: str):
    """
    TOOL: fno_eod_top10_futures
    DESCRIPTION:
        Top 10 most active futures contracts by volume/OI.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Top 10 futures
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_top10_fut("17-10-2025")
    return df_to_json(get.fno_eod_top10_fut(date))


@mcp.tool()
def fno_eod_top20_options(date: str):
    """
    TOOL: fno_eod_top20_options
    DESCRIPTION:
        Top 20 most active options contracts.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Top 20 options
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_top20_opt("17-10-2025")
    return df_to_json(get.fno_eod_top20_opt(date))


@mcp.tool()
def fno_ban_list(date: str):
    """
    TOOL: fno_ban_list
    DESCRIPTION:
        Stocks under F&O ban period.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Ban list
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_sec_ban("17-10-2025")
    return df_to_json(get.fno_eod_sec_ban(date))


@mcp.tool()
def fno_mwpl_data(date: str):
    """
    TOOL: fno_mwpl_data
    DESCRIPTION:
        Market Wide Position Limits (MWPL) and usage %.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        MWPL report
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_mwpl_3("17-10-2025")
    return df_to_json(get.fno_eod_mwpl_3(date))


@mcp.tool()
def fno_combined_oi(date: str):
    """
    TOOL: fno_combined_oi
    DESCRIPTION:
        Combined futures & options open interest.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        OI snapshot
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_combine_oi("17-10-2025")
    return df_to_json(get.fno_eod_combine_oi(date))


@mcp.tool()
def fno_participant_wise_oi(date: str):
    """
    TOOL: fno_participant_wise_oi
    DESCRIPTION:
        FII, DII, Pro, Client wise open interest.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Participant OI
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_participant_wise_oi("17-10-2025")
    return df_to_json(get.fno_eod_participant_wise_oi(date))


@mcp.tool()
def fno_participant_wise_volume(date: str):
    """
    TOOL: fno_participant_wise_volume
    DESCRIPTION:
        FII, DII, Pro, Client wise trading volume in F&O.
    PARAMETERS:
        date: str – "DD-MM-YYYY"    (Note: if user no date given, last trading date is used. if date given, used user date.)
    RETURNS:
        Volume breakdown
    CATEGORY:
        FnO_EOD
    """
    rate_limit()
    # Original: get.fno_eod_participant_wise_vol("17-10-2025")
    return df_to_json(get.fno_eod_participant_wise_vol(date))


@mcp.tool()
def futures_price_history(symbol: str, type_: str, expiry: str = None, from_date: str = None, to_date: str = None, period: str = None):
    """
    TOOL: futures_price_history
    DESCRIPTION:
        Historical futures price, volume, OI.
    PARAMETERS:
        symbol: str – "NIFTY", "RELIANCE"
        type_: str – "Index Futures", "Stock Futures"
        expiry: str – "OCT-25", "28-Nov-2025"
        period: str – "1M", "3M", "1Y"
        from_date/to_date: str
    RETURNS:
        Futures time series
    CATEGORY:
        FnO_Historical
    """
    rate_limit()
    # Original: get.future_price_volume_data(...)
    return df_to_json(get.future_price_volume_data(symbol, type_, expiry or period, from_date, to_date))


@mcp.tool()
def options_price_history(symbol: str, type_: str, strike: str = None, from_date: str = None, to_date: str = None, expiry: str = None, period: str = None):
    """
    TOOL: options_price_history
    DESCRIPTION:
        Historical options price, volume, OI, IV.
    PARAMETERS:
        symbol: str – "NIFTY", "ITC"
        type_: str – "Index Options", "Stock Options"
        strike: str – "47000", "CE", "PE"
        expiry: str – "28-10-2025"
        period: str – "3M", "1Y"
    RETURNS:
        Options time series
    CATEGORY:
        FnO_Historical
    """
    rate_limit()
    # Original: get.option_price_volume_data(...)
    return df_to_json(get.option_price_volume_data(symbol, type_, strike, from_date, to_date, expiry=expiry or period))


@mcp.tool()
def fno_lot_sizes(symbol: str = None):
    """
    TOOL: fno_lot_sizes
    DESCRIPTION:
        Current F&O lot sizes (all or specific symbol).
    PARAMETERS:
        symbol: str – Optional, e.g., "TCS"
    RETURNS:
        Lot size data
    CATEGORY:
        FnO_Reference
    """
    rate_limit()
    # Original: get.fno_eom_lot_size("TCS")
    return df_to_json(get.fno_eom_lot_size(symbol))


@mcp.tool()
def fno_business_growth(mode: str = "monthly", month: str = None, year: int = None):
    """
    TOOL: fno_business_growth
    DESCRIPTION:
        F&O segment daily/monthly/yearly turnover growth.
    PARAMETERS:
        mode: str – "daily", "monthly", "yearly"
        month: str – "OCT", "JAN" etc.
        year: int – e.g., 2025
    RETURNS:
        F&O growth data
    CATEGORY:
        FnO_Stats
    """
    rate_limit()
    # Original: get.fno_dmy_biz_growth(...)
    return df_to_json(get.fno_dmy_biz_growth(mode, month=month, year=year))


@mcp.tool()
def fno_settlement_report(period: str = None, from_year: str = None, to_year: str = None):
    """
    TOOL: fno_settlement_report
    DESCRIPTION:
        NSE Monthly Settlement Statistics (F&O) for given financial years or period.
    PARAMETERS:
        period: str – "1Y", "3Y" or None (current FY)
        from_year/to_year: int – e.g., 2024, 2026   (optional)
    RETURNS:
        F&O settlement data
    CATEGORY:
        FnO_Stats
    """
    rate_limit()
    # Original: get.fno_monthly_settlement_report(...)
    return df_to_json(get.fno_monthly_settlement_report(period=period, from_year=from_year, to_year=to_year))


# =====================================================================
#                         SEBI DATA
# =====================================================================

@mcp.tool()
def sebi_circulars(from_date: str = None, to_date: str = None, period: str = None):
    """
    TOOL: sebi_circulars
    DESCRIPTION:
        Latest or historical SEBI circulars.
    PARAMETERS:
        from_date/to_date: str – "DD-MM-YYYY"
        period: str – "1W", "1M", "3M", "1Y"
    RETURNS:
        List of circulars with links
    CATEGORY:
        Regulatory
    """
    rate_limit()
    # Original: get.sebi_circulars(...)
    return df_to_json(get.sebi_circulars(period or from_date, to_date))


@mcp.tool()
def sebi_data_pages(page: int = 1):
    """
    TOOL: sebi_data_pages
    DESCRIPTION:
        Paginated SEBI circulars and orders.
    PARAMETERS:
        page: int – Page number
    RETURNS:
        Circulars for given page
    CATEGORY:
        Regulatory
    """
    rate_limit()
    # Original: get.sebi_data()
    return df_to_json(get.sebi_data(page))


@mcp.tool()
def price_chart_index(index: str = "NIFTY 50", timeframe: str = "1D"):
    """
    TOOL: price_chart_index

    DESCRIPTION:
        Retrieves intraday or historical price chart data for the NIFTY Indices 
        based on the selected timeframe.  
        The tool internally connects to the NSE Next-API `getIndexChart` endpoint,
        handles cookie/session rotation automatically, and normalizes the response 
        into a clean DataFrame before converting it to JSON.

    PARAMETERS:
        index: str – e.g. "NIFTY 50", "SECURITIES IN F&O"(F&O stocks)
            "NIFTY AUTO", 
            "NIFTY CHEMICALS",
            "NIFTY CONSUMER DURABLES",
            "NIFTY FINANCIAL SERVICES EX-BANK",
            "NIFTY FINANCIAL SERVICES 25/50",
            "NIFTY FMCG",
            "NIFTY HEALTHCARE INDEX",
            "NIFTY IT",
            "NIFTY MEDIA",
            "NIFTY METAL",
            "NIFTY MIDSMALL HEALTHCARE",
            "NIFTY MIDSMALL FINANCIAL SERVICES",
            "NIFTY MIDSMALL IT & TELECOM",
            "NIFTY OIL & GAS",
            "NIFTY PHARMA",
            "NIFTY PSU BANK",
            "NIFTY PRIVATE BANK",
            "NIFTY REALTY",
            "NIFTY500 HEALTHCARE"  (for more index use list_of_indices() tool)
        timeframe (str):
            Defines the chart duration or lookback period.
            Examples:
                "1D" – 1-day intraday chart 
                "1M" – 1-month chart  
                "3M" – 3-month chart  
                "6M" – 6-month chart  
                "1Y" – 1-year historical chart  
            note: The NSE server will return only the valid supported timeframes.

    RETURNS:
        JSON chart data containing:
            - datetime_utc (string): Timestamp in UTC formatted as "%Y-%m-%d %H:%M:%S"
            - price (float): Index price at that timestamp
            - flag (string): Event marker provided by NSE (e.g., "PO"- Pre Open Market, "NM"- Normal Market, etc.) 

    CATEGORY:
        ChartData
        (All market chart–related tools fall under this category.)
    """
    rate_limit()
    return df_to_json(get.index_chart(index, timeframe))


@mcp.tool()
def price_chart_stock(symbol: str, timeframe: str = "1D"):
    """
    TOOL: price_chart_stock

    DESCRIPTION:
        Retrieves intraday or historical price chart data for the stock 
        based on the selected timeframe.  
        The tool internally connects to the NSE Next-API `getGraphChart` endpoint,
        handles cookie/session rotation automatically, and normalizes the response 
        into a clean DataFrame before converting it to JSON.

    PARAMETERS:
        timeframe (str):
            Defines the chart duration or lookback period.
            Examples:
                "1D" – 1-day intraday chart 
                "1W" – 1-week chart 
                "1M" – 1-month chart  
                "1Y" – 1-year historical chart  
            note: The NSE server will return only the valid supported timeframes.

    RETURNS:
        JSON chart data containing:
            - datetime_utc (string): Timestamp in UTC formatted as "%Y-%m-%d %H:%M:%S"
            - price (float): stock price at that timestamp
            - flag (string): Event marker provided by NSE (e.g., "PO"- Pre Open Market, "NM"- Normal Market, etc.) 

    CATEGORY:
        ChartData
        (All market chart–related tools fall under this category.)
    """
    rate_limit()
    return df_to_json(get.stock_chart(symbol, timeframe))


@mcp.tool()
def fno_intraday_chart(symbol: str, inst_type: str, expiry: str, strike: str = ""):
    """
    TOOL: fno_intraday_chart

    DESCRIPTION:
        Retrieves intraday chart data for the futures/options contracts (Stock + Index).
        Examples:
            get.fno_chart("TCS", "FUTSTK","30-12-2025")
            get.fno_chart("NIFTY", "OPTIDX","20-01-2026","PE25700")

    PARAMETERS:
        symbol   : Stock or Index
        inst_type: FUTSTK, OPTSTK, FUTIDX, OPTIDX   (FUTSTK-Stock Futures, OPTSTK-Stock Options, FUTIDX-Index Futures, OPTIDX-Index Options)
        expiry   : DD-MM-YYYY (use fno_expiry_dates_and_strikePrice to find available expiry & strike Price but expiry date must be (DD-MM-YYYY) this format only)
        strike   : CE/PE + price (options need CE/PE)

    RETURNS:
        JSON chart data containing:
            - datetime_utc (string): Timestamp in UTC formatted as "%Y-%m-%d %H:%M:%S"
            - price (float): stock price at that timestamp

    CATEGORY:
        ChartData
        (All market chart–related tools fall under this category.)
    """
    rate_limit()
    return df_to_json(get.fno_chart(symbol, inst_type, expiry, strike))


@mcp.tool()
def price_chart_india_vix():
    """
    TOOL: price_chart_india_vix

    DESCRIPTION:
        Retrieves intraday chart data for the India VIX Index.

    RETURNS:
        JSON chart data containing:
            - datetime_utc (string): Timestamp in UTC formatted as "%Y-%m-%d %H:%M:%S"
            - price (float): India VIX Index at that timestamp
            - flag (string): Event marker provided by NSE (e.g., "PO"- Pre Open Market, "NM"- Normal Market, etc.) 

    CATEGORY:
        ChartData (India Volatility Index = India VIX)
    """
    rate_limit()
    return df_to_json(get.india_vix_chart())


@mcp.tool()
def symbol_full_fno_live_data(symbol: str):
    """
    TOOL: symbol_full_fno_live_data
    DESCRIPTION:
        Fetches complete live FnO data for the specified stock or index.
        Includes all available Futures & Options contracts, identifiers,
        last traded price, volume, open interest, and other key market metrics.

    PARAMETERS:
        symbol: str – Example: "NIFTY", "BANKNIFTY", "RELIANCE", "TCS", etc.

    RETURNS:
        Dict containing full live FnO chain with identifiers for all
        Futures and Options contracts.

    CATEGORY:
        symbol_fno_live_data
    """
    rate_limit()
    return get.symbol_full_fno_live_data(symbol)


@mcp.tool()
def symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI(symbol: str, type_mode: str):
    """
    TOOL: symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI
    DESCRIPTION:
        Fetches the Top 5 Most Active CALLS, PUTS, or CONTRACTS based on Open Interest
        for a specific stock or index.

    PARAMETERS:
        symbol: str – Example: "NIFTY", "RELIANCE"
        type_mode: str – Allowed:
            "CALLS"      → Most Active Call Options by OI
            "PUTS"       → Most Active Put Options by OI
            "CONTRACTS"  → Most Active Combined Contracts by OI

    RETURNS:
        List / dict of the Top 5 most active FnO contracts based on Open Interest.

    CATEGORY:
        symbol_fno_live_data
    """
    rate_limit()
    return get.symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI(symbol, type_mode)


@mcp.tool()
def price_chart_fno_contracts(identifier: str):
    """
    TOOL: price_chart_fno_contracts
    DESCRIPTION:
        Fetches intraday price chart data (timestamp, price, flag)
        for a specific Futures or Options contract using its NSE identifier.

    PARAMETERS:
        identifier: str – Examples:
            "OPTSTKTCS30-12-2025CE3300.00"
            "FUTSTKTCS30-12-2025XX0.00"
            "FUTIDXNIFTY30-12-2025XX0.00"
            "OPTIDXNIFTY09-12-2025PE25800.00"

        (To find valid identifiers, use:
            symbol_full_fno_live_data
            symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI
        )

    RETURNS:
        Intraday price chart data for the specific FnO contract.

    CATEGORY:
        symbol_fno_live_data
    """
    rate_limit()
    return get.identifier_based_fno_contracts_live_chart_data(identifier)


@mcp.tool()
def investors_statewise():
    """
    TOOL: investors_statewise
    DESCRIPTION:
        Fetches NSE Registered Investors by State.(AS ON DATE, PREVIOUS CALENDAR DAY, PREVIOUS MONTH, PREVIOUS QUARTER, LAST YEAR, LAST 5 YEARS)
    PARAMETERS:
        None
    RETURNS:
        Registered Investors by State.
    CATEGORY:
        registered_investors
    """
    rate_limit()
    return get.state_wise_registered_investors()


@mcp.tool()
def quarterly_financial_results(symbol: str):
    """
    TOOL: quarterly_financial_results
    DESCRIPTION:
        Quarterly Results (Total Income, Profit Before Tax, Net Profit/ Loss, EARNINGS PER SHARE(Rs))  Note: all Amount in (Lakhs) so cores convert
    PARAMETERS:
        symbol: str – Example: "TCS"
    RETURNS:
        Quarterly Results.
    CATEGORY:
        quarterly_financial_result
    """
    rate_limit()
    return get.quarterly_financial_results(symbol)


@mcp.tool()
def quarterly_financial_results_full_data(url: str):
    """
    TOOL: quarterly_financial_results_full_data
    DESCRIPTION:
        Quarterly Results (Total Income, Profit Before Tax, Net Profit/ Loss, EARNINGS PER SHARE(Rs))  Note: all Amount in (Lakhs) so cores convert
    PARAMETERS:
        symbol: str – Example: "TCS"
    RETURNS:
        Quarterly Results.
    CATEGORY:
        quarterly_financial_result
    """
    rate_limit()
    return get.html_tables(url)
    # return df_to_json(get.html_tables(url))



# @mcp.prompt()
# def pre_market_analysis() -> str:
#     """
#     PROMPT: pre_market_analysis
#     PURPOSE:
#         Guide the AI to generate a structured NSE pre-market report
#         using NseKit-MCP tools.
#     """
#     return """
# You are a professional Indian stock market analyst.

# Generate a PRE-MARKET NSE report.

# Steps:
# 1. Check if market is open today.
# 2. Fetch Gift Nifty trend.
# 3. Analyze pre-open market breadth.
# 4. Identify gap-up and gap-down Nifty50 & F&O stocks.
# 5. Highlight NIFTY 50 & BANKNIFTY pre-open sentiment.

# Output Format:
# - Market Status
# - Global / Gift Nifty Cues
# - Market Breadth
# - Key Movers
# - Intraday Bias
# - Risk Notes
# """

@mcp.prompt()
def pre_market_analysis() -> str:
    """Generate NSE pre-market analysis prompt"""
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
        "- Do not assume prices or direction\n"
    )

@mcp.prompt()
def market_overview() -> str:
    """Get comprehensive market overview"""
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
    """Analyze option chain for given symbol"""
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
        "Symbol will be provided by user (e.g., NIFTY, RELIANCE)"
        "Present in a clean, organized format."
    )

@mcp.prompt()
def stock_deep_dive() -> str:
    """Perform deep analysis of a stock"""
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
        "Stock symbol will be provided by user."
        "Present in a clean, organized format."
    )

@mcp.prompt()
def fno_expiry_analysis() -> str:
    """Analyze F&O positions before expiry"""
    return (
        "Generate F&O EXPIRY DAY analysis:\n\n"
        "1. Check if today is an expiry day\n"
        "2. Get most active options by OI and volume\n"
        "3. Analyze max pain levels for Nifty and BankNifty\n"
        "4. Review F&O ban stocks\n"
        "5. Check participant-wise OI (FII/DII positioning)\n"
        "6. Identify key support and resistance from OI\n"
        "7. Provide expiry day strategy notes\n\n"
        "Focus on: NIFTY, BANKNIFTY, and top F&O stocks"
        "Present in a clean, organized format."
    )

@mcp.prompt()
def market_sentiment() -> str:
    """Gauge overall market sentiment"""
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
        "Include confidence level and key factors."
        "Present in a clean, organized format."
    )

@mcp.prompt()
def daily_market_wrap() -> str:
    """Generate end-of-day market summary"""
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


# @mcp.prompt()
# def my_intraday_stock_selection() -> str:
#     """
#     Primary MCP scanner to identify high-probability NSE intraday trade setups
#     using market regime, liquidity, institutional activity, price structure,
#     and F&O confirmation with strict risk controls.
#     """
#     return (
#         "You are a professional Indian stock market analyst operating an intraday trading desk. "
#         "Your task is to identify high-probability intraday trade setups using ONLY NseKit-MCP tools "
#         "and real-time NSE data, without assumptions.\n\n"

#         "=============================\n"
#         "PROMPT 1: MARKET REGIME & RISK FILTER\n"
#         "=============================\n"
#         "Use:\n"
#         "- market_live_status\n"
#         "- india_vix\n"
#         "- gift_nifty_live\n"
#         "- market_advances_declines\n\n"
#         "Objective:\n"
#         "Determine the current intraday market regime:\n"
#         "1) Trending\n"
#         "2) Range-bound\n"
#         "3) High-volatility risk-off\n\n"
#         "Output:\n"
#         "- Market Bias (Bullish / Bearish / Neutral)\n"
#         "- Volatility Condition (Low / Normal / High)\n"
#         "- Allowed Trading Style (Scalp / Momentum / Avoid)\n\n"
#         "Risk Rules:\n"
#         "- Rising VIX with skewed advances/declines → reduce position size\n"
#         "- Flat GIFT NIFTY with low VIX → prefer range-bound strategies\n\n"

#         "=============================\n"
#         "PROMPT 2: HIGH LIQUIDITY INTRADAY STOCK SELECTION\n"
#         "=============================\n"
#         "Use:\n"
#         "- most_active_equities\n"
#         "- equity_volume_surge\n"
#         "- market_live_turnover\n\n"
#         "Objective:\n"
#         "Identify the top 20 intraday tradable stocks where:\n"
#         "- Volume expansion is greater than recent averages\n"
#         "- Turnover concentration is high\n"
#         "- Liquidity is suitable for intraday execution\n\n"
#         "Output:\n"
#         "Rank stocks based on:\n"
#         "1) Volume Surge\n"
#         "2) Turnover\n"
#         "3) Liquidity Score\n\n"

#         "=============================\n"
#         "PROMPT 3: INSTITUTIONAL FOOTPRINT (CASH MARKET)\n"
#         "=============================\n"
#         "Use:\n"
#         "- equity_block_deals_live\n"
#         "- equity_bulk_deals_live\n"
#         "- fii_dii_activity\n\n"
#         "Objective:\n"
#         "Detect institutional participation by identifying:\n"
#         "- Same-day block or bulk deal activity\n"
#         "- Alignment with FII directional bias\n\n"
#         "Output:\n"
#         "Classify stocks as:\n"
#         "- Accumulation\n"
#         "- Distribution\n"
#         "- Noise\n\n"
#         "Rule:\n"
#         "- Avoid retail-only volume spikes without institutional support\n\n"

#         "=============================\n"
#         "PROMPT 4: PRICE STRUCTURE & INTRADAY LEVELS\n"
#         "=============================\n"
#         "Use:\n"
#         "- equity_live_stock_quote\n"
#         "- price_chart_stock\n"
#         "- equity_52week_high_live\n"
#         "- equity_52week_low_live\n\n"
#         "Objective:\n"
#         "Analyze intraday price behavior to identify:\n"
#         "- Opening range breakout or breakdown candidates\n"
#         "- VWAP hold or rejection zones\n"
#         "- Pressure near day high or day low\n\n"
#         "Output:\n"
#         "- Trend Bias (Up / Down / Range)\n"
#         "- Key Levels (VWAP, Day High, Day Low)\n\n"

#         "=============================\n"
#         "PROMPT 5: FUTURES STRENGTH CONFIRMATION (OPTIONAL)\n"
#         "=============================\n"
#         "Use:\n"
#         "- fno_live_futures_data\n"
#         "- fno_live_change_in_oi\n"
#         "- fno_participant_wise_oi\n\n"
#         "Objective:\n"
#         "Confirm directional strength using price and open interest behavior:\n"
#         "- Price up + OI up → Long buildup\n"
#         "- Price down + OI up → Short buildup\n\n"
#         "Output:\n"
#         "- Directional Conviction Score (0–10)\n\n"

#         "=============================\n"
#         "PROMPT 6: OPTION CHAIN BIAS (ATM FOCUS)\n"
#         "=============================\n"
#         "Use:\n"
#         "- fno_live_option_chain\n"
#         "- fno_live_most_active_contracts_by_oi\n"
#         "- symbol_specific_most_active_Calls_or_Puts_or_Contracts_by_OI\n\n"
#         "Objective:\n"
#         "Identify options market bias by detecting:\n"
#         "- ATM Put writing (Bullish bias)\n"
#         "- ATM Call writing (Bearish bias)\n"
#         "- Long gamma traps via price and OI divergence\n\n"
#         "Output:\n"
#         "- Option Bias (Bullish / Bearish / Neutral)\n"
#         "- Trap Warning if OI and price diverge\n\n"

#         "=============================\n"
#         "PROMPT 7: HIGH PROBABILITY TRADE QUALIFIER\n"
#         "=============================\n"
#         "Input:\n"
#         "Outputs from Prompts 1 through 6\n\n"
#         "Qualification Conditions:\n"
#         "- Volume expansion present\n"
#         "- Institutional alignment confirmed\n"
#         "- Price holding above or below VWAP\n"
#         "- F&O confirmation (if available)\n"
#         "- Alignment with overall market regime\n\n"
#         "Output:\n"
#         "- Trade Decision (TRADE / NO TRADE)\n"
#         "- Direction (Long / Short)\n"
#         "- Confidence Score (%)\n\n"

#         "=============================\n"
#         "PROMPT 8: EXECUTION & RISK MANAGEMENT PLAN\n"
#         "=============================\n"
#         "Use:\n"
#         "- equity_live_stock_quote\n\n"
#         "Objective:\n"
#         "Define a disciplined intraday trade plan with controlled risk:\n"
#         "- Entry trigger based on price confirmation\n"
#         "- Technical stop-loss (not fixed points)\n"
#         "- Target ensuring minimum Risk:Reward of 1:1.5\n\n"
#         "Output:\n"
#         "- Exact Entry Price\n"
#         "- Stop-Loss Level\n"
#         "- Target Level\n"
#         "- Position Sizing Suggestion\n"
#         "- Maximum Loss Per Trade\n\n"

#         "Strict Rules:\n"
#         "- Use ONLY NseKit-MCP tools\n"
#         "- Do NOT assume market direction or outcomes\n"
#         "- No trade recommendations without confirmation\n"
#         "- Capital preservation is mandatory\n"
#     )

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
    mcp.run(transport="stdio")  # No 'port' arg — uses default (http://127.0.0.1:8000 for HTTP)