#coding:utf-8
import  os
import sys

parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #系统的主目录
sys.path.insert(0,parentdir)

import threading
import pymysql
import  thread
import urllib
from constants import DB_CONFIG

class DataBase:

    def __int__(self):
        #下面是默认的设置
        self.host='127.0.0.1'
        self.db_name='suriweb'
        self.username='root'
        self.password='root'
        self.port=3306
        self.connection=None
        pass


    @classmethod
    def wrap_str(cls, raw_str):    #把"  换成\
        return '"' + str(raw_str).replace('"', '\'') + '"'

    #设置数据库的内容
    def config(self,config_dict):
        self.host = config_dict['url']
        self.db_name = config_dict['db_name']
        self.username = config_dict['username']
        self.password = config_dict['password']
        self.host, port = urllib.splitport(str(config_dict['url']))
        try:
            self.port = int(port)
        except Exception:
            self.port = 3306

        #进行数据库的连接
        try:
            self.connection = pymysql.connect(host=self.host, port=self.port, user=self.username,
                                              passwd=self.password, db=self.db_name, charset="utf8")
            print 'database connect success!'
        except BaseException as e:
            print e
            print '[Fail]database config Fails...'
            return False
        return True

    #查找sql语句的第一个元素
    def select_by_id(self,sql):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result=cursor.fetchone()  #读取符合条件的第一个内容
            if not result:
                return None
            #print result
            return result

    #删除 数据表的 id 号元素
    def delete_by_id(self,table,item_id):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('delete from %s where id= %d'%(table,item_id))
            self.connection.commit()

    #获取数据表的所有数据
    def select_all(self,table):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('select * from %s'%(table))
            result=cursor.fetchall()
            self.connection.commit()
            return result

    #向数据表插入新的数据
    def insert(self,table_name,**params): #params 插入的字典
        cols,args=zip(*params.iteritems())
        for arg in args:
            print 'type of',arg,' is ',type(arg)
        args=[self.wrap_str(arg) if isinstance(arg,unicode) or isinstance(arg,str) else str(arg) for arg in args]
        sql = 'insert into `%s` (%s) values (%s)'% (table_name, ','.join(['`%s`' % col for col in cols]), ','.join([arg for arg in args]))
        if self.connection is None:
            self.config(DB_CONFIG)
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            try:
                print '[sql]:',sql
                cursor.execute(sql)
                self.connection.commit()
            except pymysql.IntegrityError:
                print '[Error] Dumplicate entry'

    #更新数据表的内容
    def update(self,table_name,item_id,**params):
        print 'update params ',params
        sql='update ' +table_name +' set '

        for field,value in params.items():
            if isinstance(value,str) or isinstance(value,unicode):  #添加双引号
                value=self.wrap_str(value)
            sql +=str(field)+'='+str(value)+','
        sql=sql[:-1]+' where id='+str(item_id)+';'
        with self.connection.cursor() as cursor:
            try:
                print "[sql:]",sql
                cursor.execute(sql)
                self.connection.commit()
            except Exception as e:
                print '[Error]sql_database Update mission', item_id, ' fails'
                print e
    def __block__execute__(self,sql):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            try:
                self.connection.commit()
            finally:
                thread.exit_thread()

    def execute(self,sql):
        sql_thread=threading.Thread(target=self.__block__execute__,args=(sql,))
        sql_thread.start()
        self.__block__execute__(sql)

database=DataBase()
database.config(DB_CONFIG)

'''
if __name__=="__main__":
    c=DataBase()
    c.config(DB_CONFIG)
    arg={'username':'wuyy56','password':'wuyy'}
    c.update('user',4,**arg)
'''

