import os
import re


pattern = r'{{(.*?)}}'

def parse_args(obj):
	comp = re.compile(pattern)
	ret = comp.findall(obj)
	return ret if ret else ()
	

def replace_template(app, path, **options):
	content = '<h1> Not Find template</h1>'
	path = os.path.join(app.template_folder, path)
	if os.path.exists(path):
		with open(path, 'rb') as f:
			content = f.read().decode('utf-8')
		args = parse_args(content)
		
		if options:
			for arg in args:
				key = arg.strip()
				content = content.replace('{{ %s }}'%arg, str(options.get(key, arg)))
	
	return content