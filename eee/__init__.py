from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from eee.wsgi_adapter import wsgi_app
from eee.exceptions import URLExistsError, ViewFuncExistsError
from eee.helper import parse_static_key
from eee.route import Route
from eee.template_engine import replace_template
from eee.session import create_session_id, session
import os
import json


# 错误模板
ERROR_MAP = {
		'401': Response('<h1> 401 Unkown or unseported method</h1>', content_type='text/html; charset=utf-8', status=401),
		'404': Response('<h1> 404 Source Not Found</h1>', content_type='text/html; charset=utf-8', status=404),
		'503': Response('<h1> 503 Unkown Function Type</h1>', content_type='text/html; charset=utf-8', status=503)
	}

# 定义可支持文件类型
TYPE_MAP = {
		'css': 'text/css',
		'js': 'text/js',
		'png': 'image/png',
		'jpg': 'image/jpg',
		'jpeg': 'image/jpeg'
		
	}


class ExecFunc:
	
	def __init__(self, func, func_type, **options):
		"""
		:param func: 一个视图函数，用来指向url的处理视图函数
		:param func_type:指定类型：route(url),static(静态文件)，template（模板文件）
		:param options:其他可选参数
		"""
		self.func = func
		self.func_type = func_type
		self.options = options
		



class Eee:
	template_folder = None
	# 实例化方法
	def __init__(self, static_folder='static', template_folder='templates', session_path="session_"):
		# 默认IP 127.0.0.1
		self.host = '127.0.0.1'
		# 默认端口 8888
		self.port = 8888
		# 引入路由
		self.route = Route(self)
		# dict 一个关于url 和 endpoint 的映射字典
		self.url_map = {}
		self.static_map = {}
		# dict 一个关于endpoint 和 视图函数的映射字典
		self.function_map = {}
		# 静态文件夹
		self.static_folder = static_folder
		# 模板目录
		self.template_folder = template_folder
		# 初始化同时指定模板目录
		Eee.template_folder = template_folder
		# session持久化文件夹
		self.session_path = session_path
	
	def dispatch_static(self, static_path):
		"""
		静态资源访问函数，被路由分发函数所调配
		:param static_path: 请求资源路径
		:return:
		"""
		if os.path.exists(static_path):
			# 来源于helper模块，用于从url中提取文件路径
			key = parse_static_key(static_path)
			# 获取文件类型
			doc_type = TYPE_MAP.get(key, 'text/plain')
			try:
				with open(static_path, 'rb') as f:
					rep = f.read()
			except OSError as e:
				# 读取文件失败
				return ERROR_MAP['404']
			else:
				# 直接返回请求资源内容
				return Response(rep, content_type=doc_type)
			
		else:
			return ERROR_MAP['404']
	
	
	
	def dispatch_request(self, request):	
		"""
		路由分发函数
		request = Request(environ)
		:param request: 包含http请求信息的字典类型
		:return: Response 响应体
		"""
		# 获取http请求的cookies信息
		cookies = request.cookies
		# 判断用户是否第一次访问，如果是的话，设置一个session_id用于后续的会话维持
		if 'session_id' not in cookies:
			headers = {
					'Set-Cookie': 'session_id=%s' % create_session_id(),
					'Server': 'Eee provided'
				}
		else:
			headers = {
					'Server': 'Eee provided'
				}
		
		# 从http://www.baidu.com/get?key=XXX 这样的url中获取/get这样的资源符
		url = '/' + '/'.join(request.url.split('/')[3:]).split('?')[0]
		if url.startswith('/' + self.static_folder + '/'):
			# 判断请求的是否是静态资源，若满足，则设endpoint为static,表明应该使用静态的函数去处理
			# 静态资源有统一的视图函数来处理，所以将endpoint设为一个值，即：static
			endpoint = 'static'
			# 获取静态资源名
			url = url[1:]
		else:
			# 否则的话从url_map映射表中获取
			# 这个表的初始化由app创建者完成，即一个url对应一个视图
			endpoint = self.url_map.get(url, None)
		if endpoint is None:
			# 未找到相应的视图则返回：请求资源不存在404
			return ERROR_MAP['404']
		# 通过endpoint结点值， 从function_map中找到对应的试图处理函数
		exec_func = self.function_map[endpoint]
		# 如果函数类型为route,则进行路由分发，即匹配路由对应的视图
		if exec_func.func_type == 'route':
			# 判断请求方式是否合法
			if request.method in exec_func.options.get('methods'):
				argcount = exec_func.func.__code__.co_argcount
				
				if argcount > 0:
					rep = exec_func.func(request)
				else:
					rep = exec_func.func()
			else:
				return ERROR_MAP['401']
		elif exec_func.func_type == 'view':
			rep = exec_func.func(request)
		elif exec_func.func_type == 'static':
			return exec_func.func(url)
		else:
			return ERROR_MAP['503']
		
		status = 200
		content_type = 'text/html'
		if isinstance(rep, Response):
			return rep
		return Response(rep, content_type='%s; charset=UTF-8' % content_type,headers=headers, status=status)

	# bind_view()的包装函数
	def load_controller(self, controller):
		name = controller.__name__()
		
		for rule in controller.url_map:
			self.bind_view(rule['url'], rule['view'], name + '.' + rule['endpoint'])
	
	# 绑定url和视图类以及endpoint
	def bind_view(self, url, view_class, endpoint):
		self.add_url_rule(url, func=view_class.get_func(endpoint), func_type='view')
	
	# 具体加载url_map 和 function_map字典的生成函数
	def add_url_rule(self, url, func, func_type, endpoint=None, **options):
		if endpoint is None:
			endpoint = func.__name__
			
		if url in self.url_map:
			raise URLExistsError(url)
		
		if endpoint in self.function_map and func_type != 'static':
			raise ViewFuncExistsError
		
		self.url_map[url] = endpoint
		self.function_map[endpoint] = ExecFunc(func, func_type, **options)
		
	
	
	# app调用开始方法
	def run(self, host=None, port=None, **options):
		# 加载额外属性
		for key, value in options.items():
			if value is not None:
				self.__setattr__(key, value)
		# 指定ip和port
		if host:
			self.host = host
		if port:
			self.port = port
		# 指定static处理函数
		self.function_map['static'] = ExecFunc(func=self.dispatch_static, func_type='static')
		# 冲于session持久化操作
		if not os.path.exists(self.session_path):
			os.mkdir(self.session_path)
		# 获取session目录
		session.set_storage_path(self.session_path)
		# 加载session数据
		session.load_local_session()
		# 在调用run_simple的时候传入self,即我们自己创建的应用
		run_simple(hostname=self.host, port=self.port, application=self, **options)
		
	# 框架被WSGI调用入口方法
	def __call__(self, environ, start_response):
		return wsgi_app(self, environ, start_response)
		
		
# 模板引擎
def simple_template(path, **options):
	return replace_template(Eee, path, **options)

# 重定向
def redirect(url, status_code=302):
	response = Response('', status=status_code)
	response.headers['Location'] = url
	return response

# 用json格式返回数据
def render_json(data):
	content_type = 'text/plain'
	
	if isinstance(data, dict) or isinstance(data, list):
		data = json.dumps(data)
		content_type = 'application/json'

	return Response(data, content_type="%s;charset=UTF-8" % content_type, status=200)
	
# 返回文件格式
def render_file(file_path, file_name=None):
	if os.path.exists(file_path):
		with open(file_path, 'rb') as f:
			content = f.read()
		
		if file_name is None:
			file_name = file_path.split('/')[-1]
		
		headers = {
			'Content-Disposition': "attachment;filename=%s" % file_name
		}
		
		return Response(content, headers=headers, status=200)
	else:
		return ERROR_MAP['404'] 	
	
	
	
	
	
	
	
	
		