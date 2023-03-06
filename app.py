from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('hello.html')
    
@app.route('/results', methods=['POST'])
def results():
    Cname = (request.form['Cname']) 
    Cname_result = Cname

    Date = (request.form['start'])
    return render_template('results.html', result= Cname_result + " " + Date) 


    

if __name__ == "__main__":
    app.run()

