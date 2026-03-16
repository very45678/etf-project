
import sqlite3
import os
import logging
from datetime import datetime, timedelta
from db import get_db_connection, close_db_connection
from data_store import insert_error

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_cleanup')

def cleanup_old_data(days=5):
    """
    清理过期数据
    :param days: 保留最近几天的数据
    """
    conn = None
    try:
        # 计算过期时间
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"开始清理 {cutoff_date} 之前的数据...")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 清理价格数据
        cursor.execute('DELETE FROM prices WHERE price_date < ?', (cutoff_date,))
        prices_deleted = cursor.rowcount
        logger.info(f"清理了 {prices_deleted} 条价格数据")
        
        # 清理净值数据 (净值数据通常保留更久，这里暂时也按5天清理，或者可以保留更久)
        # 注意：净值数据表字段是 nav_date (DATE类型)，格式可能是 YYYY-MM-DD
        # 如果 nav_date 是 DATE 类型，比较时可能需要注意格式，但在 SQLite 中通常是字符串比较
        cursor.execute('DELETE FROM nav WHERE nav_date < ?', (cutoff_date[:10],))
        nav_deleted = cursor.rowcount
        logger.info(f"清理了 {nav_deleted} 条净值数据")
        
        # 清理收益率数据
        cursor.execute('DELETE FROM yields WHERE yield_date < ?', (cutoff_date,))
        yields_deleted = cursor.rowcount
        logger.info(f"清理了 {yields_deleted} 条收益率数据")
        
        # 清理提醒记录
        cursor.execute('DELETE FROM alerts WHERE alert_time < ?', (cutoff_date,))
        alerts_deleted = cursor.rowcount
        logger.info(f"清理了 {alerts_deleted} 条提醒记录")
        
        # 清理错误记录
        cursor.execute('DELETE FROM errors WHERE error_time < ?', (cutoff_date,))
        errors_deleted = cursor.rowcount
        logger.info(f"清理了 {errors_deleted} 条错误记录")
        
        conn.commit()
        
        logger.info("数据清理完成")
        return True
        
    except Exception as e:
        error_msg = f"数据清理失败: {str(e)}"
        logger.error(error_msg)
        insert_error('数据清理失败', str(e))
        return False
    finally:
        if conn:
            close_db_connection(conn)

if __name__ == '__main__':
    cleanup_old_data()
