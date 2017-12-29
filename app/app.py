#coding: utf-8
import os
import sys
import re
from datetime import datetime, timedelta
reload(sys)
sys.setdefaultencoding('utf-8')  #Python自然调用ascii编码解码程序去处理字符流，当字符流不属于ascii范围内，就会抛出异常,所以python 默认编码改为utf-8

import time
from scapy.all import *
from flask import Flask, Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import session
from flask import flash
from flask import send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import UserMixin
from flask_login import current_user
from database.database import database
import threading
from time import ctime,sleep


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
firstStart = 0

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


threads = []

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
    global firstStart
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
	    firstStart = 0
            return redirect('/index')
        else:
            # wrong username or password
            print 'Fails login'
            flash("Wrong password")
    return render_template('login.html')

def test():
    print 1
    for i in Task.query.all():
        if i.id == 50:
            print 2
            i.isCompleted = 1
            # i.endTime = int(time.time())
            print i
            break

isCompleted = {}
endTime = {}
# 运行任务的子线程
def RunMission(func, func2):
    print "start running"
    str1 =  "./test.exe 100000000 %d ./result/%d_%d.result" %(int(time.time()),func2,func)
    str =  "suricata -r "+basedir+"/pcap/%d_%d.pcap "%(func2,func)+"-l "+basedir+"/log/%d_%d/"%(func2,func)
    print str
    os.system("mkdir "+basedir+"/log/%d_%d/"%(func2,func))
    os.system(str)
    os.system("zip -r result/%d_%d.zip log/%d_%d/" %(func2,func,func2,func))
    os.system("rm -r log/%d_%d" %(func2, func))
    # 修改数据库某一项的例子 假设我们已经知道任务的id，这里假设已知的id为10，即为数据库中root用户的第二个任务
    isCompleted[func] = 1
    endTime[func] = int(time.time())
    print "finish running"


proto = {}
srcIP = {}
dstIP = {}
segments = []
cumulate = []
isAnalysing = 0

def RunChart(func):
    print "start analysing"
    global proto
    global srcIP
    global dstIP
    global segments
    global cumulate
    global isAnalysing
    proto = {}
    srcIP = {}
    dstIP = {}
    s1=PcapReader(func)
    cnt=0
    statistic = []
    while 1:
    	p = s1.read_packet()
   	if p is None:
            break
    	else:
            cnt = cnt + 1
        if cnt % 10000 == 0:
            print cnt
        tmp = []
	tmp.append(p.time)
	try:
	    tmp.append(p.len)
	except Exception as e:
	    tmp.append(-1)
	statistic.append(tmp)
	if not(p.name == 'IP' or p.payload.name == 'IP' or p.payload.payload.name == 'IP'):
            continue
        reprval = p["IP"].src
        if reprval in srcIP.keys(): 
            srcIP[reprval] = srcIP[reprval] + 1
        else:
            srcIP[reprval] = 1
        
        reprval = p["IP"].dst
           
        if reprval in dstIP.keys(): 
            dstIP[reprval] = dstIP[reprval] + 1
        else:
            dstIP[reprval] = 1
            
        reprval = p["IP"].proto
        if reprval in proto.keys(): 
            proto[reprval] = proto[reprval] + 1
        else:
            proto[reprval] = 1
    s1.close()
    timeseg = (statistic[-1][0]-statistic[0][0])/100.0
    segments = [(statistic[0][0]+i*timeseg) for i in range(100)] #x array
    cumulate = [0 for i in range(100)]
    for i in range(cnt):
 	idx = int((statistic[i][0] - statistic[0][0])/timeseg)
	if idx >= 100:
	    idx = 99
       
	cumulate[idx] += 1
	
    tmp = segments[0]
    for i in range(100):
	segments[i] -= tmp
    isAnalysing = 0
    print "finish analysing"

