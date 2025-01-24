#pip install yfinance matplotlib

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from datetime import datetime
import numpy as np

# Function to get the historical stock prices for the custom start date to present
def get_stock_data(ticker, start_date):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date)  # Fetch data from the start date to present
    stock_info = stock.info  # Get stock's detailed information (stats)
    return stock_data, stock_info

# Function to calculate the weighted average of a list of values
def weighted_average(values, weights):
    return sum(v * w for v, w in zip(values, weights))

# Function to calculate the daily returns for each stock and the portfolio
def calculate_returns(stock_data_dict, tickers, weightings):
    portfolio_returns = pd.Series(index=stock_data_dict[tickers[0]].index, data=0.0)
    
    for ticker in tickers:
        stock_data = stock_data_dict[ticker]
        # Calculate the daily returns
        stock_data['Daily Return'] = stock_data['Close'].pct_change()
        
        # Add the weighted returns to the portfolio
        weighted_returns = stock_data['Daily Return'] * weightings[tickers.index(ticker)]
        portfolio_returns += weighted_returns
    
    # Drop the first NaN value after pct_change
    portfolio_returns = portfolio_returns.dropna()
    
    return portfolio_returns

# Function to calculate the weighted dividend yield
def calculate_weighted_dividend_yield(tickers, weightings, stock_info_dict):
    dividend_yields = []
    for ticker in tickers:
        stock_info = stock_info_dict[ticker]
        # Fetch dividend yield from the stock_info dictionary
        dividend_yield = stock_info.get('yield', None)  # None if missing
        
        # If dividend yield is None or 0, we should check further or handle it
        if dividend_yield is None or dividend_yield == 0:
            print(f"Dividend Yield for {ticker} is missing or zero. Please check manually.")
            dividend_yield = 0  # Assign 0 or try alternative methods if needed

        # Convert to percentage if the value exists
        dividend_yields.append(dividend_yield * 100 if dividend_yield else 0)  # Make sure to handle None or missing
        
    return weighted_average(dividend_yields, weightings)

# Function to calculate the weighted Beta (relative to SPY)
def calculate_weighted_beta(tickers, weightings, stock_data_dict):
    market_data = stock_data_dict["SPY"]  # SPY is used as the benchmark (S&P 500)
    market_returns = market_data['Close'].pct_change().dropna()  # Calculate market returns
    
    betas = []
    for ticker in tickers:
        if ticker != "SPY":  # Skip SPY for individual stock beta calculation
            stock_data = stock_data_dict[ticker]
            stock_returns = stock_data['Close'].pct_change().dropna()  # Calculate stock returns

            # Align the stock and market data (date-wise) for correlation
            aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
            stock_returns_aligned = aligned_data.iloc[:, 0]
            market_returns_aligned = aligned_data.iloc[:, 1]
            
            # Calculate Beta using covariance/variance
            covariance = np.cov(stock_returns_aligned, market_returns_aligned)[0, 1]
            market_variance = np.var(market_returns_aligned)
            beta = covariance / market_variance
            betas.append(beta)
        else:
            betas.append(1)  # For SPY, Beta is 1 by definition (relative to itself)
    
    return weighted_average(betas, weightings)

# Function to calculate positive periods ratio (positive / positive + negative)
def calculate_positive_periods_ratio(portfolio_returns):
    positive_periods = (portfolio_returns > 0).sum()
    total_periods = len(portfolio_returns)
    if total_periods > 0:
        return positive_periods / total_periods
    else:
        return 0  # Return 0 if there are no periods

# Function to calculate Gain/Loss Ratio
def calculate_gain_loss_ratio(portfolio_returns):
    gains = portfolio_returns[portfolio_returns > 0].mean()
    losses = portfolio_returns[portfolio_returns < 0].mean()
    if losses != 0:
        return gains / abs(losses)
    else:
        return float('inf')  # Return infinity if no losses

# Function to calculate CAGR (Compound Annual Growth Rate)
def calculate_cagr(portfolio_value, start_date):
    start_value = portfolio_value.iloc[0]
    end_value = portfolio_value.iloc[-1]
    years = (portfolio_value.index[-1] - portfolio_value.index[0]).days / 365.25
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr * 100  # Convert to percentage

