# price_fetcher.py
import datetime
import time
import requests
from data_store import insert_fund, insert_price, insert_error
from migrate_db import safe_insert_price

def fetch_etf_price_tencent(fund_code):
    """
    使用腾讯财经接口获取ETF价格数据
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    try:
        print(f"开始获取ETF价格数据: {fund_code}")
        
        # 腾讯财经接口
        # 沪市ETF代码格式: sh{code}
        url = f"https://qt.gtimg.cn/q=sh{fund_code}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://stock.finance.qq.com/',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 腾讯接口返回的是类似 JavaScript 的格式，需要解析
            content = response.text
            print(f"腾讯接口返回: {content[:200]}")
            
            # 解析数据格式: v_sh511880="1~银华日利~511880~100.035~100.035~100.035~..."
            if f'v_sh{fund_code}' in content:
                # 提取数据部分
                start = content.find(f'v_sh{fund_code}="') + len(f'v_sh{fund_code}="')
                end = content.find('";', start)
                data_str = content[start:end]
                
                # 分割数据
                parts = data_str.split('~')
                
                if len(parts) >= 45:
                    name = parts[1]  # 基金名称
                    price = parts[3]  # 最新价
                    bid = parts[9]    # 买一价
                    ask = parts[19]   # 卖一价
                    
                    if price and price != '0.000':
                        price_val = float(price)
                        bid_val = float(bid) if bid and bid != '0.000' else price_val
                        ask_val = float(ask) if ask and ask != '0.000' else price_val
                        # 精确到分钟的时间戳
                        price_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                        
                        # 存储数据
                        insert_fund(fund_code, name)
                        result = safe_insert_price(fund_code, price_val, price_date, bid_val, ask_val)
                        
                        if result:
                            print(f"价格数据存储成功: {fund_code}, 名称={name}, 价格={price_val}, 买一={bid_val}, 卖一={ask_val}")
                            return True
                        else:
                            raise ValueError("价格数据存储失败")
                    else:
                        raise ValueError(f"未获取到有效价格: {fund_code}")
                else:
                    raise ValueError(f"数据格式不正确: {parts}")
            else:
                raise ValueError(f"返回数据中未找到基金代码: {fund_code}")
        else:
            raise ValueError(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"腾讯财经接口获取失败: {str(e)}")
        return False

def fetch_etf_price_eastmoney(fund_code):
    """
    使用东方财富接口获取ETF价格数据（备用）
    """
    try:
        print(f"尝试使用东方财富接口获取: {fund_code}")
        
        # 东方财富接口
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=1.{fund_code}&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and data['data']:
                stock_data = data['data']
                
                name = stock_data.get('f58', f'基金{fund_code}')
                price = stock_data.get('f43')  # 最新价
                bid = stock_data.get('f44')    # 买一价
                ask = stock_data.get('f45')    # 卖一价
                
                if price:
                    price_val = float(price) / 100  # 东方财富价格需要除以100
                    bid_val = float(bid) / 100 if bid else price_val
                    ask_val = float(ask) / 100 if ask else price_val
                    # 精确到分钟的时间戳
                    price_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    insert_fund(fund_code, name)
                    result = safe_insert_price(fund_code, price_val, price_date, bid_val, ask_val)
                    
                    if result:
                        print(f"东方财富获取成功: {fund_code}, 名称={name}, 价格={price_val}")
                        return True
                else:
                    raise ValueError(f"未获取到有效价格")
            else:
                raise ValueError(f"返回数据为空")
        else:
            raise ValueError(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"东方财富接口获取失败: {str(e)}")
        return False

def fetch_etf_price(fund_code):
    """
    获取ETF价格数据 - 主函数
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    # 先尝试腾讯财经接口
    if fetch_etf_price_tencent(fund_code):
        return True
    
    # 失败则尝试东方财富
    print(f"腾讯接口失败，尝试东方财富...")
    if fetch_etf_price_eastmoney(fund_code):
        return True
    
    # 都失败则记录错误
    error_msg = f"所有接口都无法获取基金 {fund_code} 的价格数据"
    print(error_msg)
    insert_error('价格数据采集失败', error_msg)
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
    if now.weekday() >= 5:
        return False
    if now.hour < 9 or (now.hour == 9 and now.minute < 30) or now.hour >= 15:
        return False
    return True

if __name__ == '__main__':
    print("开始采集数据...")
    success_count = fetch_all_funds()
    print(f"数据采集完成，成功获取 {success_count} 条数据")
