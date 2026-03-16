# data_store.py
import sqlite3
import os
from db import get_db_connection, close_db_connection

def insert_fund(fund_code, fund_name):
    """
    插入基金信息
    :param fund_code: 基金代码
    :param fund_name: 基金名称
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO funds (fund_code, fund_name) VALUES (?, ?)', (fund_code, fund_name))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入基金信息失败: {e}")
        close_db_connection(conn)
        return False

def insert_price(fund_code, price, price_date, buy_price=None, sell_price=None):
    """
    插入价格数据（更新为支持买入价和卖出价）
    :param fund_code: 基金代码
    :param price: 最新价
    :param price_date: 价格日期
    :param buy_price: 买入价（可选）
    :param sell_price: 卖出价（可选）
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prices (fund_code, price, buy_price, sell_price, price_date) VALUES (?, ?, ?, ?, ?)', 
                      (fund_code, price, buy_price, sell_price, price_date))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入价格数据失败: {e}")
        close_db_connection(conn)
        return False

def insert_nav(fund_code, nav, nav_date):
    """
    插入净值数据
    :param fund_code: 基金代码
    :param nav: 净值
    :param nav_date: 净值日期
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO nav (fund_code, nav, nav_date) VALUES (?, ?, ?)', (fund_code, nav, nav_date))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入净值数据失败: {e}")
        close_db_connection(conn)
        return False

def insert_yield(fund_code, yield_rate_buy, yield_rate_sell, yield_date):
    """
    插入收益率数据（扩展为支持两种收益率）
    :param fund_code: 基金代码
    :param yield_rate_buy: 买入价收益率
    :param yield_rate_sell: 卖出价收益率
    :param yield_date: 收益率日期
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 使用yield_rate_buy作为yield_rate字段的值
        cursor.execute('INSERT INTO yields (fund_code, yield_rate, yield_date, yield_rate_buy, yield_rate_sell) VALUES (?, ?, ?, ?, ?)', 
                      (fund_code, yield_rate_buy, yield_date, yield_rate_buy, yield_rate_sell))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入收益率数据失败: {e}")
        close_db_connection(conn)
        return False

def insert_alert(fund_code, fund_name, yield_rate):
    """
    插入提醒记录
    :param fund_code: 基金代码
    :param fund_name: 基金名称
    :param yield_rate: 收益率
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO alerts (fund_code, fund_name, yield_rate) VALUES (?, ?, ?)', (fund_code, fund_name, yield_rate))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入提醒记录失败: {e}")
        close_db_connection(conn)
        return False

def insert_error(error_type, error_message):
    """
    插入错误记录
    :param error_type: 错误类型
    :param error_message: 错误消息
    :return: 是否插入成功
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO errors (error_type, error_message) VALUES (?, ?)', (error_type, error_message))
        conn.commit()
        close_db_connection(conn)
        return True
    except Exception as e:
        print(f"插入错误记录失败: {e}")
        close_db_connection(conn)
        return False

def get_funds(fund_code=None):
    """
    获取基金列表
    :param fund_code: 基金代码，None表示所有基金
    :return: 基金列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 只返回目标基金
        target_funds = ['511880', '511990']
        
        if fund_code:
            if fund_code in target_funds:
                cursor.execute('SELECT * FROM funds WHERE fund_code = ?', (fund_code,))
            else:
                return []
        else:
            placeholders = ','.join('?' for _ in target_funds)
            cursor.execute(f'SELECT * FROM funds WHERE fund_code IN ({placeholders})', target_funds)
            
        funds = cursor.fetchall()
        close_db_connection(conn)
        return funds
    except Exception as e:
        print(f"获取基金列表失败: {e}")
        close_db_connection(conn)
        return []

def get_prices(fund_code=None, limit=100):
    """
    获取基金价格数据
    :param fund_code: 基金代码，None表示获取所有基金
    :param limit: 返回数据条数限制
    :return: 价格数据列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 只返回目标基金
    target_funds = ['511880', '511990']
    
    try:
        if fund_code:
            if fund_code not in target_funds:
                return []
            query = "SELECT * FROM prices WHERE fund_code = ? ORDER BY price_date DESC, id DESC LIMIT ?"
            cursor.execute(query, (fund_code, limit))
        else:
            placeholders = ','.join('?' for _ in target_funds)
            query = f"SELECT * FROM prices WHERE fund_code IN ({placeholders}) ORDER BY price_date DESC, id DESC LIMIT ?"
            params = target_funds + [limit]
            cursor.execute(query, params)
        
        prices = cursor.fetchall()
        return prices
    except Exception as e:
        print(f"获取价格数据失败: {e}")
        return []
    finally:
        close_db_connection(conn)

