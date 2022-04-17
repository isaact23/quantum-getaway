from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def form():
    return render_template("form.html")


@app.route('/results', methods = ['POST', 'GET'])
def results():
    return render_template("results.html")
