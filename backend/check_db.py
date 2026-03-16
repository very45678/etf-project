import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 查询所有表
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()

print('数据库中的表:')
for table in tables:
    print(table[0])

# 查询511880基金的净值数据
print('\n511880基金的净值数据:')
cursor.execute('SELECT * FROM nav WHERE fund_code = ? ORDER BY nav_date DESC, id DESC LIMIT 10', ('511880',))
navs = cursor.fetchall()
for nav in navs:
    print(f'ID: {nav[0]}, 日期: {nav[3]}, 净值: {nav[2]}')

# 查询511880基金的价格数据
print('\n511880基金的价格数据:')
cursor.execute('SELECT * FROM prices WHERE fund_code = ? ORDER BY price_date DESC, id DESC LIMIT 10', ('511880',))
prices = cursor.fetchall()
for price in prices:
    print(f'ID: {price[0]}, 日期: {price[5]}, 买入价: {price[3]}, 卖出价: {price[4]}')

# 关闭连接
conn.close()