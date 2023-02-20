import numpy as np
import pandas as pd
import streamlit as st
import yahooquery as yf
import plotly.express as px


# url or file of the ticker source
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
djia_url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'

# Create a new variable query_submit and set equal to false for flow - used later, set at beginning
query_submit = False

# Create a simple title for our page
st.title('A new stock screener @ UNF!')

# Create a form located on a sidebar with a key and no clear on submit
with st.form(key = 'stock_inputs', clear_on_submit = False):
    with st.sidebar:

        # Create a sidebar title
        st.sidebar.title('Stock Inputs Go Below')

        # Create a selectbox for the index of choice
        stock_index = st.sidebar.selectbox('Select Index of Interest:', ['', 'S&P500', 'DJIA'])

        # Retrieving tickers data only IF index is selected, use read_html(x, flavor = 'html5lib')[x]['Symbol'])
        if stock_index:
            if stock_index == 'S&P500':
                stock_list = pd.read_html(sp500_url, flavor = 'html5lib')[0]['Symbol']
            if stock_index == 'DJIA':
                stock_list = pd.read_html(djia_url, flavor = 'html5lib')[1]['Symbol']

            # Select the ticker of interest from the index selected
            stock_ticker = st.sidebar.selectbox(f'Select ticker from {stock_index}', stock_list)

            # Get the data for that specific ticker using yf.Ticker
            ticker_data = yf.search(stock_ticker, first_quote = True)

            # Get the historical prices for that ticker using a period of '30d' and the file created above and .history
            ticker_raw = yf.Ticker(stock_ticker)
            ticker_prices = ticker_raw.history(period = '1mo').reset_index().set_index('date')

            # Drop all missing values from prices
            ticker_prices.dropna(inplace = True)

            # Create a form submit button with a label
            query_submit = st.form_submit_button('Submit stock inputs.')

# if query_submit is changed from False to True in the above for loop, display stock info
if query_submit:

    # display ticker logo (.info['logo_url'])
    #st.image(ticker_data.info['logo_url'])

    # display company long name (longName), use st.header
    stock_name = ticker_raw.quotes[stock_ticker]['shortName']
    st.header(stock_name)

    # display company summary (longBusinessSummary), use st.write
    st.write(ticker_raw.asset_profile[stock_ticker]['longBusinessSummary'])

    # get actual price data and display the dataframe
    st.dataframe(ticker_prices.head())

    # Create a new subheader for a graph of price over time
    st.subheader(f'Change in price over time for {stock_name}')

    # create a streamlit line_chart from ticker_prices with date on the x-axis and adjclose on the y-axis
    st.line_chart(ticker_prices['adjclose'])

    # create subheader for analyst recommendations
    st.subheader('Analyst Recommendations')

    # download recommendations with .get_recommendations
    recos = ticker_raw.grading_history
   
    # display the most recent values from the tail
    st.dataframe(recos.tail(10))
