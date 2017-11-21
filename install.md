1.

	pip install flask_sqlalchemy

2.

	pip install flask_login

3.

	3.1
		安装Microsoft Visual C++ Compiler for Python 2.7： https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266
	3.2
		修改Python27\Lib下的ntpath.py文件的join函数，在函数开始加上两行：
		    reload(sys)
			sys.setdefaultencoding('gbk')
	3.3
		pip install wheel
	3.4
		pip install mysqlclient-1.3.12-cp27-cp27m-win32.whl  注意这里命令行路径下需要存在此.whl文件
