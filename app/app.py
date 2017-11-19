import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import session

from database.database import database

app = Flask(__name__)
app.secret_key = 'Xa\r5\xfd\xe0\x84\x81)lfDCJ.a\xc2\x01\x1bn0\xef\x01\xc8'

def request_to_dict(http_request):
    data_dict = dict(http_request.form)
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0]
    return data_dict


@app.route('/')
def home():
	return redirect('/index')

# login Fail
@app.route('/login_fail')
def login_fail():
	str =""
	if 'login' in session:
		if session['login'] == 0:
			str = "Wrong username or password"
			print str
	return jsonify(result = str)

# login
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	#print request.form
	#print request.method
	if request.method == 'POST':
		data=request_to_dict(request)
		username = data['username']
		password = data['password']

		# check if these infomation are correct in the database
		result=database.select_by_id("select * from user where username='%s' and password='%s'"%(username,password))
		#result=database.select_all('user')
		if not result:
			# wrong username or password
			print 'Fails login'
			session['login'] = 0

		else:
			print "Login Successful"
			session['login'] = 1
			return redirect('/index')

	return render_template('login.html')

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	return render_template('register.html')

if __name__ == '__main__':
	app.run(debug=True)