from eee import Eee, redirect, render_json
from eee.view_base import BaseView
from eee.view import Controller
from eee import simple_template
from eee.view_base import SessionView
from eee.session import session
from database_conn import conn


app = Eee()


@app.route('/index', methods=['GET'])
def index():
	return simple_template('index.html')


class Index(BaseView):
	def get(self, request):
		return simple_template('index.html')
		
'''
# 首页视图, 需要登录才能看到
class Index(SessionView):
	def get(self, request):
		user = session.get(requests, 'user')
		return simple_template('index.html', user=user, message=' Eazy easy eficial ')
		
class Login(BaseView):
	def get(self, request):
		return simple_template('login.html')
	
	def post(self, request):
		user = request.form['user']
		session.push(request, 'user', user)
		ret = conn.insert('INSERT INTO user(f_name) VALUES %(user)s', request.form)
		if ret.suc:
			return redirect('/')
		else:
			return render_json(ret.to_dict().encode())
	
class Logout(SessionView):
	def get(self, request):
		session.pop(request, 'user')
		return "已退出<a href='/'>返回</a>"
		
'''	



eee_url_map = [
		{
			'url': '/index',
			'view': Index,
			'endpoint': 'index'
		}
		
	]


controller = Controller('index', eee_url_map)
app.load_controller(controller)


app.run(host='0.0.0.0', port=3389)