# Function to plot the stock prices and portfolio value
def plot_stock_prices(stock_data_dict, tickers, weightings, investment_amount, num_stocks):
    weighted_avg_prices = pd.DataFrame()
    portfolio_value = pd.Series(index=stock_data_dict[tickers[0]].index, data=0.0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for ticker in tickers:
        stock_data = stock_data_dict[ticker]
        ax.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Closing Price')
        
        if num_stocks > 1 and weighted_avg_prices.empty:
            weighted_avg_prices = stock_data[['Close']] * weightings[tickers.index(ticker)]
        elif num_stocks > 1:
            weighted_avg_prices += stock_data[['Close']] * weightings[tickers.index(ticker)]
        
        stock_value = stock_data['Close'] * (weightings[tickers.index(ticker)] * investment_amount) / stock_data['Close'].iloc[0]
        portfolio_value += stock_value

    if num_stocks > 1:
        ax.plot(weighted_avg_prices.index, weighted_avg_prices['Close'], label="Weighted Average Price", color='black', linestyle='--', linewidth=2)

    ax.plot(portfolio_value.index, portfolio_value, label="Portfolio Value", color='green', linestyle='-', linewidth=2)

    #ax.set_title('Stock Prices and Portfolio Value Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Portfolio Value (USD)')
    ax.grid(True)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    ax.legend()

    plt.subplots_adjust(left=0.1, bottom=0.4,)
    
    return fig, ax, portfolio_value

# Function to display the statistics in the matplotlib table
def display_weighted_stats_table(ax, weighted_stats):
    table_data = [
        ["Weighted Dividend Yield", f"{weighted_stats['Weighted Dividend Yield']:.2f}%"],
        ["Weighted Beta (Relative to SPY)", f"{weighted_stats['Weighted Beta (Relative to SPY)']:.2f}"],
        ["Positive Periods", f"{weighted_stats['Positive Periods']:.2f}"],
        ["Gain/Loss Ratio", f"{weighted_stats['Gain/Loss Ratio']:.2f}"],
        ["CAGR (Compound Annual Growth Rate)", f"{weighted_stats['CAGR']:.2f}%"],
    ]
    
    table = ax.table(cellText=table_data, colLabels=["Statistic", "Value"], loc="top", cellLoc='center', colColours=[mcolors.CSS4_COLORS['skyblue']] * 2)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

# Function to display portfolio value in the matplotlib table
def display_portfolio_value_table(ax, portfolio_value):
    sample_dates = portfolio_value.iloc[::len(portfolio_value)//5].dropna()
    table_data = [["Date", "Portfolio Value"]]
    for date, value in sample_dates.items():
        table_data.append([date.strftime('%Y-%m-%d'), f"${value:,.2f}"])

    table = ax.table(cellText=table_data, colLabels=["Date", "Portfolio Value"], loc="bottom", cellLoc='center', colColours=[mcolors.CSS4_COLORS['lightgreen']] * 2)
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)

# Main script
def main():
    start_date_str = input("Enter the start date of your investment (DDMMYYYY format, e.g., 02122024): ")
    
    try:
        start_date = datetime.strptime(start_date_str, "%d%m%Y").date()
    except ValueError:
        print("Invalid date format. Please use DDMMYYYY format.")
        return

    num_stocks = int(input("How many stocks are you tracking? "))

    tickers = []
    weightings = []

    if num_stocks == 1:
        ticker = input(f"Enter the ticker for your stock: ").strip()
        tickers.append(ticker)
        weightings.append(1)
    else:
        for i in range(num_stocks):
            ticker = input(f"Enter the ticker for stock {i+1}: ").strip()
            weighting = float(input(f"Enter the weighting (0 to 1) for {ticker}: ").strip())
            tickers.append(ticker)
            weightings.append(weighting)

    investment_amount = float(input("Enter your total investment amount (e.g., 10000, 1234.56): "))

    if num_stocks > 1 and sum(weightings) != 1:
        print("Warning: The sum of weightings is not equal to 1. Adjusting to sum to 1.")
        adjustment_factor = 1 / sum(weightings)
        weightings = [w * adjustment_factor for w in weightings]

    stock_data_dict = {}
    stock_info_dict = {}
    
    # Fetch SPY data (S&P 500 benchmark) as well for beta calculation
    stock_data_dict["SPY"], _ = get_stock_data("SPY", start_date)
    
    for ticker in tickers:
        print(f"\nFetching data for {ticker}")
        stock_data, stock_info = get_stock_data(ticker, start_date)
        stock_data_dict[ticker] = stock_data
        stock_info_dict[ticker] = stock_info

    portfolio_returns = calculate_returns(stock_data_dict, tickers, weightings)

    weighted_dividend_yield = calculate_weighted_dividend_yield(tickers, weightings, stock_info_dict)
    weighted_beta = calculate_weighted_beta(tickers, weightings, stock_data_dict)
    positive_periods_ratio = calculate_positive_periods_ratio(portfolio_returns)
    gain_loss_ratio = calculate_gain_loss_ratio(portfolio_returns)

    # Calculate the CAGR of the portfolio
    fig, ax, portfolio_value = plot_stock_prices(stock_data_dict, tickers, weightings, investment_amount, num_stocks)
    cagr = calculate_cagr(portfolio_value, start_date)

    weighted_stats = {
        "Weighted Dividend Yield": weighted_dividend_yield,
        "Weighted Beta (Relative to SPY)": weighted_beta,
        "Positive Periods": positive_periods_ratio,
        "Gain/Loss Ratio": gain_loss_ratio,
        "CAGR": cagr,
    }

    # Display the statistics table on the plot
    display_weighted_stats_table(ax, weighted_stats)
    
    # Display portfolio values in a separate table
    display_portfolio_value_table(ax, portfolio_value)

    plt.show()

# Run the main function
if __name__ == "__main__":
    main()
