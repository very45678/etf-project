import sqlite3

# 连接数据库
conn = sqlite3.connect('etf_data.db')
cursor = conn.cursor()

# 查询511880基金的净值数据
cursor.execute('SELECT * FROM nav WHERE fund_code = ? ORDER BY nav_date DESC, id DESC LIMIT 10', ('511880',))
rows = cursor.fetchall()

print('数据库中的511880净值数据:')
for row in rows:
    print(f'ID: {row[0]}, 日期: {row[3]}, 净值: {row[2]}')

# 关闭连接
conn.close()