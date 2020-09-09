from eee.dbconnector import BaseDB


# 示例连接
db_user = 'root'
db_password = 'Wsad123456;'
db_database = 'shiyanlou'

try:
	conn = BaseDB(db_user, db_password, db_database)
except Exception as e:
	# code, _ = e.args
	
	# if code == 1049:
	if e:
		create_table = \
'''
CREATE TABLE user(
	id INT PRIMARY KEY AUTO_INCREMENT,
	f_name VARCHAR(50) 	UNIQUE
)CHARSET=utf8
'''
		conn = BaseDB(db_user, db_password)
		ret = conn.create_db(db_database)
		if ret.suc:
			ret = conn.choose_db(db_database)
			
			if ret.suc:
				ret = conn.execut(create_table)
				
		if not ret:
			conn.delete_db(db_database)
			print(ret.error.args)
			exit()
	else:
		print(e)
		exit()
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				