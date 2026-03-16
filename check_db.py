import os
import sqlite3

# 数据库文件路径
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'fund_arb.db')

print(f"数据库文件路径: {db_path}")
print(f"数据库文件是否存在: {os.path.exists(db_path)}")
print(f"backend目录是否存在: {os.path.exists(os.path.join(os.path.dirname(__file__), 'backend'))}")

try:
    # 尝试连接数据库
    conn = sqlite3.connect(db_path)
    print("数据库连接成功")
    
    # 尝试执行简单查询
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM funds LIMIT 1')
    result = cursor.fetchone()
    print(f"查询结果: {result}")
    
    # 关闭连接
    conn.close()
    print("数据库连接关闭成功")
except Exception as e:
    print(f"数据库操作失败: {e}")