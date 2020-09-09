import base64
import time
import json
import os

# 创建一个session_id
def create_session_id():
	return base64.encodebytes(str(time.time()).encode()).decode().replace('=', '')[:-2][::-1]
	
# 从http请求的cookies中获取session_id
def get_session_id(request):
	return request.cookies.get('session_id', '')
	

class Session:
	
	_instance = None
	
	def __init__(self):
		# 初始化
		self.__session_map__ = {}
		self.__storage_path__ = None
		
	# 获取当前请求session_id用户的信息
	def map(self, request):
		return self.__session_map__.get(get_session_id(request), {})
	
	# 获取已经确定过session_id信息的具体信息
	def get(self, request, item):
		return self.map(request).get(item, None)
	
	# 获取session存储路径
	def set_storage_path(self, path):
		self.__storage_path__ = path
		
	# 将当前session信息保存到文件中
	def storage(self, session_id):
		session_path = os.path.join(self.__storage_path__, session_id)
		if self.__storage_path__ is not None:
			with open(session_path, 'wb') as f:
				content = json.dumps(self.__session_map__[session_id])
				f.write(base64.encodebytes(content.encode()))
			
	# 利用单例模式使得Session类只允许出现一个实例	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls, *args, **kwargs)
		return cls._instance
	
	# 存入session信息
	def push(self, request, item, value):
		session_id = get_session_id(request)
		if session_id in self.__session_map__:
			self.__session_map__[session_id][item] = value
		else:
			self.__session_map__[session_id] = {}
			self.__session_map__[session_id][item] = value
		self.storage(session_id)
	
	# 获取session信息
	def pop(self, request, item, value=True):
		session_id = get_session_id(request)
		current_session = self.__session_map__.get(session_id, {})
		if item in current_session:
			current_session.pop(item, value)
			self.storage(session_id)
		else:
			return "<h1>未登录<h1>"
			
	# 从本地加载用户session信息
	def load_local_session(self):
		if self.__storage_path__ is not None:
			session_id_list = os.listdir(self.__storage_path__)
			for session_id in session_id_list:
				path = os.path.join(self.__storage_path__, session_id)
				with open(path, 'rb') as f:
					content = f.read()
				content = base64.decodebytes(content)
				self.__session_map__[session_id] = json.loads(content.decode())

session = Session()


# 校验装饰器
# 校验方式为：
# 在auth_logic 为真的情况下返回auth_logic函数逻辑，否则返回auth_fail_callback函数逻辑
class AuthSession:
	
	@classmethod
	def auth_session(cls, f, *args, **options):
		def decorator(obj, request):
			return f(obj, request) if cls.auth_logic(request, *args, **options) else cls.auth_fail_callback(request, *args,
**options)
		return decorator
		
	@staticmethod
	def auth_logic(request, *args, **options):
		raise NotImplementedError
	
	@staticmethod
	def auth_fail_callback(request, *args, **options):
		raise NotImplementedError



















	
	
		