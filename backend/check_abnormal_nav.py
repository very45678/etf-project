import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM nav WHERE fund_code = "511880" AND nav > 101 ORDER BY id DESC LIMIT 5')
print("异常净值数据:")
for row in cursor.fetchall():
    print(row)
conn.close()
