import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print('价格数据:')
try:
    cursor.execute('SELECT fund_code, price_date, buy_price, sell_price FROM prices ORDER BY price_date DESC LIMIT 10')
    prices = cursor.fetchall()
    for p in prices:
        print(p)
except Exception as e:
    print(f'获取价格数据失败: {e}')

print('\n净值数据:')
try:
    cursor.execute('SELECT fund_code, nav_date, nav FROM nav ORDER BY nav_date DESC LIMIT 10')
    navs = cursor.fetchall()
    for n in navs:
        print(n)
except Exception as e:
    print(f'获取净值数据失败: {e}')

# 关闭连接
conn.close()