import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 查看错误的净值数据
cursor.execute('SELECT id, nav, nav_date FROM nav WHERE fund_code = "511880" AND nav > 101 ORDER BY id DESC')
print("错误的累计净值数据:")
for row in cursor.fetchall():
    print(row)

# 删除错误的净值数据（累计净值大于101的）
cursor.execute('DELETE FROM nav WHERE fund_code = "511880" AND nav > 101')
print(f"\n删除了 {cursor.rowcount} 条错误的净值数据")

# 确认删除后剩余的数据
cursor.execute('SELECT id, nav, nav_date FROM nav WHERE fund_code = "511880" ORDER BY id DESC LIMIT 5')
print("\n剩余最新的净值数据:")
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
