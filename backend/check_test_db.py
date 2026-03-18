import sqlite3
# 检查另一个数据库
conn = sqlite3.connect('../test/fund_arb.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM nav WHERE fund_code = "511880" ORDER BY id DESC LIMIT 5')
print("test/fund_arb.db - 511880 净值数据:")
for row in cursor.fetchall():
    print(row)
conn.close()
