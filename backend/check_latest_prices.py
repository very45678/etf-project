import sqlite3

# 连接数据库
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 查询511880基金的最新5条价格数据
print('511880基金的最新5条价格数据:')
cursor.execute('SELECT * FROM prices WHERE fund_code = ? ORDER BY price_date DESC, id DESC LIMIT 5', ('511880',))
results = cursor.fetchall()

# 打印数据
for row in results:
    print(row)

# 关闭连接
conn.close()