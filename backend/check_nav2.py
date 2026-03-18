import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 检查511880最新净值数据
cursor.execute('SELECT * FROM nav WHERE fund_code = "511880" ORDER BY id DESC LIMIT 3')
print("511880 净值数据:")
for row in cursor.fetchall():
    print(row)

conn.close()
