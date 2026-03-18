import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 检查511880最新价格数据
cursor.execute('SELECT * FROM prices WHERE fund_code = "511880" ORDER BY id DESC LIMIT 3')
print("511880 价格数据:")
for row in cursor.fetchall():
    print(row)

print()

# 检查511880最新收益率数据
cursor.execute('SELECT * FROM yields WHERE fund_code = "511880" ORDER BY id DESC LIMIT 3')
print("511880 收益率数据:")
for row in cursor.fetchall():
    print(row)

conn.close()
