# v2 appending more data from 2017 - present 

import json
import os
import pickle
from sklearn.model_selection import train_test_split
import yfinance as yf
import datetime as dt
import numpy as n

with open('../stocks.json','r') as file:
    stocks = json.loads(file.read())
    file.close()

if not os.path.exists('./v2-models'):
    os.mkdir('./v2-models')


for stock in stocks:
    model = pickle.load(open(f'../models/{stock}-model.pkl','rb'))

    try:
        company = yf.Ticker(stock)
        history = company.history(start="2017-01-01", end="2023-04-16", interval="1d")

        dates = []
        prices = []

        for index, data in history.iterrows():
            split_date_str = index.strftime('%Y-%m-%d').split("-")

            date = dt.date(int(split_date_str[0]), int(split_date_str[1]), int(split_date_str[2])).toordinal()
            close = data["Close"]

            dates.append(date)
            prices.append(close)

        
        dates = n.array(dates).reshape(-1, 1)
        prices = n.array(prices).reshape(-1, 1)


        X_train, X_test, y_train, y_test = train_test_split(dates, prices, test_size = 0.33, random_state = 0)

        model.fit(X_train, y_train)
        
        filename = f'./v2-models/{stock}-model.pkl'
        
        pickle.dump(model, open(filename,'wb'))
    except:
        continue

  
