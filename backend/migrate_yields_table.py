# migrate_yields_table.py
import sqlite3
import os
from db import get_db_connection, close_db_connection

def migrate_yields_table():
    """迁移yields表结构，添加yield_rate_buy和yield_rate_sell字段"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查yields表结构
        cursor.execute("PRAGMA table_info(yields)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"当前yields表字段: {columns}")
        
        # 如果缺少字段，添加它们
        if 'yield_rate_buy' not in columns:
            cursor.execute("ALTER TABLE yields ADD COLUMN yield_rate_buy REAL")
            print("添加yield_rate_buy字段")
        
        if 'yield_rate_sell' not in columns:
            cursor.execute("ALTER TABLE yields ADD COLUMN yield_rate_sell REAL")
            print("添加yield_rate_sell字段")
        
        conn.commit()
        close_db_connection(conn)
        print("yields表结构迁移完成")
        return True
    except Exception as e:
        print(f"迁移yields表结构失败: {e}")
        close_db_connection(conn)
        return False

if __name__ == "__main__":
    migrate_yields_table()