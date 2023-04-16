# v3 use the 200 moving averages # v2 appending more data from 2017 - present 

import json
import os
import pickle
import yfinance as yf
import datetime as dt
import numpy as n
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

with open('../stocks.json','r') as file:
    stocks = json.loads(file.read())
    file.close()

if not os.path.exists('./v3-models'):
    os.mkdir('./v3-models')


for stock in stocks:
    try:
        company = yf.Ticker(stock)
        history = company.history(period="10y", interval="1d")

        dates = []
        prices = []

        history["200D MA"] = history["Close"].rolling(window=200).mean()
        
        # remove NaN's
        for index, data in history.iterrows():
            if n.isnan(data["200D MA"]):
                history = history.drop(index=index)
            else:
                split_date_str = index.strftime('%Y-%m-%d').split("-")
                prices.append(data["200D MA"])

                date = dt.date(int(split_date_str[0]), int(split_date_str[1]), int(split_date_str[2])).toordinal()
                dates.append(date)

        
        regressor = LinearRegression()

        dates = n.array(dates).reshape(-1, 1)
        prices = n.array(prices).reshape(-1, 1)


        X_train, X_test, y_train, y_test = train_test_split(dates, prices, test_size = 0.33, random_state = 0)

        regressor.fit(X_train, y_train)
        
        filename = f'./v3-models/{stock}-model.pkl'
        
        pickle.dump(regressor, open(filename,'wb'))
    except:
        continue

