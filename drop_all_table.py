import pymysql
from my_tapd_backend.prd_settings import DATABASES

connection = pymysql.connect(
    host=DATABASES['default']['HOST'],  # 服务器ip地址
    port=DATABASES['default']['PORT'],  # mysql默认端口号
    user=DATABASES['default']['USER'],  # 用户名
    password=DATABASES['default']['PASSWORD'],  # 密码
    charset="utf8",  # 字符集
    db=DATABASES['default']['NAME']  # 数据库
)

my_cursor = connection.cursor()
sql = "SELECT concat('DROP TABLE ', table_name, ';') FROM information_schema.tables WHERE table_schema = 'my_tapd_backend';"
my_cursor.execute(sql)
data = my_cursor.fetchall()
for i in data:
    print(i[0])
    my_cursor.execute(i[0])
    my_cursor.commit()

my_cursor.close()
connection.close()