#上传任务
@app.route('/upload', methods=['POST','GET'])
def upload():
    f = request.files['uploadfile']

    # (1)上传文件插入数据库并通过全局变量isCompleted和endTime记录子线程中对数据库的修改
    path = basedir + '/result/' + str(current_user.username) + '/'
    print path
    t=Task(userId = current_user.id,isCompleted = 0, beginTime = int(time.time()), endTime = 0, resultPath=path)

    db.session.add(t)
    db.session.commit()
    isCompleted[t.id] = 0
    endTime[t.id] = 0
    # (2)存储文件到本地
    temp = basedir+'/pcap/'+str(current_user.id)+'_'+str(t.id)+'.pcap'
    f.save(temp)

    # (3)开启子线程来运行任务
    t1 = threading.Thread(target=RunMission,args=(t.id, current_user.id, ))
    threads.append(t1)
    t1.setDaemon(True)
    t1.start()


    '''
    # (3)删除任务，根据任务ID
    dt=Task.query.filter_by(id=5).first()
    db.session.delete(dt)
    db.session.commit()
    '''
    return redirect('/uploadMission')

#显示任务列表
@app.route('/display', methods=['POST','GET'])
def display():
    global firstStart
    # 对isCompleted和endTime进行初始化
    if firstStart == 0:
        firstStart = 1    
        task = Task.query.filter_by(userId=current_user.id).all()
        for x in task:
            isCompleted[x.id] = x.id
            endTime[x.id] = x.endTime
    if request.method == 'GET':
        task = Task.query.filter_by(userId=current_user.id).all()
        result = {}
        cnt = 0
        for x in task:
            A={}
            if isCompleted[x.id]==1 :
                x.isCompleted = 1
                x.endTime = endTime[x.id]
            A['id']=x.id
            A['userId']=x.userId
            A['isCompleted']=x.isCompleted
            A['beginTime']=x.beginTime
            A['endTime']=x.endTime
            A['resultPath']=x.resultPath
            result[cnt]=A
            cnt = cnt + 1

        

        return jsonify(result=result, cnt=cnt)

#根据任务id开启解析线程
@app.route('/getChart', methods=['GET'])
def getChart():
    global isAnalysing
    if isAnalysing == 1:
        return jsonify(flag = 1)
    if request.args.get("a")=="":
	return jsonify(flag = 2)
    print request.args.get("a")
    path = basedir+'/pcap/'+str(current_user.id)+'_'+str(request.args.get("a"))+'.pcap'
    print path
    t1 = threading.Thread(target=RunChart,args=(path,))
    threads.append(t1)
    t1.setDaemon(True)
    t1.start()
    isAnalysing = 1
    return jsonify(flag = 0)

#刷新解析界面并返回结果
@app.route('/refresh', methods=['GET'])
def refresh():
    global isAnalysing
    global proto
    global srcIP
    global dstIP
    global segments
    global cumulate
    if isAnalysing == 1:
        return jsonify(flag = 1, srcIP = {}, dstIP = {}, proto = {})
    return jsonify(flag = 0, srcIP = srcIP, dstIP = dstIP, proto = proto,segments = segments, cumulate = cumulate)

@app.route('/downloadResult', methods=['GET'])
def downloadResult():
    return send_from_directory('result',str(current_user.id)+'_'+str(request.args.get("id"))+'.zip',as_attachment=True)
    #return 1
    
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
			if data['rpassword'] == "" or data['rinfo'] == "" or data['rpassword'] != data['rrpassword']:
				print "invalid password or info, register fail"
				flash("Invalid password or info")
				return redirect('/register')
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
				    return redirect('/register')
			else:
			    flash("Invalid mail address")
			    return redirect('/register')

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

@app.route('/analyse')
@login_required
def analyse():
    return render_template('analyse.html')

@app.route('/developing')
def developing():
    return render_template('developing.html')

@app.route('/infomation')
@login_required
def infomation():
    test = []
    for i in User.query.all():
        if i.username == current_user.username:
            #print i.username
            #print i.mail
            #print i.info
            test.append(str(i.username)) # test[0] username
            test.append(str(i.mail)) # test[1] mail
            test.append(str(i.info)) # test[2] info
            #flash(test) # go to frontend
    flash(test)
    return render_template('infomation.html')

@app.route('/infomation' ,methods=['POST','GET'])
def changeInfomation():
	print "change infomation"
	# username and mail cannot be changed
	if request.method == 'POST':
		data = request_to_dict(request)
		if data['rpassword'] == "" or data['rinfo'] == "" or data['rpassword'] != data['rrpassword']:
			print "change infomation failed. Invalid password or info."
			return redirect('infomation')
		for i in User.query.all():
			if i.id == current_user.id:
				i.password = data['rpassword']
				i.info = data['rinfo']
				print "change infomation successfully"
		return redirect('infomation')
	return redirect('infomation')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

