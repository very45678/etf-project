# migrate_db.py
import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

def check_table_columns():
    """
    检查价格表是否包含买入价和卖出价字段
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取价格表的列信息
        cursor.execute("PRAGMA table_info(prices)")
        columns = cursor.fetchall()
        
        column_names = [column[1] for column in columns]
        
        print("价格表当前列信息:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")
        
        # 检查是否缺少买入价和卖出价字段
        missing_columns = []
        if 'buy_price' not in column_names:
            missing_columns.append('buy_price')
        if 'sell_price' not in column_names:
            missing_columns.append('sell_price')
        
        conn.close()
        
        return missing_columns
        
    except Exception as e:
        print(f"检查表结构失败: {e}")
        return []

def migrate_database():
    """
    迁移数据库表结构，添加缺失的字段
    """
    try:
        missing_columns = check_table_columns()
        
        if not missing_columns:
            print("数据库表结构已经是最新的，无需迁移")
            return True
        
        print(f"需要添加的字段: {missing_columns}")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 备份现有数据
        print("备份现有价格数据...")
        cursor.execute("SELECT * FROM prices")
        existing_data = cursor.fetchall()
        
        # 删除旧表
        print("删除旧的价格表...")
        cursor.execute("DROP TABLE IF EXISTS prices_old")
        cursor.execute("ALTER TABLE prices RENAME TO prices_old")
        
        # 创建新表（包含买入价和卖出价字段）
        print("创建新的价格表...")
        cursor.execute('''
        CREATE TABLE prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fund_code TEXT NOT NULL,
            price REAL NOT NULL,
            buy_price REAL,
            sell_price REAL,
            price_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (fund_code) REFERENCES funds (fund_code)
        )
        ''')
        
        # 恢复数据
        print("恢复价格数据...")
        for row in existing_data:
            # 根据旧表的列数决定如何插入数据
            if len(row) == 6:  # 旧表有6列（不包含buy_price和sell_price）
                cursor.execute('''
                INSERT INTO prices (id, fund_code, price, price_date, created_at)
                VALUES (?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[4], row[5]))
            else:
                # 如果有其他格式，使用通用方法
                cursor.execute('''
                INSERT INTO prices (fund_code, price, price_date)
                VALUES (?, ?, ?)
                ''', (row[1], row[2], row[4]))
        
        # 删除备份表
        cursor.execute("DROP TABLE prices_old")
        
        conn.commit()
        conn.close()
        
        print("数据库迁移完成！")
        return True
        
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        return False

def safe_insert_price(fund_code, price, price_date, buy_price=None, sell_price=None):
    """
    安全插入价格数据，如果表结构有问题会自动迁移
    """
    try:
        from data_store import insert_price
        return insert_price(fund_code, price, price_date, buy_price, sell_price)
    except Exception as e:
        if "no column named buy_price" in str(e) or "no column named sell_price" in str(e):
            print("检测到表结构问题，开始自动迁移...")
            if migrate_database():
                # 迁移成功后重试插入
                from data_store import insert_price
                return insert_price(fund_code, price, price_date, buy_price, sell_price)
            else:
                print("自动迁移失败，使用备用方法插入数据（不包含买入价和卖出价）")
                # 使用备用方法插入数据
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO prices (fund_code, price, price_date) VALUES (?, ?, ?)', 
                                  (fund_code, price, price_date))
                    conn.commit()
                    conn.close()
                    return True
                except Exception as e2:
                    print(f"备用方法插入数据失败: {e2}")
                    return False
        else:
            # 其他错误，直接抛出
            raise e

if __name__ == '__main__':
    print("开始检查数据库表结构...")
    missing_columns = check_table_columns()
    
    if missing_columns:
        print("检测到表结构不完整，开始迁移...")
        if migrate_database():
            print("数据库迁移成功！")
        else:
            print("数据库迁移失败！")
    else:
        print("数据库表结构完整，无需迁移")