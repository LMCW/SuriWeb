#coding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  #Python自然调用ascii编码解码程序去处理字符流，当字符流不属于ascii范围内，就会抛出异常,所以python 默认编码改为utf-8


from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from database.database import database

app = Flask(__name__)

def request_to_dict(http_request):
    data_dict = dict(http_request.form)
    print data_dict
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0]
    return data_dict


@app.route('/')
def home():
	return redirect('/index')


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
		else:
			print "Login Successful"
			return redirect('/index')

	return render_template('login.html')

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register' ,methods=['POST','GET'])
def register():
    if request.method == 'POST':
        data=request_to_dict(request)
        arg2={'username':data['rname'],'password':data['rpassword'],'mail':data['rmail'],'info':data['rinfo']}
        if database.insert(database.user_table,**arg2):
            print "succeed register"
        else:
           print "failed register"
    return render_template('register.html')

if __name__ == '__main__':
	app.run(debug=True)