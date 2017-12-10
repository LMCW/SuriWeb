#coding: utf-8
import os
import sys
import re
from datetime import datetime, timedelta
reload(sys)
sys.setdefaultencoding('utf-8')  #Python自然调用ascii编码解码程序去处理字符流，当字符流不属于ascii范围内，就会抛出异常,所以python 默认编码改为utf-8

import time
from flask import Flask, Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import UserMixin
from flask_login import current_user
from database.database import database

#initialization of app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'Xa\r5\xfd\xe0\x84\x81)lfDCJ.a\xc2\x01\x1bn0\xef\x01\xc8'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/suriweb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialization of database
db = SQLAlchemy(app)

#initialization of login manager
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.remember_cookie_duration = timedelta(days=1)
login_manager.init_app(app)


class User(db.Model, UserMixin):
	__tablename__='user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64),unique=True, index=True)
	password = db.Column(db.String(28))
	mail = db.Column(db.String(64),index=True)
	info = db.Column(db.String(255))

	def confirm_password(self, p):
		if p==self.password:
			return True
		else:
			return False


class Task(db.Model):
    __tablename__='task'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    isCompleted=db.Column(db.Integer)
    beginTime=db.Column(db.Integer)
    endTime=db.Column(db.Integer)
    resultPath=db.Column(db.String(200))

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
		'''
		print User.query.all()
		for i in User.query.all():
			print i.username
		'''
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



@app.route('/upload', methods=['POST','GET'])
def upload():
    f = request.files['uploadfile']
   
    
    #创建 by wuyy

    # (1)上传文件插入数据库
    path = basedir + '\\result\\' + str(current_user.username) + '\\'
    t=Task(userId = current_user.id,isCompleted = 0, beginTime = int(time.time()), endTime = 0, resultPath=path)
    db.session.add(t)
    db.session.commit()

    # (2)存储文件到本地
    temp = basedir+'\\pcap\\'+str(current_user.id)+'_'+str(t.id)+'.pcap'
    print temp
    f.save(temp)
    
    
    '''
    # (3)删除任务，根据任务ID
    dt=Task.query.filter_by(id=5).first()
    db.session.delete(dt)
    db.session.commit()
    '''
    return redirect('/uploadMission')

@app.route('/display', methods=['POST','GET'])
def display():
    # (1)通过用户名查找对应的任务,存储在result 字典里面

    if request.method == 'GET':
        task = Task.query.filter_by(userId=current_user.id).all()
        result = {}
        cnt = 0
        for x in task:
            A={}
            A['userId']=x.userId
            A['isCompleted']=x.isCompleted
            A['beginTime']=x.beginTime
            A['endTime']=x.endTime
            A['resultPath']=x.resultPath
            result[cnt]=A
            cnt = cnt + 1
        print result
        return jsonify(result=result, cnt=cnt)
   
    
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register' ,methods=['POST','GET'])
def register():
    if request.method == 'POST':
    	data=request_to_dict(request)
    	# 设定不允许出现重复username
    	flag = True
    	for i in User.query.all():
    		if i.username == data['rname']:
    			flag = False
    			break
    	# print flag
    	if flag == False:
    		print "the username has been registered, register fail"
    		# flash 重复用户名处理
    		flash("The username has been registered")
    		return redirect('/register')
    	else:
    		# 判断邮箱是否合法
    		if len(data['rmail']) > 7:
    			if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", data['rmail']) != None:
					# 在数据库中id递增，因此新加入的用户的id为usertable的size+1
		    		newUser = User(id = len(User.query.all()) + 1, username = data['rname'], password = data['rpassword'], mail = data['rmail'], info = data['rinfo'])
		        	db.session.add(newUser)
		        	db.session.commit() 
		        	print "register successfully"
		        	return redirect('/login')
	        	else:
	        		print "invalid mailaddress, register fail"
	        		flash("Invalid mail address")
    		else:
    			flash("Invalid mail address")

    	'''  原来的写法
        data=request_to_dict(request)
        arg2={'username':data['rname'],'password':data['rpassword'],'mail':data['rmail'],'info':data['rinfo']}
        if database.insert(database.user_table,**arg2):
            print "succeed register"
        else:
           print "failed register"
        '''
    print "register fail"
    return render_template('register.html')

@app.route('/uploadMission')
@login_required
def uploadMission():
	return render_template('uploadMission.html')

@app.route('/missionList')
@login_required
def missionList():
	return render_template('missionList.html')


@app.route('/developing')
def developing():
	return render_template('developing.html')



@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/index')


if __name__ == '__main__':
	app.run(debug=True)

