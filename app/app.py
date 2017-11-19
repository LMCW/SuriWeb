import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
	return redirect('/index')

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	return render_template('login.html')

@app.route('/index')
def index():
	return 'index'

if __name__ == '__main__':
	app.run(debug=True)