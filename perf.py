import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Function to get the historical stock prices for the past year
def get_stock_data(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # One year ago
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)  # Fetch data for the past year
    return stock_data

# Function to calculate CAGR
def calculate_cagr(initial_value, final_value, years):
    if initial_value <= 0 or years <= 0:
        return 0
    return ((final_value / initial_value) ** (1 / years) - 1) * 100  # Return CAGR as a percentage

# Function to plot the stock prices
def plot_stock_performance(stock_data, ticker, final_price, daily_change_percentage):
    plt.figure(figsize=(10, 6))
    
    # Determine the color of the line based on the trend
    if stock_data['Close'].iloc[-1] > stock_data['Close'].iloc[0]:
        line_color = 'green'  # Positive trend
    else:
        line_color = 'red'    # Negative trend

    plt.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Closing Price', color=line_color)
    plt.title(f'{ticker} Stock Performance Over the Past Year')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.legend()
    
    # Display the current price and daily change percentage below the graph
    plt.text(0.5, -0.15, f'Price: ${final_price:.2f}, {"up" if daily_change_percentage >= 0 else "down"} {abs(daily_change_percentage):.2f}% today', 
             fontsize=20, fontweight='bold', ha='center', transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.show()

# Main script
def main():
    ticker = input("Enter the stock ticker: ").strip().upper()  # Get the stock ticker from the user
    stock_data = get_stock_data(ticker)  # Fetch stock data

    if stock_data.empty:
        print(f"No data found for ticker: {ticker}. Please check the ticker symbol.")
        return

    # Calculate performance of one share
    initial_price = stock_data['Close'].iloc[0]
    final_price = stock_data['Close'].iloc[-1]
    performance = final_price - initial_price
    performance_percentage = (performance / initial_price) * 100

    # Calculate daily change percentage
    if len(stock_data) > 1:
        previous_close = stock_data['Close'].iloc[-2]
        daily_change_percentage = ((final_price - previous_close) / previous_close) * 100
    else:
        daily_change_percentage = 0  # Not enough data to calculate daily change

    # Calculate CAGR
    years = 1  # Since we are looking at a one-year period
    cagr = calculate_cagr(initial_price, final_price, years)

    print(f"\nPerformance of one share of {ticker} over the past year:")
    print(f"Initial Price: ${initial_price:.2f}")
    print(f"Final Price: ${final_price:.2f}")
    print(f"Gain/Loss: ${performance:.2f} ({performance_percentage:.2f}%)")
    print(f"CAGR: {cagr:.2f}%")

    # Plot the stock performance
    plot_stock_performance(stock_data, ticker, final_price, daily_change_percentage)

# Run the main function
if __name__ == "__main__":
    main()
