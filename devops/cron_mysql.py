import pymysql
import os

db= pymysql.connect(host="192.168.37.150",user="root",password="123",db="ansible",port=3306)
cur = db.cursor()
sql = "select * from ServerAccount_account where user_check=0"
try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    print(results[0][5])
except Exception as e:
    raise e
finally:
    db.close()
