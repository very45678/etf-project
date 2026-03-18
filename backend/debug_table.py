import sqlite3
conn = sqlite3.connect('fund_arb.db')
cursor = conn.cursor()

# 检查价格数据的字段
cursor.execute('PRAGMA table_info(prices)')
print("prices表结构:")
for row in cursor.fetchall():
    print(row)

print("\n511880最新价格数据:")
cursor.execute('SELECT * FROM prices WHERE fund_code = "511880" ORDER BY id DESC LIMIT 1')
for row in cursor.fetchall():
    print(row)
    print("索引0:", row[0])
    print("索引1 (fund_code):", row[1])
    print("索引2 (price):", row[2])
    print("索引3 (buy_price):", row[3])
    print("索引4 (sell_price):", row[4])
    print("索引5 (price_date):", row[5])

# 检查净值数据的字段
cursor.execute('PRAGMA table_info(nav)')
print("\nnav表结构:")
for row in cursor.fetchall():
    print(row)

print("\n511880最新净值数据:")
cursor.execute('SELECT * FROM nav WHERE fund_code = "511880" ORDER BY id DESC LIMIT 1')
for row in cursor.fetchall():
    print(row)
    print("索引0:", row[0])
    print("索引1 (fund_code):", row[1])
    print("索引2 (nav):", row[2])
    print("索引3 (nav_date):", row[3])

conn.close()
