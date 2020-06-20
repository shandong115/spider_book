import os, shutil
import datetime
import requests
import brotli
import codes
from codes import dict_codes
import traceback
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from lxml import etree
import time
#from pypinyin import lazy_pinyin, Style
#import pypinyin
from os.path import getsize


def parse_page_one_book(html):
	book_dict = {}
	html2 = etree.HTML(html, etree.HTMLParser())
	
	pan_type = html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//fieldset/table/tbody/tr/td[1]/a/text()')
	if(len(pan_type)>0):
		book_dict['pan_type'] = pan_type[0].strip()
	else:
		book_dict['pan_type'] =''
		
	pan_url = html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//fieldset/table/tbody/tr/td[1]/a/attribute::*[2]')
	if(len(pan_url)>0):
		book_dict['pan_url'] = pan_url[0].strip()
	else:
		book_dict['pan_url'] =''
	
	pan_code = html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//fieldset/table/tbody/tr/td[3]//input/attribute::*[4]')
	if(len(pan_code)>0):
		book_dict['pan_code'] = pan_code[0].strip()
	else:
		book_dict['pan_code'] =''
	
	on_shalf_date 	= html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/text()')
	if(len(on_shalf_date)>0):
		book_dict['on_shalf_date'] = on_shalf_date[0].strip()
	else:
		book_dict['on_shalf_date'] =''
	
	list_abstract 		= html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//div[1]//text()')
	if len(list_abstract) == 0:
		list_abstract 	= html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/p/text()')
		if len(list_abstract) == 0:
			list_abstract 	= html2.xpath('/html/body/main/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]//span/text()')
			if len(list_abstract) == 0:
				print('have not got abstract!')
	if len(list_abstract) > 0:
		ll=[]
		for la in list_abstract:
			str_tmp =la.strip('\u2003').strip()
			if str_tmp.find('&emsp') >0:
				str_tmp.replace('&emsp','',4)
			ll.append(str_tmp)
		
		abstract = str(ll)
		if(len(abstract)>4096):
			book_dict['abstract'] = abstract[:4095]
		else:
			book_dict['abstract'] = abstract
	else:
		book_dict['abstract'] = 'have no abstract!'
		
	#print(book_dict['pan_type'])
	#print(book_dict['pan_url'])
	#print(book_dict['pan_code'])
	#print(book_dict['on_shalf_date'])
	#print(len(str(book_dict['abstract'])))
	#print(len(book_dict['abstract']))
	#print(book_dict['abstract'])
	
	return book_dict

def get_one_page(url):
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'__cfduid=dcf6c63af2f4848e11e8975957a749b231587277319; bbs_sid=mku1ce0l8flsv4hihvr69ds914; _ga=GA1.2.2143680669.1587277427; __gads=ID=77c90ea56ccb0625:T=1587277418:S=ALNI_MbdqlI7X0aQx7xrq0x2FQ2ntV11jQ; __utma=52185463.2143680669.1587277427.1587321211.1587441826.5; __utmz=52185463.1587277433.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bbs_token=YsOeqi_2BTYkb49bGFNuwcTQKK6D_2B3rQZ7nbg7drbsCkxOaD5a1nX0DDOiw_2BBGe1aERhgAMCEyt5jAiej83vD33b8nqeA_3D; _gid=GA1.2.289808507.1587441826; __utmc=52185463; nciaer_popup=1',
		#'Host':url,	
		#'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'
		}

	try:
		response = requests.get(url, headers=headers,timeout=30)
		if not response.status_code == requests.codes.ok:
			print('Request Not Successfully: '+url + ',status_code:'+str(response.status_code)+'->'+dict_codes[response.status_code])
			return None
		print('Request Successfully: ' + url)
	except RequestException as e:
		print('Request Exception!'+url)
		traceback.print_exc()
		return None
		
	key = 'Content-Encoding'
	if(key in response.headers and response.headers['Content-Encoding'] == 'br'):
		data = brotli.decompress(response.content)
		data1 = data.decode('utf-8')
		return(data1)
	else:
		return(response.text)
		
def get_now_time():
	dt=datetime.datetime.now()
	return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_file_index_inpath(path):
	#path = "D:\\Ebook\\obook\\workplace\\out"

	files = os.listdir(path)
	values=[]
	for file in files:
		i = file.find('.txt', 0, len(file))
		v = file[5:i]
		if len(v) != 0:
			values.append(int(v))

	return(values)
	
def get_now_date():
	return time.strftime("%Y%m%d", time.localtime())
	
def get_file_name_first_letter(path):
	files = os.listdir(path)
	values=[]
	for file in files:
		print(file)
		first_letters=""
		first_letters=first_letters+"".join(lazy_pinyin(file,style=Style.FIRST_LETTER, errors='ignore'))
		print(first_letters)
		break

def compare_files():
	path = "D:\\book\\epub_book\\"
	path2 = "D:\\book\\wrong\\put\\"
	books = os.listdir(path)
	print("books num: "+str(len(books)))
	wrong=[]
	right = 0
	unright = 0
	noput = 0
	for book in books:
		book_size1 = getsize(path+book)
		flag = -1
		with open('filesize.txt', mode='r') as f:
			line = f.readline()
			while(line):
				book_name = line[:line.find('|')]
				if(book == book_name):
					book_size2 = int(line[line.find('|')+1:])
					if(book_size1 == int(book_size2)):
						#print(book + " has put! size: " + str(book_size1))
						flag = 0
						right=right+1
						break
					else:
						print(book + " put wrong size1: " + str(book_size1) + "size2: " + str(book_size2))
						wrong.append(book)
						unright=unright+1
						flag = 1
						#shutil.copy(path+book, path2)
						break
				line = f.readline()
			if(flag == -1):
				noput=noput+1
				#print(book + " hasnt put")
				#shutil.copy(path+book, path2)
	for w in wrong:
		print(w)
	print("noput: "+str(noput))
	print("right: "+str(right))
	print("unright: "+str(unright))


if __name__ == '__main__':
	compare_files()
	#get_file_name_first_letter("E:\\workplace\\python\\python-project\\book")
	#print(get_now_date())
#	with open('thread-7774.htm', 'r', encoding='utf-8') as fp:
#		parse_page_one_book(fp.read())
	
	#html = get_one_page('https://obook.cc/thread-7774.htm')
	#with open('thread-7774.htm', 'w', encoding='utf-8') as fp:
		#fp.write(html)
	#print(get_now_time())
	#path = "D:\\Ebook\\obook\\workplace\\out"
	
	#index_list = get_file_index_inpath(path)
	#print(str(index_list))
	#print(len(index_list))
	
