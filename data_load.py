import sys
import ast
import pymysql
import traceback
from my_util import get_now_time

host 		= 'localhost'
database 	= 'bookdb'
user 		= 'dayou'
passwd 		= 'asdasd321321'

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

if __name__ == '__main__':
	#print(get_book_id('thread-14634.htm'))
	#print(get_sql_str())
	
	#data_load('obook.txt')
	
	data_load(sys.argv[1])