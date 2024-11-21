import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch data from Yahoo Finance
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data

# Function to apply stock selection criteria
def apply_criteria(stock_data):
    stock_data['52_week_high'] = stock_data['High'].rolling(window=252, min_periods=1).max()
    stock_data['52_week_high_diff'] = stock_data['Close'] / stock_data['52_week_high'] - 1
    
    last_price = stock_data['Close'].iloc[-1]
    three_months_return = stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[-63] - 1
    six_months_return = stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[-126] - 1
    one_year_return = stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[-252] - 1
    
    return {
        'last_price': last_price,
        'three_months_return': three_months_return,
        'six_months_return': six_months_return,
        'one_year_return': one_year_return,
        '52_week_high_diff': stock_data['52_week_high_diff'].iloc[-1]
    }

# Main function
def main():
    st.title("Stock Selection from Nifty 200")
    tickers = st.text_input("Enter Nifty 200 stock tickers separated by commas:")
    if tickers:
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        
        results = []
        for ticker in tickers_list:
            data = fetch_data(ticker)
            criteria_results = apply_criteria(data)
            if (
                criteria_results['last_price'] < 5000 and
                criteria_results['three_months_return'] > 0 and
                criteria_results['one_year_return'] > 0.20 and
                criteria_results['one_year_return'] > criteria_results['six_months_return'] > criteria_results['three_months_return']
            ):
                results.append({
                    'Ticker': ticker,
                    'Last Price': criteria_results['last_price'],
                    '3 Months Return': criteria_results['three_months_return'],
                    '6 Months Return': criteria_results['six_months_return'],
                    '1 Year Return': criteria_results['one_year_return'],
                    '52 Week High Diff': criteria_results['52_week_high_diff']
                })
        
        sorted_results = sorted(results, key=lambda x: x['52 Week High Diff'])
        top_stocks = sorted_results[:3]
        
        st.write("Top 3 Selected Stocks:")
        st.dataframe(pd.DataFrame(top_stocks))
        
if __name__ == "__main__":
    main()
