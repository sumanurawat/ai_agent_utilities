import matplotlib.pyplot as plt

def plot_stock_prices(dates, prices):
    """
    Plot stock prices over time.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker="o", linestyle="-", color="b")
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($)")
    plt.title("Stock Price Trend")
    plt.grid()
    plt.show()

# Example usage with dummy data
if __name__ == "__main__":
    dates = ["2024-03-01", "2024-03-02", "2024-03-03"]
    prices = [150, 152, 148]
    plot_stock_prices(dates, prices)