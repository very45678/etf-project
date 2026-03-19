# price_fetcher.py
import datetime
import time
import requests
import json
from data_store import insert_fund, insert_price, insert_error
from migrate_db import safe_insert_price

def fetch_etf_price(fund_code):
    """
    获取ETF价格数据 - 使用新浪财经API
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    try:
        print(f"开始获取ETF价格数据: {fund_code}")
        
        # 使用新浪财经API获取ETF实时行情
        # 基金代码格式：sh511880（上海）或 sz159915（深圳）
        exchange = "sh" if fund_code.startswith("5") else "sz"
        symbol = f"{exchange}{fund_code}"
        
        url = f"https://quotes.sina.cn/cn/api/quotes.php?symbol={symbol}&_={int(time.time()*1000)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 解析返回的数据
            data = response.json()
            
            if data and 'data' in data and len(data['data']) > 0:
                quote = data['data'][0]
                
                # 获取价格信息
                price = float(quote.get('price', 0))
                buy_price = float(quote.get('buy', 0)) if quote.get('buy') else price
                sell_price = float(quote.get('sell', 0)) if quote.get('sell') else price
                name = quote.get('name', f'基金{fund_code}')
                
                if price > 0:
                    price_date = datetime.date.today().strftime('%Y-%m-%d')
                    
                    # 使用安全插入方法
                    insert_fund(fund_code, name)
                    result = safe_insert_price(fund_code, price, price_date, buy_price, sell_price)
                    
                    if result:
                        print(f"ETF价格数据存储成功: {fund_code}")
                        print(f"名称: {name}")
                        print(f"最新价: {price}, 买入价: {buy_price}, 卖出价: {sell_price}")
                        return True
                    else:
                        raise ValueError("价格数据存储失败")
                else:
                    raise ValueError(f"基金代码 {fund_code} 的价格数据无效")
            else:
                raise ValueError(f"未找到基金代码 {fund_code} 的数据")
        else:
            raise ValueError(f"API请求失败: {response.status_code}")
        
    except Exception as e:
        print(f"价格数据采集失败: {str(e)}")
        insert_error('价格数据采集失败', str(e))
        return False

def fetch_all_funds():
    """
    获取所有货币基金数据
    :return: 成功获取的基金数量
    """
    fund_codes = ['511880', '511990']
    success_count = 0
    
    for fund_code in fund_codes:
        if fetch_etf_price(fund_code):
            success_count += 1
        time.sleep(2)  # 避免请求过于频繁
    
    return success_count

def get_fund_codes():
    """
    获取需要监控的基金代码列表
    :return: 基金代码列表
    """
    return ['511880', '511990']

def is_market_open():
    """
    检查市场是否开盘
    :return: 是否开盘
    """
    now = datetime.datetime.now()
    # 简单的开盘时间检查（周一至周五，9:30-15:00）
    if now.weekday() >= 5:  # 周六、周日
        return False
    if now.hour < 9 or (now.hour == 9 and now.minute < 30) or now.hour >= 15:
        return False
    return True

if __name__ == '__main__':
    # 测试数据采集
    print("开始采集数据...")
    success_count = fetch_all_funds()
    print(f"数据采集完成，成功获取 {success_count} 条数据")
