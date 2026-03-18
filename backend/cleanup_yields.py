import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 删除收益率异常的数据
cursor.execute('DELETE FROM yields WHERE yield_rate > 1000')
print(f"删除了 {cursor.rowcount} 条异常收益率数据")

# 确认删除
cursor.execute('SELECT COUNT(*) FROM yields WHERE fund_code = "511880"')
print(f"剩余511880收益率数据: {cursor.fetchone()[0]}")

conn.commit()
conn.close()
