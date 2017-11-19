import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from database.database.py import database

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
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template('register.html')

if __name__ == '__main__':
	app.run(debug=True)