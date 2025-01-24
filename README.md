Stock Portfolio Tracker
This Python script allows you to track a portfolio of stocks, calculate various statistics, and visualize the portfolio's performance over time. It fetches historical stock data from Yahoo Finance using the yfinance package and provides insights like weighted dividend yield, CAGR (Compound Annual Growth Rate), positive periods ratio, gain/loss ratio, and more.

##Key Features:
Historical Stock Data: Fetches stock prices and other relevant data for the stocks you are tracking.
Portfolio Analysis: Computes and displays portfolio statistics like:

Weighted Dividend Yield
Weighted Beta (relative to SPY)
CAGR (Compound Annual Growth Rate)
Positive Periods Ratio (percentage of positive return days)
Gain/Loss Ratio (average gain vs. average loss)
Visualization: Plots stock prices and portfolio value over time.
Requirements:
Python 3.x
Libraries:
yfinance
matplotlib
pandas
numpy

You can install the required libraries using the following command:
pip install yfinance matplotlib pandas numpy

##Usage:
Run the script.
The script will prompt you to input the start date for your investment (in DDMMYYYY format).
Specify the number of stocks in your portfolio, their tickers, and the respective weightings (ensure the sum of weightings is 1).
Input your total investment amount.
The script will fetch data for the stocks and calculate the statistics.
The portfolio performance, including a graph and a table with the calculated statistics, will be displayed.
Disclaimer:
This script is not financial advice. It uses historical stock data and basic statistical calculations to provide insights into portfolio performance. The results may not be accurate or reflect the actual future performance of the stocks or portfolio. Always consult a financial professional before making investment decisions. The figures returned by this script may be incorrect or misleading, and should not be used as the sole basis for financial decisions.

Example Output:
Weighted Dividend Yield: 2.56%
Weighted Beta (Relative to SPY): 1.12
CAGR: 8.5%
Positive Periods Ratio: 0.65
Gain/Loss Ratio: 1.5
A plot of stock prices and portfolio value will also be generate
