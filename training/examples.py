import pickle
import datetime as dt
import json
import os

# Example of loading in one of the model and getting a prediction
model = pickle.load(open('./example-models/AAPL-model.pkl','rb'))
test_date = dt.date(2023,3,9).toordinal()
prediction = model.predict([[test_date]])
print(prediction[0][0])

# reading data from stocks.json
# probably wanna use it to check if the ticker request is in this list
with open('stocks.json','r') as file:
    l = json.loads(file.read())
    print(len(l))