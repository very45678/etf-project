import os
import sqlite3

# 数据库文件路径
DB_PATH = os.path.join('backend', 'fund_arb.db')

print(f"检查数据库文件: {DB_PATH}")
print(f"文件是否存在: {os.path.exists(DB_PATH)}")

# 初始化数据库
if not os.path.exists(DB_PATH):
    print("数据库文件不存在，开始创建...")
    
    # 确保backend目录存在
    if not os.path.exists('backend'):
        os.makedirs('backend')
    
    # 连接数据库（如果不存在会自动创建）
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建funds表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT UNIQUE,
        fund_name TEXT
    )''')
    
    # 创建prices表（添加买入价和卖出价字段）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT,
        price REAL,
        buy_price REAL,
        sell_price REAL,
        price_date TEXT
    )''')
    
    # 创建nav表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nav (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT,
        nav REAL,
        nav_date TEXT
    )''')
    
    # 创建yields表（添加买入和卖出收益率字段）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS yields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT,
        yield_rate REAL,
        yield_date TEXT,
        yield_rate_buy REAL,
        yield_rate_sell REAL
    )''')
    
    # 创建alerts表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT,
        fund_name TEXT,
        yield_rate REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 创建errors表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type TEXT,
        error_message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 插入初始基金数据
    funds_data = [
        ('511880', '银华日利'),
        ('511990', '华宝添益')
    ]
    cursor.executemany('INSERT OR IGNORE INTO funds (fund_code, fund_name) VALUES (?, ?)', funds_data)
    
    conn.commit()
    conn.close()
    print("数据库初始化完成")
else:
    print("数据库文件已存在")
    # 检查funds表是否有数据
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM funds')
    funds = cursor.fetchall()
    print(f"funds表中的数据: {funds}")
    conn.close()