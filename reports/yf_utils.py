import yfinance as yf
import datetime
import json 

def fetch_stock_data(ticker_symbol, start_date, end_date, interval="1d"):
    """
    Fetches historical stock data for a given ticker symbol within a specified date range and interval.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL", "MSFT").
        start_date (str): The start date in "YYYY-MM-DD" format.
        end_date (str): The end date in "YYYY-MM-DD" format.
        interval (str, optional):  The data interval.  Valid values are:
            "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo".
            Defaults to "1d" (daily).

    Returns:
        pandas.DataFrame: A DataFrame containing the historical stock data, or None if an error occurs.
            The DataFrame will have columns like 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'.
            The index will be the date/time.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None


def fetch_stock_news(ticker_symbol, limit=10):
    """
    Fetches news articles related to a given stock ticker symbol.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "AAPL", "MSFT").
        limit (int): maximum number of news to return

    Returns:
        list: A list of dictionaries, where each dictionary represents a news article.
              Each dictionary contains keys like 'uuid', 'title', 'publisher', 'link',
              'providerPublishTime' (timestamp), 'type'.  Returns an empty list if no news is found
              or an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        return news[:limit]  # Limit the number of news items
    except Exception as e:
        print(f"Error fetching news for {ticker_symbol}: {e}")
        return []

def get_ticker_info(ticker_symbol):
    """
    Retrieves various information about a ticker symbol using yfinance's Ticker object.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing various information about the ticker, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.info  # Access the 'info' attribute for a dictionary of information
    except Exception as e:
        print(f"Error getting info for {ticker_symbol}: {e}")
        return None

def get_recommendations(ticker_symbol):
    """
    Retrieves analyst recommendations for a given ticker symbol.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing analyst recommendations, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.recommendations
    except Exception as e:
        print(f"Error getting recommendations for {ticker_symbol}: {e}")
        return None

def get_major_holders(ticker_symbol):
    """
    Retrieves information about the major holders of a stock.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing information about major holders, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.major_holders
    except Exception as e:
        print(f"Error getting major holders for {ticker_symbol}: {e}")
        return None

def get_institutional_holders(ticker_symbol):
    """
    Retrieves information about institutional holders of a stock.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing information about institutional holders, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.institutional_holders
    except Exception as e:
        print(f"Error getting institutional holders for {ticker_symbol}: {e}")
        return None

def get_dividends(ticker_symbol):
    """
    Retrieves historical dividend data for a stock.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.Series: A Series containing dividend data, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.dividends
    except Exception as e:
        print(f"Error getting dividends for {ticker_symbol}: {e}")
        return None

def get_splits(ticker_symbol):
    """
    Retrieves historical stock split data.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.Series: A Series containing stock split data, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.splits
    except Exception as e:
        print(f"Error getting splits for {ticker_symbol}: {e}")
        return None

def get_actions(ticker_symbol):
    """
    Retrieves both dividends and splits.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing both dividends and splits, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.actions
    except Exception as e:
        print(f"Error getting actions for {ticker_symbol}: {e}")
        return None

def get_financials(ticker_symbol, frequency='yearly'):
    """
    Retrieves financial statements (yearly or quarterly).

    Args:
        ticker_symbol (str): The stock ticker symbol.
        frequency (str): 'yearly' or 'quarterly'. Defaults to 'yearly'.

    Returns:
        pandas.DataFrame: A DataFrame containing the financial statements, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        if frequency == 'yearly':
            return ticker.financials
        elif frequency == 'quarterly':
            return ticker.quarterly_financials
        else:
            print("Invalid frequency.  Must be 'yearly' or 'quarterly'.")
            return None
    except Exception as e:
        print(f"Error getting financials for {ticker_symbol}: {e}")
        return None

