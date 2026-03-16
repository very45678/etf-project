# api.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import sqlite3
import logging

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from data_store import get_funds, get_prices, get_nav, get_yields, get_alerts, get_errors
from scheduler import FundDataScheduler

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化数据库
def init_database():
    """初始化数据库，创建表结构和插入初始数据"""
    try:
        # 数据库文件路径
        db_path = os.path.join(os.path.dirname(__file__), 'fund_arb.db')
        print(f"数据库路径: {db_path}")
        
        # 连接数据库（如果不存在则创建）
        conn = sqlite3.connect(db_path)
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
    except Exception as e:
        print(f"数据库初始化失败: {e}")

import os

# 获取前端dist目录的路径
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')

app = Flask(__name__, static_folder=frontend_dist, static_url_path='/')
CORS(app)  # 启用CORS支持

# 初始化数据库
init_database()

# 启动定时任务调度器
scheduler = None
if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':  # 避免在Reload模式下启动两次
    try:
        scheduler = FundDataScheduler()
        scheduler.start_scheduler()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")

@app.route('/api/funds', methods=['GET'])
def get_funds_list():
    """
    获取基金列表API
    :return: 基金列表JSON
    """
    try:
        funds = get_funds()
        # 转换为字典列表
        funds_list = []
        for fund in funds:
            funds_list.append({
                'id': fund[0],
                'fund_code': fund[1],
                'fund_name': fund[2]
            })
        return jsonify({
            'status': 'success',
            'data': funds_list,
            'message': '获取基金列表成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取基金列表失败: {str(e)}'
        }), 500

@app.route('/api/prices', methods=['GET'])
def get_prices_list():
    """
    获取价格数据API
    :return: 价格数据JSON
    """
    try:
        # 获取查询参数
        fund_code = request.args.get('fund_code', None)
        limit = request.args.get('limit', 100, type=int)
        
        # 调用get_prices函数获取数据
        prices = get_prices(fund_code, limit)
        
        # 转换为字典列表
        prices_list = []
        for price in prices:
            prices_list.append({
                'id': price[0],
                'fund_code': price[1],
                'price': price[2],
                'buy_price': price[3],
                'sell_price': price[4],
                'price_date': price[5]
            })
        
        return jsonify({
            'status': 'success',
            'data': prices_list,
            'message': '获取价格数据成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取价格数据失败: {str(e)}'
        }), 500

@app.route('/api/nav', methods=['GET'])
def get_nav_list():
    """
    获取净值数据API
    :return: 净值数据JSON
    """
    try:
        # 获取查询参数
        fund_code = request.args.get('fund_code', None)
        limit = request.args.get('limit', 100, type=int)
        
        # 调用get_nav函数获取数据
        nav_data = get_nav(fund_code, limit)
        
        # 转换为字典列表
        nav_list = []
        for nav_item in nav_data:
            nav_list.append({
                'id': nav_item[0],
                'fund_code': nav_item[1],
                'nav': nav_item[2],
                'nav_date': nav_item[3]
            })
        
        return jsonify({
            'status': 'success',
            'data': nav_list,
            'message': '获取净值数据成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取净值数据失败: {str(e)}'
        }), 500

@app.route('/api/yields', methods=['GET'])
def get_yields_list():
    """
    获取收益率数据API
    :return: 收益率数据JSON
    """
    try:
        # 获取查询参数
        fund_code = request.args.get('fund_code', None)
        limit = request.args.get('limit', 100, type=int)
        
        # 调用get_yields函数获取数据
        yields_data = get_yields(fund_code, limit)
        
        # 转换为字典列表
        yields_list = []
        for yield_item in yields_data:
            yields_list.append({
                'id': yield_item[0],
                'fund_code': yield_item[1],
                'yield_rate': yield_item[2],
                'yield_date': yield_item[3],
                'yield_rate_buy': yield_item[5],
                'yield_rate_sell': yield_item[6]
            })
        
        return jsonify({
            'status': 'success',
            'data': yields_list,
            'message': '获取收益率数据成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取收益率数据失败: {str(e)}'
        }), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts_list():
    """
    获取提醒记录API
    :return: 提醒记录JSON
    """
    try:
        # 获取查询参数
        fund_code = request.args.get('fund_code', None)
        limit = request.args.get('limit', 100, type=int)
        
        # 调用get_alerts函数获取数据
        alerts_data = get_alerts(fund_code, limit)
        
        # 转换为字典列表
        alerts_list = []
        for alert in alerts_data:
            alerts_list.append({
                'id': alert[0],
                'fund_code': alert[1],
                'fund_name': alert[2],
                'yield_rate': alert[3],
                'created_at': alert[4] if len(alert) > 4 else None
            })
        
        return jsonify({
            'status': 'success',
            'data': alerts_list,
            'message': '获取提醒记录成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取提醒记录失败: {str(e)}'
        }), 500

@app.route('/api/errors', methods=['GET'])
def get_errors_list():
    """
    获取错误记录API
    :return: 错误记录JSON
    """
    try:
        # 获取查询参数
        error_type = request.args.get('error_type', None)
        limit = request.args.get('limit', 100, type=int)
        
        # 调用get_errors函数获取数据
        errors_data = get_errors(error_type, limit)
        
        # 转换为字典列表
        errors_list = []
        for error in errors_data:
            errors_list.append({
                'id': error[0],
                'error_type': error[1],
                'error_message': error[2],
                'created_at': error[3] if len(error) > 3 else None
            })
        
        return jsonify({
            'status': 'success',
            'data': errors_list,
            'message': '获取错误记录成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'获取错误记录失败: {str(e)}'
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """
    测试API端点，不依赖数据库
    :return: 测试数据JSON
    """
    try:
        return jsonify({
            'status': 'success',
            'data': [
                {'fund_code': '511880', 'fund_name': '银华日利'}, 
                {'fund_code': '511990', 'fund_name': '华宝添益'}
            ],
            'message': '测试API成功'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'data': [],
            'message': f'测试API失败: {str(e)}'
        }), 500

# 提供前端文件
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """提供前端文件"""
    # 优先从static_folder提供文件
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    # 否则返回index.html (SPA支持)
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # 开发环境使用
    app.run(debug=True, host='0.0.0.0', port=5001)