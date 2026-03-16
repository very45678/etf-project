import sqlite3
import os

def check_price_yield_data():
    """
    检查数据库中的价格和收益率数据
    """
    try:
        # 数据库文件路径
        db_path = os.path.join(os.path.dirname(__file__), 'fund_arb.db')
        print(f"数据库文件路径: {db_path}")
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查prices表数据
        print("\n检查prices表数据:")
        cursor.execute("SELECT * FROM prices LIMIT 10")
        prices = cursor.fetchall()
        print(f"prices表数据条数: {len(prices)}")
        for price in prices:
            print(price)
        
        # 检查yields表数据
        print("\n检查yields表数据:")
        cursor.execute("SELECT * FROM yields LIMIT 10")
        yields = cursor.fetchall()
        print(f"yields表数据条数: {len(yields)}")
        for yield_data in yields:
            print(yield_data)
        
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == '__main__':
    check_price_yield_data()