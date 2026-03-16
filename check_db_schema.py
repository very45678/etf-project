import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'fund_arb.db')

try:
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查表结构
    print("=== 检查数据库表结构 ===")
    
    # 检查funds表
    print("\n1. funds表结构:")
    cursor.execute("PRAGMA table_info(funds)")
    funds_columns = cursor.fetchall()
    for col in funds_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查prices表
    print("\n2. prices表结构:")
    cursor.execute("PRAGMA table_info(prices)")
    prices_columns = cursor.fetchall()
    for col in prices_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查nav表
    print("\n3. nav表结构:")
    cursor.execute("PRAGMA table_info(nav)")
    nav_columns = cursor.fetchall()
    for col in nav_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查yields表
    print("\n4. yields表结构:")
    cursor.execute("PRAGMA table_info(yields)")
    yields_columns = cursor.fetchall()
    for col in yields_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查alerts表
    print("\n5. alerts表结构:")
    cursor.execute("PRAGMA table_info(alerts)")
    alerts_columns = cursor.fetchall()
    for col in alerts_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查errors表
    print("\n6. errors表结构:")
    cursor.execute("PRAGMA table_info(errors)")
    errors_columns = cursor.fetchall()
    for col in errors_columns:
        print(f"  字段: {col[1]}, 类型: {col[2]}")
    
    # 检查数据
    print("\n=== 检查数据 ===")
    
    # 检查funds数据
    print("\n1. funds数据:")
    cursor.execute("SELECT * FROM funds")
    funds_data = cursor.fetchall()
    for fund in funds_data:
        print(f"  代码: {fund[1]}, 名称: {fund[2]}")
    
    # 检查nav数据
    print("\n2. nav数据:")
    cursor.execute("SELECT * FROM nav ORDER BY nav_date DESC LIMIT 5")
    nav_data = cursor.fetchall()
    for nav in nav_data:
        print(f"  代码: {nav[1]}, 净值: {nav[2]}, 日期: {nav[3]}")
    
    # 检查prices数据
    print("\n3. prices数据:")
    cursor.execute("SELECT * FROM prices ORDER BY price_date DESC LIMIT 5")
    prices_data = cursor.fetchall()
    for price in prices_data:
        print(f"  代码: {price[1]}, 价格: {price[2]}, 买入价: {price[3]}, 卖出价: {price[4]}, 日期: {price[5]}")
    
    # 检查yields数据
    print("\n4. yields数据:")
    cursor.execute("SELECT * FROM yields ORDER BY yield_date DESC LIMIT 5")
    yields_data = cursor.fetchall()
    for yield_item in yields_data:
        print(f"  代码: {yield_item[1]}, 收益率: {yield_item[2]}, 日期: {yield_item[3]}")
        if len(yield_item) > 5:
            print(f"  买入收益率: {yield_item[4]}, 卖出收益率: {yield_item[5]}")
    
    # 关闭连接
    conn.close()
    print("\n检查完成！")
    
except Exception as e:
    print(f"检查数据库失败: {e}")