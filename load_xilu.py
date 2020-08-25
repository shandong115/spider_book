import my_util
import sys
import os
from my_util import get_one_page2, parse_page
import datetime

if __name__ == '__main__':
	url = sys.argv[1]
	count = sys.argv[2]
	for i in range(int(count)):
		html=get_one_page2(url+'_'+str(i+1)+'.html')
		parse_page(html)
	#date = datetime.datetime.now().strftime('%Y%m%d')
	#test_path = "F:\\zhanlang\\"+date[2:]+"\\"
	#mkdirlambda =lambda x: os.makedirs(x) if not os.path.exists(x)  else True  # 目录是否存在,不存在则创建
	#mkdirlambda(test_path)
	