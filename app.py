from flask import Flask, render_template, request
import json
import pickle
import datetime as dt


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/results', methods=['POST'])
def results():
    ticker = (request.form['ticker']) 
    dateStr = request.form['start']

    # validate ticker
    with open('stocks.json','r') as file:
        list = json.loads(file.read())
        file.close()

    if ticker not in list:
        return ('', 204) # empty HTTP response

    # load model
    model = pickle.load(open(f'./models/{ticker}-model.pkl','rb'))
    
    # predict
    date = dt.datetime.fromisoformat(dateStr).toordinal()
    prediction = model.predict([[date]])

    return render_template('results.html', ticker = ticker, date = dateStr, price = prediction[0][0]) 

    

if __name__ == "__main__":
    app.run()

