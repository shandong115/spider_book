import sys
import ast
import pymysql
import traceback
import time
from my_util import get_now_time,get_one_page,parse_page_one_book

#1.从数据库逐条取记录
#2.获取网页
#3.解析出关键字段
#4.入库

host 		= 'localhost'
database 	= 'bookdb'
user 		= 'dayou'
passwd 		= 'asdasd321321'
remote_host	= 'https://obook.cc/'

def get_one_book_detail(book_href):
	url = remote_host+book_href
	html = get_one_page(url)
	if html is None:
		print('get one page Error! '+url)
		return None
			
	return parse_page_one_book(html)
	
def get_one_book_detail2(book_href):
	
	
	with open('thread-2.htm','r',encoding='utf-8') as fp:
		html=fp.read()
		
	return parse_page_one_book(html)	
		
def get_data_from_db(low, high):
	# 打开数据库连接
	conn = pymysql.connect(host, user, passwd, database )
	cursor = conn.cursor()
	
	# SQL 查询语句
	sql_query = "SELECT book_id, book_href FROM book_info \
       WHERE is_ok=0 and book_id>= %s and book_id<%s" % (low, high)
	
	# SQL插入语句
	sql_insert = "INSERT INTO book_detail_info (book_id,pan_type,pan_url,pan_code,on_shalf_date,abstract,create_date)\
			VALUES (%s,%s,%s,%s,%s,%s,%s)"
	
	# SQL更新语句
	sql_update = "UPDATE book_info SET is_ok = 1 WHERE book_id = %s"
	
	i = 0
	try:
		# 执行SQL语句
		cursor.execute(sql_query)
		# 获取所有记录列表
		results = cursor.fetchall()
		for row in results:
			book_id = row[0]
			book_href = row[1]
			# 打印结果
			print ("book_id=%s,book_href=%s" % (book_id, book_href))
			book_dict = get_one_book_detail(book_href)
			if book_dict is None:
				print('get_one_book_detail Error! '+book_href)
				time.sleep(5)
				continue
			create_date = get_now_time()
			book_tup = (int(book_id),book_dict['pan_type'],book_dict['pan_url'],book_dict['pan_code'],book_dict['on_shalf_date'],book_dict['abstract'],create_date)
			
			#print(str(book_tup))
			cursor.execute(sql_insert, book_tup)
			cursor.execute(sql_update, int(book_id))
			
			i=i+1
			if i%20 == 0:
				conn.commit()
				print('have dealed books: '+str(i))
				
			time.sleep(3)
			
	except Exception as e:
		print('db deal Error! ')
		traceback.print_exc()
		print ("Error: unable to fetch data")
	
	# 关闭数据库连接
	conn.commit()
	cursor.close()
	conn.close()
	
if __name__ == '__main__':
	start_index = sys.argv[1]
	end_index = sys.argv[2]
	for i in range(10):
		get_data_from_db(start_index,end_index)
		time.sleep(60)
		print(str(i))
	
	