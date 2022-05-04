import pymysql
from my_tapd_backend.prd_settings import DATABASES

connection = pymysql.connect(
    host=DATABASES['default']['HOST'],  # 服务器ip地址
    port=DATABASES['default']['PORT'],  # mysql默认端口号
    user=DATABASES['default']['USER'],  # 用户名
    password=DATABASES['default']['PASSWORD'],  # 密码
    charset="utf8",  # 字符集
)

my_cursor = connection.cursor()
# # 清空表
# sql = "SELECT concat('TRUNCATE TABLE ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'my_tapd_backend';"
# my_cursor.execute(sql)
# data = my_cursor.fetchall()
# for i in data:
#     print(i[0])
#     my_cursor.execute(i[0])
#     my_cursor.commit()
# # 删除表
# sql = "SELECT concat('DROP TABLE ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'my_tapd_backend';"
# my_cursor.execute(sql)
# data = my_cursor.fetchall()
# for i in data:
#     print(i[0])
#     my_cursor.execute(i[0])
#     my_cursor.commit()
sql = "DROP DATABASE my_tapd_backend IF EXISTS"
my_cursor.execute(sql)
sql = "CREATE DATABASE my_tapd_backend IF NOT EXISTS"
my_cursor.execute(sql)
connection.commit()
connection.close()
