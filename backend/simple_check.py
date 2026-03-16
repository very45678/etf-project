import sqlite3
import os

def simple_check():
    """
    简单检查数据库连接和表结构
    """
    try:
        # 数据库文件路径
        db_path = os.path.join(os.path.dirname(__file__), 'fund_arb.db')
        print(f"数据库文件路径: {db_path}")
        print(f"数据库文件是否存在: {os.path.exists(db_path)}")
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        print("成功连接数据库")
        
        # 检查funds表是否存在
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funds'")
        result = cursor.fetchone()
        print(f"funds表是否存在: {result is not None}")
        
        # 插入一条测试数据
        try:
            cursor.execute("INSERT OR IGNORE INTO funds (fund_code, fund_name) VALUES (?, ?)", ('000001', '华夏成长混合'))
            conn.commit()
            print("插入测试数据成功")
        except Exception as e:
            print(f"插入测试数据失败: {e}")
        
        # 查询数据
        cursor.execute("SELECT * FROM funds")
        funds = cursor.fetchall()
        print(f"查询到的基金数量: {len(funds)}")
        for fund in funds:
            print(fund)
        
        # 关闭连接
        cursor.close()
        conn.close()
        print("数据库连接已关闭")
        
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == '__main__':
    simple_check()