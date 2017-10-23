from flask import Flask, jsonify, render_template, request, session
from datetime import datetime

app = Flask(__name__)


@app.route('/_get_weather_info', methods=['GET', 'POST'])
def response():
    pass


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
