import pymysql

# 用于管理数据库连接的一个数据结构
class DBResult:
	suc = False
	result = None
	error = None
	rows = None
	
	# result下标为index的查询结果
	def index_of(self, index):
		if self.suc and isinstance(index, int) and self.rows > index >= -self.rows:
			return self.result[index]
		return None
	
	# 获取第一条查询结果
	def get_first(self):
		return self.index_of(0)
	
	# 获取最后一条查询结果
	def get_last(self):
		return self.index_of(-1)
	
	# 异常捕获装饰器
	@staticmethod
	def handler(func):
		def decorator(*args, **options):
			# 实例化
			ret = DBResult()
			
			# 捕获异常
			try:
				# 如果未捕获到异常，则将影响的行数以及结果存入ret中
				ret.rows, ret.result = func(*args, **options)
				ret.suc = True
			except Exception as e:
				# 如果捕获到异常，将放到对象.error里面
				ret.error = e
			
			return ret
		# 返回DBReult对象
		return decorator
	
	# 获取字典表示
	def to_dict(self):
		return {
			'suc': self.suc,
			'result': self.result,
			'error': self.error,
			'rows': self.rows
			}
			
			
			
class BaseDB:
	
	def __init__(self, user, password, database='', host='127.0.0.1', port=3306, charset='utf8', 
cursor_class=pymysql.cursors.DictCursor):
		self.user = user
		self.password = password
		self.host = host
		self.port = port
		self.database = database
		self.charset = charset
		self.cursor_class = cursor_class
		self.conn = self.connect()
		
	def connect(self):
		return pymysql.connect(host=self.host,port=self.port, user=self.user, passwd=self.password, db=self.database, charset=self.charset, cursorclass=self.cursor_class )
		
	def close(self):
		self.conn.close()
		
	@DBResult.handler
	def execut(self, sql, params=None):
		with self.conn as cursor:
			rows = cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execut(sql)
			result = cursor.fetchall()
		return rows, result 
		
	def insert(self, sql, params=None):
		ret = self.execut(sql, params)
		ret.result = self.conn.insert_id()
		
		return ret
		
	# 存储过程调用
	@DBResult.handler
	def process(self, func, params=None):
		with self.conn as cursor:
			rows = cursor.callproc(func, params) if params and isinstance(params, dict) else cursor.callproc(func)
			result = cursor.fetchall()
			
		return rows, result
		
	def create_db(self, db_name, db_charset='utf8'):
		return self.execut('CREATE DATABASE %s DEFAULT CHARACTER SET %s' % (db_name, db_charset))
		
	def delete_db(self, db_name):
		return self.execut('DELETE DATABASE %s' % db_name)
		
	@DBResult.handler
	def choose_db(self, db_name):
		self.conn.select_db(db_name)
			
		return None, None
		
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
		
			
			
			
			
			
			
			
			
			
			
			