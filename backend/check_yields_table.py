import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查表结构
print('yields表结构:')
cursor.execute('PRAGMA table_info(yields)')
columns = cursor.fetchall()
for column in columns:
    print(column)

# 关闭连接
conn.close()