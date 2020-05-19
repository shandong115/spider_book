import pymysql
 
host 		= 'localhost'
database 	= 'bookdb'
user 		= 'dayou'
passwd 		= 'asdasd321321'

def print_mysql_version():
	# 打开数据库连接
	db = pymysql.connect(host, user, passwd, database )
	 
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()
	 
	# 使用 execute()  方法执行 SQL 查询 
	cursor.execute("SELECT VERSION()")
	 
	# 使用 fetchone() 方法获取单条数据.
	data = cursor.fetchone()
	 
	print ("Database version : %s " % data)
	 
	# 关闭数据库连接
	db.close()
	
if __name__ == '__main__':
	
	print_mysql_version()