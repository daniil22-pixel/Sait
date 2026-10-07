import pandas as pd
import numpy as np

def simulate_bitcoin_prices(days=60, initial_price=60000, volatility=0.05):
    """
    Simulate Bitcoin price data using Geometric Brownian Motion.
    """
    np.random.seed(42)  # For reproducibility
    prices = [initial_price]

    for _ in range(1, days):
        # Drift is set to 0 for simplicity, volatility is daily volatility
        drift = 0
        shock = volatility * np.random.normal()
        price = prices[-1] * np.exp(drift + shock)
        prices.append(price)

    return prices

def main():
    # 1. Simulate 60 days of Bitcoin price data
    days = 60
    prices = simulate_bitcoin_prices(days=days, initial_price=60000, volatility=0.05)

    # 2. Use pandas to calculate the 7-day and 30-day Moving Averages
    df = pd.DataFrame({
        'Day': range(1, days + 1),
        'Price': prices
    })

    df['SMA7'] = df['Price'].rolling(window=7).mean()
    df['SMA30'] = df['Price'].rolling(window=30).mean()

    # 3. Implement 'Golden Cross' trading algorithm
    initial_balance = 10000.0 # Start with $10,000
    usd_balance = initial_balance
    btc_balance = 0.0

    print("--- Daily Ledger ---")
    print(f"Initial Portfolio: ${usd_balance:.2f}, {btc_balance} BTC\n")

    position = 0 # 0 means we only hold USD, 1 means we hold BTC

    for i in range(len(df)):
        day = df.loc[i, 'Day']
        price = df.loc[i, 'Price']
        sma7 = df.loc[i, 'SMA7']
        sma30 = df.loc[i, 'SMA30']
        action = "HOLD"

        # Check for crossovers only if we have sufficient data
        if pd.notna(sma7) and pd.notna(sma30) and i > 0:
            prev_sma7 = df.loc[i-1, 'SMA7']
            prev_sma30 = df.loc[i-1, 'SMA30']

            if pd.notna(prev_sma7) and pd.notna(prev_sma30):
                # Golden Cross: 7-day SMA crosses above 30-day SMA -> BUY
                if prev_sma7 <= prev_sma30 and sma7 > sma30:
                    if position == 0:
                        btc_bought = usd_balance / price
                        btc_balance += btc_bought
                        usd_balance = 0.0
                        position = 1
                        action = f"BUY {btc_bought:.6f} BTC at ${price:.2f}"

                # Death Cross: 7-day SMA crosses below 30-day SMA -> SELL
                elif prev_sma7 >= prev_sma30 and sma7 < sma30:
                    if position == 1:
                        usd_bought = btc_balance * price
                        usd_balance += usd_bought
                        btc_balance = 0.0
                        position = 0
                        action = f"SELL at ${price:.2f}"

        # Determine SMA strings for printing
        sma7_str = f"${sma7:.2f}" if pd.notna(sma7) else "N/A"
        sma30_str = f"${sma30:.2f}" if pd.notna(sma30) else "N/A"

        print(f"Day {day:02d} | Price: ${price:9.2f} | SMA7: {sma7_str:>10} | SMA30: {sma30_str:>10} | Action: {action}")

    # 4. Final Portfolio Performance
    print("\n--- Final Performance ---")
    final_value_usd = usd_balance + (btc_balance * df.iloc[-1]['Price'])
    profit = final_value_usd - initial_balance
    profit_pct = (profit / initial_balance) * 100

    print(f"Final USD Balance: ${usd_balance:.2f}")
    print(f"Final BTC Balance: {btc_balance:.6f} BTC")
    print(f"Final Portfolio Value (in USD): ${final_value_usd:.2f}")
    print(f"Total Profit/Loss: ${profit:.2f} ({profit_pct:.2f}%)")

if __name__ == "__main__":
    main()
