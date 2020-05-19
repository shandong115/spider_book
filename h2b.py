from html5print import HTMLBeautifier
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

fp=open(input_file, 'r', encoding='utf-8')
content = fp.read()
fp.close()

with open(output_file, 'w', encoding='utf-8') as fp:
	fp.write(HTMLBeautifier.beautify(content))
