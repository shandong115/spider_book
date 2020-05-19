from lxml import etree, html
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

fp=open(input_file, 'r', encoding='utf-8')
content = fp.read()
fp.close()

document_root = html.fromstring(content)
result = etree.tostring(document_root, encoding='utf-8', pretty_print=True)
with open(output_file,'w',encoding='utf-8') as f:
	f.write(result.decode('utf-8'))