
# 视图基类
class View:
	# 支持的请求方法
	methods = None
	
	# 请求函数处理映射
	methods_meta = None
	
	def dispatch_request(self, request, *args, **options):
		raise NotImplementedError
	
	
	# 参数name就是结点名
	@classmethod
	def get_func(cls, name):
		
		def func(*args, **kwargs):
			# 创建的obj是当前类的对象
			obj = func.view_class()
			# 调用的是类中的处理视图方法
			return obj.dispatch_request(*args, **kwargs)
		# view_class 指向当前类
		func.view_class = cls
		func.__name__ = name
		func.methods = cls.methods
		func.__doc__ = cls.__doc__
		func.__module__ = cls.__module__
		
		return func
		

class Controller:
	''' 控制器类 '''
	def __init__(self, name, url_map):
		# 一个类型为dict的list类型，存放的是映射关系
		self.url_map = url_map
		# 控制器名
		self.name = name
		
	def __name__(self):
		return self.name
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	