def get_nav(fund_code=None, limit=100):
    """
    获取基金净值数据
    :param fund_code: 基金代码，None表示获取所有基金
    :param limit: 返回数据条数限制
    :return: 净值数据列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 只返回目标基金
    target_funds = ['511880', '511990']
    
    try:
        if fund_code:
            if fund_code not in target_funds:
                return []
            query = "SELECT * FROM nav WHERE fund_code = ? ORDER BY nav_date DESC, id DESC LIMIT ?"
            cursor.execute(query, (fund_code, limit))
        else:
            placeholders = ','.join('?' for _ in target_funds)
            query = f"SELECT * FROM nav WHERE fund_code IN ({placeholders}) ORDER BY nav_date DESC, id DESC LIMIT ?"
            params = target_funds + [limit]
            cursor.execute(query, params)
        
        navs = cursor.fetchall()
        return navs
    except Exception as e:
        print(f"获取净值数据失败: {e}")
        return []
    finally:
        close_db_connection(conn)

def get_yields(fund_code=None, limit=100):
    """
    获取收益率数据（扩展为返回两种收益率）
    :param fund_code: 基金代码，None表示所有基金
    :param limit: 返回数据条数
    :return: 收益率数据列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 只返回目标基金
        target_funds = ['511880', '511990']
        
        if fund_code:
            if fund_code not in target_funds:
                return []
            cursor.execute('SELECT * FROM yields WHERE fund_code = ? ORDER BY yield_date DESC, id DESC LIMIT ?', (fund_code, limit))
        else:
            placeholders = ','.join('?' for _ in target_funds)
            query = f"SELECT * FROM yields WHERE fund_code IN ({placeholders}) ORDER BY yield_date DESC, id DESC LIMIT ?"
            params = target_funds + [limit]
            cursor.execute(query, params)
            
        yields = cursor.fetchall()
        close_db_connection(conn)
        return yields
    except Exception as e:
        print(f"获取收益率数据失败: {e}")
        close_db_connection(conn)
        return []

def get_alerts(fund_code=None, limit=100):
    """
    获取提醒记录
    :param fund_code: 基金代码，None表示所有基金
    :param limit: 返回数据条数
    :return: 提醒记录列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 只返回目标基金
        target_funds = ['511880', '511990']
        
        if fund_code:
            if fund_code not in target_funds:
                return []
            cursor.execute('SELECT * FROM alerts WHERE fund_code = ? ORDER BY id DESC LIMIT ?', (fund_code, limit))
        else:
            placeholders = ','.join('?' for _ in target_funds)
            query = f"SELECT * FROM alerts WHERE fund_code IN ({placeholders}) ORDER BY id DESC LIMIT ?"
            params = target_funds + [limit]
            cursor.execute(query, params)
            
        alerts = cursor.fetchall()
        close_db_connection(conn)
        return alerts
    except Exception as e:
        print(f"获取提醒记录失败: {e}")
        close_db_connection(conn)
        return []

def get_errors(error_type=None, limit=100):
    """
    获取错误记录
    :param error_type: 错误类型，None表示所有类型
    :param limit: 返回数据条数
    :return: 错误记录列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if error_type:
            cursor.execute('SELECT * FROM errors WHERE error_type = ? ORDER BY id DESC LIMIT ?', (error_type, limit))
        else:
            cursor.execute('SELECT * FROM errors ORDER BY id DESC LIMIT ?', (limit,))
        errors = cursor.fetchall()
        close_db_connection(conn)
        return errors
    except Exception as e:
        print(f"获取错误记录失败: {e}")
        close_db_connection(conn)
        return []