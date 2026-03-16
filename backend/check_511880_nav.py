import sqlite3

# 连接数据库
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 查询511880基金的最新5条净值数据
cursor.execute('SELECT * FROM nav WHERE fund_code = ? ORDER BY nav_date DESC, id DESC LIMIT 5', ('511880',))
results = cursor.fetchall()

print('511880基金的最新5条净值数据:')
for row in results:
    print(row)

# 关闭数据库连接
conn.close()