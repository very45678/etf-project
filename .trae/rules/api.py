# api.py
from flask import Flask, jsonify, request
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from data_store import get_funds, get_prices, get_nav, get_yields

app = Flask(__name__)

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
                'yield_rate_buy': yield_item[3],
                'yield_rate_sell': yield_item[4],
                'yield_date': yield_item[5]
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)