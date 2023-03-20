from flask import Flask, render_template, request
import json
import pickle
import datetime as dt


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/results', methods=['POST'])
def results():
    ticker = (request.form['Cname']) 
    dateStr = request.form['start']

    print(ticker)
    print(dateStr)

    # validate ticker
    with open('stocks.json','r') as file:
        l = json.loads(file.read())

    found = False
    for t in l:
        print(t)
        print(t == ticker)
        print(type(t))
        print(type(ticker))
        if t == ticker:
            found = True
            break

    if not found:
        return "Bad ticker" #

    # load model
    model = pickle.load(open(f'./models/{ticker}-model.pkl','rb'))
    
    # predict
    date = dt.datetime.fromisoformat(dateStr).toordinal()
    print(date)
    prediction = model.predict([[date]])
    print(prediction[0][0])

    return render_template('results.html', ticker = ticker, date = dateStr, price = prediction[0][0]) 


    

if __name__ == "__main__":
    app.run()

