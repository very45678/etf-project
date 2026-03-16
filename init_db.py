#!/usr/bin/env python3
# init_db.py - 初始化数据库

import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'backend', 'fund_arb.db')

# 确保backend目录存在
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if not os.path.exists(backend_dir):
    os.makedirs(backend_dir)
    print(f"创建backend目录: {backend_dir}")

# 连接数据库（如果不存在则创建）
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 创建表结构
print("创建表结构...")

# 基金表
cursor.execute('''
CREATE TABLE IF NOT EXISTS funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_code TEXT UNIQUE NOT NULL,
    fund_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 价格表
cursor.execute('''
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_code TEXT NOT NULL,
    price REAL,
    buy_price REAL,
    sell_price REAL,
    price_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
)
''')

# 净值表
cursor.execute('''
CREATE TABLE IF NOT EXISTS nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_code TEXT NOT NULL,
    nav REAL,
    nav_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
)
''')

# 收益率表
cursor.execute('''
CREATE TABLE IF NOT EXISTS yields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_code TEXT NOT NULL,
    yield_rate REAL,
    buy_yield REAL,
    sell_yield REAL,
    yield_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
)
''')

# 提醒表
cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_code TEXT NOT NULL,
    fund_name TEXT NOT NULL,
    yield_rate REAL,
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 错误表
cursor.execute('''
CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    error_type TEXT NOT NULL,
    error_message TEXT NOT NULL,
    error_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入初始基金数据
print("插入初始基金数据...")

# 插入银华日利
cursor.execute('''
INSERT OR IGNORE INTO funds (fund_code, fund_name) VALUES (?, ?)
''', ('511880', '银华日利'))

# 插入华宝添益
cursor.execute('''
INSERT OR IGNORE INTO funds (fund_code, fund_name) VALUES (?, ?)
''', ('511990', '华宝添益'))

# 提交事务
conn.commit()

# 检查基金数据
cursor.execute('SELECT * FROM funds')
funds = cursor.fetchall()
print(f"数据库初始化完成，基金数量: {len(funds)}")
for fund in funds:
    print(f"基金代码: {fund[1]}, 基金名称: {fund[2]}")

# 关闭连接
conn.close()

print("数据库初始化成功！")