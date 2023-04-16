# v1 only taking the data from 2014-2017 and creating the model

import numpy as n
import pandas 
import pickle
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#  guidance from https://towardsdatascience.com/deploy-a-machine-learning-model-using-flask-da580f84e60c



# symbol,date,open,high,low,close,volume
data = pandas.read_csv('stock_prices_2014-2017.csv')

total_rows = len(data.index)

# ticker : {dates:array of dates, prices: array of prices}
ticker_info = {}

# formats the data 
for i in range(0, total_rows):
    current_row = data.iloc[i].to_dict()

    ticker = current_row['symbol']

    if ticker in ticker_info.keys():
        ticker_dates = list(ticker_info[ticker]["dates"])
        ticker_prices = list(ticker_info[ticker]["prices"])

        ticker_prices.append(current_row['close'])
        ticker_dates.append(current_row['date'])

        ticker_info[ticker]['prices'] = ticker_prices
        ticker_info[ticker]['dates'] =  ticker_dates
    else:
        ticker_info[ticker] = {
            'prices': [current_row['close']],
            'dates':  [current_row['date']]
        }

# create json file with a list of all available tickers
with open('stocks.json', 'w') as file:
    json.dump(list(ticker_info.keys()), file)
    file.close()

if not os.path.exists('./models'):
    os.mkdir('./models')

# train each ticker with its dates and prices data
for ticker, ticker_info in ticker_info.items():
    regressor = LinearRegression()

    # convert dates into pandas timestamp
    dates_as_timestamp =  list(map(lambda date: pandas.to_datetime(date) ,ticker_info['dates']))

    # convert timestamps into a numeric starting from the day 1 year 1
    # then shaping into 2D
    ticker_date_slice = n.array(list(map(lambda date: date.toordinal() , dates_as_timestamp))).reshape(-1, 1)

    # get prices for the ticker and shape it into 2D array 
    ticker_prices_slice = n.array(ticker_info['prices']).reshape(-1, 1)


    X_train, X_test, y_train, y_test = train_test_split(ticker_date_slice, ticker_prices_slice, test_size = 0.33, random_state = 0)

    regressor.fit(X_train, y_train)
    
    filename = f'./models/{ticker}-model.pkl'
    
    pickle.dump(regressor, open(filename,'wb'))
