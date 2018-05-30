import os
import re
import json_lines
import urllib.parse

self.read_jl_file(
    urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/log_urbanlocker_3.jl')
)

def read_jl_file(self, file_path):
	error_url = []
	with open(file_path, 'rb') as f:
	    for item in json_lines.reader(f):
		if 'Spider error processing' in item['message']:
		    raw_errors = item['message']
		    error_url.append(re.findall('<GET (.*)>', raw_errors)[0])
	    return error_url

