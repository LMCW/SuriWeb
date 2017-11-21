#coding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  #Python自然调用ascii编码解码程序去处理字符流，当字符流不属于ascii范围内，就会抛出异常,所以python 默认编码改为utf-8


from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from flask_login import UserMixin
from database.database import database

app = Flask(__name__)
app.secret_key = 'Xa\r5\xfd\xe0\x84\x81)lfDCJ.a\xc2\x01\x1bn0\xef\x01\xc8'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/suriweb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.init_app(app)


class User(db.Model, UserMixin):
	__tablename__='user'
	id = db.Column(db.Integer, primary_key=True)
	mail = db.Column(db.String(64),index=True)
	username = db.Column(db.String(64),unique=True, index=True)
	password = db.Column(db.String(28))
	info = db.Column(db.String(255))

	def confirm_password(self, p):
		if p==self.password:
			return True
		else:
			return False

@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id=user_id).first()



def request_to_dict(http_request):
    data_dict = dict(http_request.form)
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0]
    return data_dict


@app.route('/')
def home():
	return redirect('/index')

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
		
		user = User.query.filter_by(username=username).first()
		# check if these infomation are correct in the database
		if user is not None and user.confirm_password(password):
			print "Login Successful"
			login_user(user,True)
			return redirect('/index')
		else:
			# wrong username or password
			print 'Fails login'
			flash("Wrong password")
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

@app.route('/uploadMission')
def upload():
	return render_template('uploadMission.html')


if __name__ == '__main__':
	app.run(debug=True)
