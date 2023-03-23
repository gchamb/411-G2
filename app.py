from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/results', methods=['POST'])
def results():
    ticker = request.form['ticker']

    date = request.form['start']
    return render_template('results.html', result=ticker + " " + date) 


    

if __name__ == "__main__":
    app.run(debug=True)

