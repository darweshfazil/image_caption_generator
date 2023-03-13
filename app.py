from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/getGreetings')
def getGreetings():
    return render_template('greetings.html')

def initialize():
    print("<-----This function will run once----->")

if __name__ == '__main__' :
    initialize()
    app.run(debug=False)