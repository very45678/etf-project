import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'fund_arb.db')

def get_db_connection():
    """
    获取数据库连接
    :return: 数据库连接对象
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    """
    关闭数据库连接
    :param conn: 数据库连接对象
    """
    if conn:
        conn.close()