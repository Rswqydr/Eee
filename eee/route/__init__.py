
# 用于用装饰器的方式来定义url
class Route:
	
	def __init__(self, app):
		self.app = app
		
	def __call__(self, url, **options):
		if 'methods' not in options:
			options['methods'] = 'GET'
			
		def decorator(f):
			# 他的本质还是掉用add_url_rule()方法，不过用装饰器装饰起来
			self.app.add_url_rule(url, f, 'route', **options)
			return f
			
		return decorator