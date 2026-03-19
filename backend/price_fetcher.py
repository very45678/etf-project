# price_fetcher.py
import akshare as ak
import datetime
import time
import requests
from data_store import insert_fund, insert_price, insert_error
from migrate_db import safe_insert_price

def setup_session():
    """
    设置HTTP会话，提高网络连接稳定性
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    session.timeout = 10
    return session

def fetch_etf_price(fund_code):
    """
    获取ETF价格数据 - 使用AKShare的实时行情接口
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    try:
        print(f"开始获取ETF价格数据: {fund_code}")
        
        # 使用AKShare的基金实时行情接口
        try:
            print("尝试使用AKShare接口获取ETF基金数据...")
            
            # 使用 fund_etf_hist_em 获取历史数据（包含最新价格）
            df = ak.fund_etf_hist_em(symbol=fund_code, period="daily", 
                                     start_date="20240101", end_date="20251231",
                                     adjust="")
            
            if df is not None and len(df) > 0:
                # 获取最新一条数据
                latest_data = df.iloc[-1]
                
                # 获取收盘价作为最新价格
                price_val = latest_data.get('收盘', latest_data.get('close', None))
                
                if price_val is not None:
                    price = float(price_val)
                    price_date = datetime.date.today().strftime('%Y-%m-%d')
                    
                    # 获取基金名称
                    fund_name_map = {
                        '511880': '银华日利',
                        '511990': '华宝添益'
                    }
                    fund_name = fund_name_map.get(fund_code, f"基金{fund_code}")
                    
                    # 使用安全插入方法
                    insert_fund(fund_code, fund_name)
                    
                    # 使用安全的价格插入方法（买入价和卖出价暂时用收盘价代替）
                    result = safe_insert_price(fund_code, price, price_date, price, price)
                    
                    if result:
                        print(f"ETF价格数据存储成功: {fund_code}")
                        print(f"名称: {fund_name}")
                        print(f"最新价: {price}")
                        return True
                    else:
                        raise ValueError("价格数据存储失败")
                else:
                    raise ValueError(f"基金代码 {fund_code} 的价格数据无效")
            else:
                raise ValueError(f"未找到基金代码 {fund_code} 的数据")
                
        except Exception as e:
            print(f"AKShare接口获取失败: {str(e)}")
            # 如果失败，尝试使用实时行情接口
            try:
                print("尝试备用方法: 使用实时行情接口...")
                
                # 使用 stock_zh_a_spot_em 获取实时行情
                df = ak.stock_zh_a_spot_em()
                
                if df is not None and len(df) > 0:
                    # 查找指定基金代码
                    fund_data = None
                    for idx in range(len(df)):
                        row = df.iloc[idx]
                        code = str(row.get('代码', ''))
                        if fund_code in code:
                            fund_data = row
                            break
                    
                    if fund_data is not None:
                        fund_name = fund_data.get('名称', f'基金{fund_code}')
                        price_val = fund_data.get('最新价', None)
                        
                        if price_val is not None:
                            price = float(price_val)
                            price_date = datetime.date.today().strftime('%Y-%m-%d')
                            
                            insert_fund(fund_code, fund_name)
                            result = safe_insert_price(fund_code, price, price_date, price, price)
                            
                            if result:
                                print(f"备用方法成功: {fund_code}, 名称={fund_name}, 价格={price}")
                                return True
                        
                raise ValueError("备用方法未找到数据")
                
            except Exception as backup_error:
                print(f"备用方法也失败: {str(backup_error)}")
                raise
        
    except Exception as e:
        print(f"价格数据采集失败: {str(e)}")
        insert_error('价格数据采集失败', str(e))
        return False

def fetch_all_funds():
    """
    获取所有货币基金数据
    :return: 成功获取的基金数量
    """
    # 这里可以配置需要监控的货币基金列表
    fund_codes = ['511880', '511990']  # 示例基金代码
    success_count = 0
    
    for fund_code in fund_codes:
        # 获取价格数据
        if fetch_etf_price(fund_code):
            success_count += 1
        # 避免请求过于频繁
        time.sleep(2)
    
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
    import datetime
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