def get_balance_sheet(ticker_symbol, frequency='yearly'):
    """
    Retrieves balance sheet data (yearly or quarterly).

    Args:
        ticker_symbol (str): The stock ticker symbol.
        frequency (str): 'yearly' or 'quarterly'. Defaults to 'yearly'.

    Returns:
        pandas.DataFrame: A DataFrame containing the balance sheet data, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        if frequency == 'yearly':
            return ticker.balance_sheet
        elif frequency == 'quarterly':
            return ticker.quarterly_balance_sheet
        else:
            print("Invalid frequency.  Must be 'yearly' or 'quarterly'.")
            return None
    except Exception as e:
        print(f"Error getting balance sheet for {ticker_symbol}: {e}")
        return None

def get_cashflow(ticker_symbol, frequency='yearly'):
    """
    Retrieves cash flow statements (yearly or quarterly).

    Args:
        ticker_symbol (str): The stock ticker symbol.
        frequency (str): 'yearly' or 'quarterly'. Defaults to 'yearly'.

    Returns:
        pandas.DataFrame: A DataFrame containing the cash flow statements, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        if frequency == 'yearly':
            return ticker.cashflow
        elif frequency == 'quarterly':
            return ticker.quarterly_cashflow
        else:
            print("Invalid frequency.  Must be 'yearly' or 'quarterly'.")
            return None
    except Exception as e:
        print(f"Error getting cashflow for {ticker_symbol}: {e}")
        return None

def get_earnings(ticker_symbol, frequency='yearly'):
    """
    Retrieves earnings data (yearly or quarterly).

    Args:
        ticker_symbol (str): The stock ticker symbol.
        frequency (str): 'yearly' or 'quarterly'. Defaults to 'yearly'.

    Returns:
        pandas.DataFrame: A DataFrame containing the earnings data, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        if frequency == 'yearly':
            return ticker.earnings
        elif frequency == 'quarterly':
            return ticker.quarterly_earnings
        else:
            print("Invalid frequency.  Must be 'yearly' or 'quarterly'.")
            return None
    except Exception as e:
        print(f"Error getting earnings for {ticker_symbol}: {e}")
        return None

def get_sustainability(ticker_symbol):
    """
    Retrieves sustainability data.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing sustainability data, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.sustainability
    except Exception as e:
        print(f"Error getting sustainability data for {ticker_symbol}: {e}")
        return None

def get_calendar(ticker_symbol):
    """
    Retrieves calendar events (e.g., earnings dates).

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        pandas.DataFrame: A DataFrame containing calendar events, or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.calendar
    except Exception as e:
        print(f"Error getting calendar data for {ticker_symbol}: {e}")
        return None

def get_options(ticker_symbol):
    """
    Retrieves the available option expiration dates.

    Args:
        ticker_symbol (str): The stock ticker symbol.

    Returns:
        list: A list of available option expiration dates (as strings), or None if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        return ticker.options
    except Exception as e:
        print(f"Error getting options data for {ticker_symbol}: {e}")
        return None

