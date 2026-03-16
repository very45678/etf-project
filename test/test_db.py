import unittest
from db import get_db_connection, close_db_connection

class TestDBConnection(unittest.TestCase):
    def test_get_db_connection(self):
        """
        测试获取数据库连接
        """
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        close_db_connection(conn)
    
    def test_close_db_connection(self):
        """
        测试关闭数据库连接
        """
        conn = get_db_connection()
        close_db_connection(conn)
        # 尝试使用已关闭的连接，应该抛出异常
        with self.assertRaises(Exception):
            conn.execute('SELECT 1')

if __name__ == '__main__':
    unittest.main()