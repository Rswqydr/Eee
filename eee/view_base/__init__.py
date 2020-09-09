from eee.view import View
from eee.session import session, AuthSession
from eee import redirect

# 创建者须普遍继承的基类
class BaseView(View):
	
	# method限制了请求的方法
	method = ['GET', 'POST', 'PUT', 'DELETE']
	
	# 继承的子类实现具体的逻辑部分
	def get(self, request, *args, **options):
		pass
		
	def post(self, request, *args, **options):
		pass
	
	def put(self, request, *args, **options):
		pass
	
	def delete(self, request, *args, **options):
		pass
		
	
	def dispatch_request(self, request, *args, **options):
	# 请求处理函数	
		methods_meta = {
			'GET': self.get,
			'POST': self.post,
			'PUT': self.put,
			'DELETE': self.delete
		}
		
		if request.method in methods_meta:
			# 从加载的控制器中，获取映射关系，从而找到处理的视图
			return methods_meta[request.method](request, *args, **options)
		else:
			return '<h1>Unknown or unsupported request method</h1>'
		
		
class AuthLogin(AuthSession):
	
	@staticmethod
	def auth_fail_callback(request, *args, **options):
		return redirect('/login')
	
	@staticmethod
	def auth_logic(request, *args, **options):
		if 'user' in session.map(request):
			return True
		return False
		
class SessionView(BaseView):
	
	@AuthLogin.auth_session
	def dispatch_request(self, request, *args, **options):
		return super().dispatch_request(request, *args, **options)
		

		
		
		
		
		
		