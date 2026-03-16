import unittest
import sqlite3
import os
import sys

# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../backend')

from db import get_db_connection, close_db_connection

class TestInitDB(unittest.TestCase):
    def test_tables_exist(self):
        """
        测试数据库表是否存在
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查funds表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funds'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查prices表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prices'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查nav表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nav'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查yields表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='yields'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查alerts表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alerts'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查errors表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='errors'")
        self.assertIsNotNone(cursor.fetchone())
        
        close_db_connection(conn)

if __name__ == '__main__':
    unittest.main()