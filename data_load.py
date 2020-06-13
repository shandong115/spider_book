import sys
import os
import ast
import pymysql
import traceback
from my_util import get_now_time
import time
from os.path import getsize
#from pypinyin import lazy_pinyin, Style
#import pypinyin

host 		= '192.168.31.42'
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
	cursor.close()
	db.close()
	
def update_book_size():
	dir_path = "E:\\workplace\\python\\python-project\\book\\"
	connection  = pymysql.connect(host, user, passwd, database )
	sql = "SELECT book_id, name FROM book_meta where book_id<6200"
	print(sql)
	i=0
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			books = cursor.fetchall()
			print(str(len(books)))
			for book in books:
				book_id = book[0]
				book_name = book[1]
				#文件大小
				file_name = dir_path + book_name + '.epub'
				try:
					fielsize = getsize(file_name)
					sql2 = "UPDATE book_meta SET size = %d WHERE book_id = %d" % (fielsize,book_id)
					#print(sql2)
					cursor.execute(sql2)
					i=i+1
					if(i%100 == 0):
						connection.commit()
						print('commit ok:'+str(i))
						time.sleep(2)
				except Exception as e:
					print(e)
					print(file_name + ' getsize fail.................\r\n')
					connection.commit()
				#else:
					#print(file_name + 'update size success: ' + str(fielsize) + '\r\n')	
				#break
		connection.commit()
	except:
		print ("db operate Error: ...")
	connection.close()
	
	
def update_book_ncode():
	connection  = pymysql.connect(host, user, passwd, database )
	sql = "SELECT book_id, book_name FROM book_meta where book_id>6199 and book_id<6299"
	print(sql)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			books = cursor.fetchall()
			print(str(len(books)))
			for book in books:
				book_id = book[0]
				book_name = book[1]
				#文件重命名
				try:
					os.rename(book_name+'.epub', book_id+'.epub')
				except Exception as e:
					print(e)
					print(book_name + ' rename fail.................\r\n')
				else:
					print(book_name + 'rename success\r\n')	
				break
	except:
		print ("db operate Error: ...")

	connection.close()
			
def update_bookName():
	connection  = pymysql.connect(host, user, passwd, database )
	#cursor = connection.cursor()
	#str1='（epub+mobi+pdf）'
	#str1='（epub+mobi）'
	#str1='（epub+mobi+azw3）'
	#str1='（epub+mobi+azw3+pdf）'
	#str1='（epub'
	#str1='（azw3'
	#str1='epub+'
	#str1='（mobi+'
	#str1=' pdf'
	str1='（pdf）'
	sql = "SELECT book_id, book_name FROM book_info where book_name like '%s%s%s'"%('%',str1,'%')
	print(sql)
	i = 0
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			books = cursor.fetchall()
			print(str(len(books)))
			for book in books:
				book_id = book[0]
				book_name = book[1]
				index = book_name.find(str1)
				if(index>0):
					book_name=book_name[:index]
					b_type=book_name[index:]
					print ("book_id:%d,book_new_name=%s" % (book_id,book_name))
					sql2 = "UPDATE book_info SET book_name = '%s', b_type='%s' WHERE book_id = %d" % (book_name,str1,book_id)
					#print(sql2)
					try:
						cursor.execute(sql2)
						i=i+1
						if(i%10 == 0):
							connection.commit()
							print('commit ok:'+str(i))
							time.sleep(2)
					except:
						print('update err...')
						connection.commit()
					#break
	except:
		print (" fetch data Error: ...")
	
	connection.commit()
	connection.close()

	
def get_sql_str():
	sql_str = "insert into book_info (book_id,book_name,book_type,ebook_type,img_path,book_href,read_num,is_ok,create_date)\
			values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	return(sql_str)

def get_book_id(book_href):
	#thread-14634.htm
	len_book_href = len(book_href)
	index_start = book_href.find('-', 0, len_book_href - 1)
	index_end = book_href.find('.', 0, len_book_href - 1)
	if(index_start>0 and index_end >0):
		return book_href[index_start+1:index_end]
	else:
		return None
		
def get_book_tup(book_dict):
	book_id = get_book_id(book_dict['book_href'])
	if book_id is None:
		print('get book_id is Error')
		return None
		
	create_date = get_now_time()
	
	tup = (int(book_id), book_dict['book_name'], book_dict['book_type'], book_dict['ebook_type'], book_dict['img_path'],book_dict['book_href'], int(book_dict['read_num']), int(book_dict['is_ok']), create_date)
	
	return(tup)
	
def deal_one_page(books):
	start = 0
	end = len(books)-1
	book_list = []
	while(1):
		index_start = books.find('{',start,end)
		index_end = books.find('}', index_start+1, end)
		if(index_start>0 and index_end>0):
			#deal one book.
			book_str = books[index_start:index_end+1]
			book_dict = ast.literal_eval(book_str)						
			start = index_end+1
						
			book_tup = get_book_tup(book_dict)
			if book_tup is None:
				print('get_book_tup Error!')
				continue
			book_list.append(book_tup)
		else:
			#print("one page books have dealed over! "+str(len(book_list)))					
			break
	return(book_list)
	
def data_load(input_file_name):

	# 打开数据库连接
	conn = pymysql.connect(host, user, passwd, database )
	cursor = conn.cursor()
	sql_str = get_sql_str()
	i = 0	
	with open(input_file_name,'r',encoding='utf-8') as fp:
		while(1):
			books = fp.readline()
			if( len(books)>0 ):
				#deal one page book.
				book_list = deal_one_page(books)
				if len(book_list) <= 0:
					print('deal one page Error! '+str(i))
					continue
				try:
					cursor.executemany(sql_str,book_list)
					if i%10 == 0:
						conn.commit()
						print('have dealed pages: '+str(i))
				except Exception as e:
					print('db deal Error! '+str(i))
					traceback.print_exc()
					continue
				i = i + 1
			else:
				print("all page books have dealed over! "+str(i))
				break;
			#break
				
	# 关闭数据库连接
	conn.commit()
	cursor.close()
	conn.close()
	
def update_book_meta_remark():
	connection  = pymysql.connect(host, user, passwd, database )
	i=0
	try:
		with connection.cursor() as cursor:
			print('connect ok...')
			with open("C:\\Users\\dayou\\Desktop\\11.csv",'r') as ff:
				print('open ok ...')
				line = ff.readline()
				print(line)
				while(len(line)>2):
					index=line.find(',')
					id1 = line[:index]
					id2 = line[index+1:-1]
					sql = "UPDATE book_meta SET remark = '%s' WHERE book_id = %s" % (id2,int(id1))
					#print(sql)
					cursor.execute(sql)
					i=i+1
					if(i%100 == 0):
						connection.commit()
						print('commit ok:'+str(i))
						time.sleep(1)
					#break;
					line=ff.readline()
				connection.commit()
	except:
		print (" fetch data Error: ...")
	
	connection.commit()
	connection.close()
	
if __name__ == '__main__':
	update_book_size()
	#update_book_meta_remark()
	#update_bookName()
	#print(get_book_id('thread-14634.htm'))
	#print(get_sql_str())
	
	#data_load('obook.txt')
	#data_load(sys.argv[1])
	#print_mysql_version()