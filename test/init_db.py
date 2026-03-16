import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

def init_database():
    """
    初始化数据库表结构
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建基金信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT UNIQUE NOT NULL,
        fund_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建价格数据表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT NOT NULL,
        price REAL NOT NULL,
        price_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
    )
    ''')
    
    # 创建净值数据表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nav (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT NOT NULL,
        nav REAL NOT NULL,
        nav_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
    )
    ''')
    
    # 创建收益率数据表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS yields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT NOT NULL,
        yield_rate REAL NOT NULL,
        yield_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
    )
    ''')
    
    # 创建提醒记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_code TEXT NOT NULL,
        fund_name TEXT NOT NULL,
        yield_rate REAL NOT NULL,
        alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
    )
    ''')
    
    # 创建错误记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_type TEXT NOT NULL,
        error_message TEXT NOT NULL,
        error_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库表结构初始化完成")

if __name__ == '__main__':
    init_database()