
# 异常基类
class EeeException(Exception):
	
	def __init__(self, code='', message='Error'):
		self.code = code
		self.message = message
	
	def __str__(self):
		return self.message
		
# 视图错误异常
class ViewFuncExistsError(EeeException):
	
	def __init__(self, func_name, message='view func exists in views, view_name:'):
		super().__init__(message + str(func_name))
	
# url路径错误视图
class URLExistsError(EeeException):
	
	def __init__(self, URL_name, message='URL exists url_map, error URL:'):
		super().__init__(message + str(URL_name))

	