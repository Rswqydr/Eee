from werkzeug.wrappers import Request


def wsgi_app(app, environ, start_response):
	"""
	WSGI 入口模板
	app 应用名
	enciron 服务器传来的请求
	start_response 响应载体
	"""
	request = Request(environ)
	response = app.dispatch_request(request)
	return response(environ, start_response)