def get_option_chain(ticker_symbol, expiration_date=None):
    """
    Retrieves the option chain for a given expiration date.

    Args:
        ticker_symbol (str): The stock ticker symbol.
        expiration_date (str, optional): The expiration date in 'YYYY-MM-DD' format.
            If None, defaults to the next available expiration date.

    Returns:
        tuple: A tuple containing two DataFrames: (calls, puts).  Returns (None, None) if an error occurs.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        if expiration_date is None:
            if not ticker.options:
                print(f"No options data available for {ticker_symbol}")
                return None, None
            expiration_date = ticker.options[0]  # Get the first available expiration date
        
        option_chain = ticker.option_chain(expiration_date)
        return option_chain.calls, option_chain.puts
    except Exception as e:
        print(f"Error getting option chain for {ticker_symbol} and expiration {expiration_date}: {e}")
        return None, None


def download_multiple_tickers(tickers, start_date, end_date, interval="1d"):
    """
    Downloads historical data for multiple tickers simultaneously.

    Args:
        tickers (list): A list of stock ticker symbols (e.g., ["AAPL", "MSFT", "GOOG"]).
        start_date (str): The start date in "YYYY-MM-DD" format.
        end_date (str): The end date in "YYYY-MM-DD" format.
        interval (str, optional): The data interval. Defaults to "1d".

    Returns:
        pandas.DataFrame: A DataFrame containing the historical data for all tickers.
            The DataFrame will have a MultiIndex for columns (Ticker, OHLCV).
            Returns None if an error occurs.
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        print(f"Error downloading data for multiple tickers: {e}")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    ticker = "AAPL"
    start = "2023-01-01"
    end = "2023-12-31"

    # Fetch historical data
    historical_data = fetch_stock_data(ticker, start, end, interval="1d")
    if historical_data is not None:
        print("\nHistorical Data:")
        print(historical_data.head())  # Show the first few rows
        print(historical_data.tail())  # Show the last few rows

    # Fetch news
    news_items = fetch_stock_news(ticker)
    if news_items:
        print("\nNews Items:")
        for item in news_items:
            print(json.dumps(item, indent=4))
  


            print("-" * 20)

    # Get ticker info
    ticker_info = get_ticker_info(ticker)
    if ticker_info:
        print("\nTicker Info:")
        print(f"  Company Name: {ticker_info.get('longName', 'N/A')}")  # Use .get() for safety
        print(f"  Sector: {ticker_info.get('sector', 'N/A')}")
        print(f"  Industry: {ticker_info.get('industry', 'N/A')}")
        print(f"  Website: {ticker_info.get('website', 'N/A')}")
        print(f"  Summary: {ticker_info.get('longBusinessSummary', 'N/A')}")


    # Get recommendations
    recommendations = get_recommendations(ticker)
    if recommendations is not None:
        print("\nRecommendations:")
        print(recommendations.tail())

    # Get major holders
    major_holders = get_major_holders(ticker)
    if major_holders is not None:
        print("\nMajor Holders:")
        print(major_holders)

    # Get institutional holders
    institutional_holders = get_institutional_holders(ticker)
    if institutional_holders is not None:
        print("\nInstitutional Holders:")
        print(institutional_holders.head())

    # Get dividends
    dividends = get_dividends(ticker)
    if dividends is not None:
        print("\nDividends:")
        print(dividends.tail())

    # Get splits
    splits = get_splits(ticker)
    if splits is not None:
        print("\nSplits:")
        print(splits)

    # Get actions (dividends and splits)
    actions = get_actions(ticker)
    if actions is not None:
        print("\nActions (Dividends and Splits):")
        print(actions.tail())

    # Get financials (yearly)
    financials_yearly = get_financials(ticker, frequency='yearly')
    if financials_yearly is not None:
        print("\nYearly Financials:")
        print(financials_yearly)

    # Get financials (quarterly)
    financials_quarterly = get_financials(ticker, frequency='quarterly')
    if financials_quarterly is not None:
        print("\nQuarterly Financials:")
        print(financials_quarterly)

    # Get balance sheet (yearly)
    balance_sheet_yearly = get_balance_sheet(ticker, frequency='yearly')
    if balance_sheet_yearly is not None:
        print("\nYearly Balance Sheet:")
        print(balance_sheet_yearly)

    # Get balance sheet (quarterly)
    balance_sheet_quarterly = get_balance_sheet(ticker, frequency='quarterly')
    if balance_sheet_quarterly is not None:
        print("\nQuarterly Balance Sheet:")
        print(balance_sheet_quarterly)

    # Get cashflow (yearly)
    cashflow_yearly = get_cashflow(ticker, frequency='yearly')
    if cashflow_yearly is not None:
        print("\nYearly Cashflow:")
        print(cashflow_yearly)

    # Get cashflow (quarterly)
    cashflow_quarterly = get_cashflow(ticker, frequency='quarterly')
    if cashflow_quarterly is not None:
        print("\nQuarterly Cashflow:")
        print(cashflow_quarterly)

    # Get earnings (yearly)
    earnings_yearly = get_earnings(ticker, frequency='yearly')
    if earnings_yearly is not None:
        print("\nYearly Earnings:")
        print(earnings_yearly)

    # Get earnings (quarterly)
    earnings_quarterly = get_earnings(ticker, frequency='quarterly')
    if earnings_quarterly is not None:
        print("\nQuarterly Earnings:")
        print(earnings_quarterly)

    # Get sustainability
    sustainability = get_sustainability(ticker)
    if sustainability is not None:
        print("\nSustainability:")
        print(sustainability)

    # Get calendar
    calendar_data = get_calendar(ticker)
    if calendar_data is not None:
        print("\nCalendar:")
        print(calendar_data)

    # Get options
    options = get_options(ticker)
    if options:
        print("\nOptions Expiration Dates:")
        print(options)

        # Get option chain for the first expiration date
        calls, puts = get_option_chain(ticker)  # Use default expiration
        if calls is not None and puts is not None:
            print("\nCalls (First Expiration):")
            print(calls.head())
            print("\nPuts (First Expiration):")
            print(puts.head())

    # Download multiple tickers
    multiple_tickers = ["AAPL", "MSFT", "GOOG"]
    multi_data = download_multiple_tickers(multiple_tickers, start, end)
    if multi_data is not None:
        print("\nMultiple Tickers Data:")
        print(multi_data.head())