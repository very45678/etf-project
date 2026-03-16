import sqlite3

# 连接数据库
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 查询最新价格数据
print('最新价格数据:')
cursor.execute('SELECT * FROM prices WHERE fund_code=? ORDER BY price_date DESC, id DESC LIMIT 5', ('511880',))
for row in cursor.fetchall():
    print(row)

# 查询最新净值数据
print('\n最新净值数据:')
cursor.execute('SELECT * FROM nav WHERE fund_code=? ORDER BY nav_date DESC, id DESC LIMIT 5', ('511880',))
for row in cursor.fetchall():
    print(row)

# 关闭连接
conn.close()