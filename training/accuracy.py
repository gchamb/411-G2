import json
import pickle
import datetime as dt
import yfinance as yf

# load in json 
with open('../stocks.json','r') as file:
    stocks = json.loads(file.read())
    file.close()

length = len(stocks)
total_accurate = 0
# iterate over models
for stock in stocks:
    try:
        model = pickle.load(open(f'./v2-models/{stock}-model.pkl','rb'))

        today = dt.date.today().toordinal()

        # predict the price of today
        prediction = float(model.predict([[today]])[0][0])
    
    
        # get the actual prices of today
        company = yf.Ticker(stock)

        company_price = float(company.info["previousClose"])
        
        # if the predicted price is within 10% higher and lower of the current price then it's somewhat accurate
        high_end = company_price + (company_price * 0.1)
        low_end = company_price - (company_price * 0.1)

        if prediction >= low_end and prediction <= high_end:
            total_accurate += 1
    except:
        length -=1
        continue

  
accuracy = total_accurate / length * 100

with open('../accuracy.txt', 'a') as accuracyFile:
    accuracyFile.write("{:.2f}\n".format(accuracy))
    accuracyFile.close()