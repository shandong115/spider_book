from lxml import etree, html
import sys
from bs4 import BeautifulSoup

input_file = sys.argv[1]
output_file = sys.argv[2]

fp=open(input_file, 'r', encoding='utf-8')
content = fp.read()
fp.close()

soup = BeautifulSoup(content, 'lxml')
with open(output_file,'w',encoding='utf-8') as f:
	f.write(soup.prettify())
