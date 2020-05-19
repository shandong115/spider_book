# -*- coding:utf-8 -*-

import time
import sys

from  my_util import get_file_index_inpath, get_one_page, get_now_date

def main(offset):
	if offset == 1:
		url = 'https://obook.cc'
	else:
		url = 'https://obook.cc/index-'+str(offset)+'.htm'
		
	html = get_one_page(url)
	if not html is None:
		out_file = 'out\obook'+get_now_date()+'_'+str(offset)+'.txt'
		with open(out_file,'w',encoding='utf-8') as fp:
			fp.write(html)

def get_deletion_page():
	path = "D:\\Ebook\\obook\\workplace\\out"	
	index_list = get_file_index_inpath(path)
	for i in range(1,497):
		if i not in index_list:
			main(offset=i)
			time.sleep(7)
		
def get_all_page(num):
	for i in range(int(num)):
		main(offset=i+1)
		time.sleep(7)

def get_especial_page(num):
	main(num)
		
if __name__ == '__main__':
	get_especial_page(int(sys.argv[1]))
	#get_deletion_page()
	#get_all_page()