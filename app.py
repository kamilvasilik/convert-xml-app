import os

from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
import requests
import logging

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)


@app.route('/')
@basic_auth.required
def form():
    return render_template('form.html')


@app.route('/data', methods=['GET', 'POST'])
def user_request():
    if request.method == 'GET':
        return f'<h2>"/data" accessed directly. Go to "/" to access form to post data.</h2>'
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html', form_data=form_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005, debug=True)
