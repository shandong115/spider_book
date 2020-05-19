import sys
from bs4 import BeautifulSoup
import json
import os

def parse_one_page(html):
	soup = BeautifulSoup(html, 'lxml')
	i=1
	for ul in soup.find_all(name='ul', attrs = {'class':'list-unstyled threadlist mb-0'}):
		books = []
		for li in ul.find_all(name='li'):
			img_path = li.img.attrs['src']
			for div in li.find_all(name='div', attrs = {'class':'ob-list-subject break-all'}):
				j=0
				for a in div.find_all(name='a'):
					if j==0:
						ebook_type = a.string
					else:
						book_name = a.string
						book_href = a.attrs['href']
					j = j + 1
				
			for div in li.find_all(name='div', attrs = {'class':'d-flex justify-content-between small mt-1'}):
				book_type = ''
				for a in div.find_all(name='a'):
					if len(book_type) == 0:
						book_type = a.string
					else:
						book_type = book_type + "|"+ a.string
				
			for div in li.find_all(name='div', attrs = {'class':'text-muted small'}):
				read_num = div.find('span', attrs={'class':'m-r-1'}).get_text()
				r_num = div.find('span', attrs={'class':'ml-2 d-none'}).get_text()
				remark_num = div.find('span', attrs={'class':'ml-2'}).get_text()
			
			book = {
				'index':i,
				'book_name':book_name,
				'img_path':img_path,
				'ebook_type':ebook_type,
				'book_href':book_href,
				'book_type':book_type,
				'read_num':read_num,
				#'pan_url':'',
				#'pan_code':'',
				#'on_time':'',
				#'abstract':'',
				'is_ok':'0'
				}
			books.append(book)
			i = i + 1
	return(str(books))

	
def write_to_json(content, output_file):
	with open(output_file, 'a', encoding='utf-8') as f:
		jsonObj = json.dumps(content,indent=4,sort_keys=True)
		f.write(str(jsonObj)+'\n')
		f.write(str(content))

def deal_all_pages(output_file):

	#output_file = sys.argv[1]
	path = "D:\\Ebook\\obook\\workplace\\out"

	files = os.listdir(path)
	with open(output_file, 'w', encoding='utf-8') as ff:
		ii=0
		for file in files:
			fp=open('out\\'+file, 'r', encoding='utf-8')
			content = fp.read()
			fp.close()
			
			ff.write(parse_one_page(content)+'\n')
			ii=ii+1
			if(ii%10 == 0):
				print('have dealed num:'+str(ii))
			
def deal_one_page(input_file, output_file):
	with open(output_file, 'w', encoding='utf-8') as ff:
		with open(input_file, 'r', encoding='utf-8') as fp:
			content = fp.read()
		ff.write(parse_one_page(content))
	print('have dealed one page.'+input_file+' to '+output_file)

	
if __name__ == '__main__':
	#input_file = sys.argv[1]
	#output_file = sys.argv[2]
	#deal_one_page(input_file, output_file)
	output_file = sys.argv[1]
	deal_all_pages(output_file)