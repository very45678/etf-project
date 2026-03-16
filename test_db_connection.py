import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'fund_arb.db')

print(f"数据库文件路径: {DB_PATH}")
print(f"数据库文件是否存在: {os.path.exists(DB_PATH)}")

try:
    # 尝试连接数据库
    conn = sqlite3.connect(DB_PATH)
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