import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch data from Yahoo Finance
def fetch_data(tickers):
    data = yf.download(tickers, period="1y", group_by='ticker')
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
    st.title("Stock Selection from Nifty 100")
    
    # Number of stocks to shortlist
    num_stocks = st.number_input("Enter the number of stocks to shortlist:", min_value=1, max_value=100, value=3)
    
    # Fetch data for Nifty 100 stocks
    tickers_list = ['RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 'TCS.NS', 'HINDUNILVR.NS', 'KOTAKBANK.NS', 'HDFC.NS', 'BHARTIARTL.NS', 'ITC.NS',
                    'SBIN.NS', 'ASIANPAINT.NS', 'BAJFINANCE.NS', 'DMART.NS', 'AXISBANK.NS', 'LT.NS', 'HCLTECH.NS', 'MARUTI.NS', 'TITAN.NS', 'SUNPHARMA.NS',
                    'ULTRACEMCO.NS', 'M&M.NS', 'TATASTEEL.NS', 'NTPC.NS', 'BAJAJ-AUTO.NS', 'ONGC.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS', 'POWERGRID.NS', 'SBILIFE.NS',
                    'BPCL.NS', 'GRASIM.NS', 'INDUSINDBK.NS', 'NESTLEIND.NS', 'ADANIGREEN.NS', 'PIDILITIND.NS', 'WIPRO.NS', 'HEROMOTOCO.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS',
                    'DRREDDY.NS', 'HINDALCO.NS', 'CIPLA.NS', 'TECHM.NS', 'APOLLOHOSP.NS', 'BRITANNIA.NS', 'SHREECEM.NS', 'COALINDIA.NS', 'UPL.NS', 'TATAMOTORS.NS',
                    'DABUR.NS', 'ICICIGI.NS', 'ADANIENT.NS', 'GODREJCP.NS', 'HDFCLIFE.NS', 'MCDOWELL-N.NS', 'LUPIN.NS', 'BIOCON.NS', 'SIEMENS.NS', 'AMBUJACEM.NS',
                    'VBL.NS', 'TRENT.NS', 'ADANITRANS.NS', 'ALKEM.NS', 'ICICIPRULI.NS', 'MARICO.NS', 'BERGEPAINT.NS', 'COLPAL.NS', 'PAGEIND.NS', 'DLF.NS',
                    'AUROPHARMA.NS', 'NAUKRI.NS', 'SRF.NS', 'ACC.NS', 'CONCOR.NS', 'BANDHANBNK.NS', 'PIIND.NS', 'INDIGO.NS', 'TORNTPHARM.NS', 'VEDL.NS',
                    'BALKRISIND.NS', 'TATACONSUM.NS', 'ADANIPOWER.NS', 'ABB.NS', 'BANKBARODA.NS', 'HAVELLS.NS', 'LTI.NS', 'HINDZINC.NS', 'APLLTD.NS', 'MFSL.NS',
                    'INDHOTEL.NS', 'YESBANK.NS', 'PEL.NS', 'ADANIGAS.NS', 'BOSCHLTD.NS', 'GAIL.NS', 'BEL.NS', 'ADANILOG.NS', 'NYKAA.NS', 'JUBLFOOD.NS']

    data = fetch_data(tickers_list)

    results = []
    for ticker in tickers_list:
        if ticker in data.columns.levels[0]:
            stock_data = data[ticker]
            criteria_results = apply_criteria(stock_data)
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
    top_stocks = sorted_results[:num_stocks]
    
    st.write(f"Top {num_stocks} Selected Stocks:")
    st.dataframe(pd.DataFrame(top_stocks))

if __name__ == "__main__":
    main()
