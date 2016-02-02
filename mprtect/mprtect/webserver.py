from flask import Flask, render_template

app = Flask('mprtect')

@app.route('/')
def home():
    return render_template('home.html')