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
    获取ETF价格数据 - 使用新浪财经接口（添加买入价和卖出价采集）
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    try:
        print(f"开始获取ETF价格数据: {fund_code}")
        
        # 使用新浪财经接口获取ETF基金数据
        try:
            print("尝试使用新浪财经接口获取ETF基金数据...")
            df = ak.fund_etf_category_sina(symbol="ETF基金")
            print(f"获取到ETF基金数据，共 {len(df)} 条")
            
            # 查找指定基金代码的数据
            fund_data = None
            
            # 尝试不同的代码匹配方式
            # 方式1: 直接匹配代码列
            if '代码' in df.columns:
                fund_data = df[df['代码'] == fund_code]
            
            # 方式2: 如果方式1没找到，尝试匹配包含基金代码的行
            if fund_data is None or fund_data.empty:
                for idx, row in df.iterrows():
                    if str(fund_code) in str(row['代码']):
                        fund_data = df.iloc[[idx]]
                        break
            
            if fund_data is not None and not fund_data.empty:
                fund_name = fund_data.iloc[0]['名称']
                price_val = fund_data.iloc[0]['最新价']
                buy_price_val = fund_data.iloc[0]['买入'] if '买入' in fund_data.columns else None
                sell_price_val = fund_data.iloc[0]['卖出'] if '卖出' in fund_data.columns else None
                
                if price_val and str(price_val) not in ['None', '', 'nan']:
                    price = float(price_val)
                    buy_price = float(buy_price_val) if buy_price_val and str(buy_price_val) not in ['None', '', 'nan'] else None
                    sell_price = float(sell_price_val) if sell_price_val and str(sell_price_val) not in ['None', '', 'nan'] else None
                    
                    price_date = datetime.date.today().strftime('%Y-%m-%d')
                    
                    # 使用安全插入方法
                    from data_store import insert_fund
                    insert_fund(fund_code, fund_name)
                    
                    # 使用安全的价格插入方法
                    result = safe_insert_price(fund_code, price, price_date, buy_price, sell_price)
                    
                    if result:
                        print(f"ETF价格数据存储成功: {fund_code}")
                        print(f"名称: {fund_name}")
                        print(f"最新价: {price}")
                        print(f"买入价: {buy_price if buy_price else 'N/A'}")
                        print(f"卖出价: {sell_price if sell_price else 'N/A'}")
                        return True
                    else:
                        raise ValueError("价格数据存储失败")
                else:
                    raise ValueError(f"基金代码 {fund_code} 的价格数据无效")
            else:
                raise ValueError(f"未找到基金代码 {fund_code} 的数据")
                
        except Exception as e:
            print(f"新浪财经接口获取失败: {str(e)}")
            # 如果新浪财经接口失败，尝试其他备用方法
            try:
                print("尝试备用方法: 使用东方财富接口...")
                df = ak.fund_etf_spot_em()
                if not df.empty:
                    fund_data = df[df['代码'] == fund_code]
                    if not fund_data.empty:
                        fund_name = fund_data.iloc[0]['名称']
                        price_val = fund_data.iloc[0]['最新价']
                        
                        if price_val and str(price_val) not in ['None', '', 'nan']:
                            price = float(price_val)
                            price_date = datetime.date.today().strftime('%Y-%m-%d')
                            
                            from data_store import insert_fund
                            insert_fund(fund_code, fund_name)
                            
                            # 使用安全的价格插入方法
                            result = safe_insert_price(fund_code, price, price_date)
                            
                            if result:
                                print(f"备用方法成功: {fund_code}, 名称={fund_name}, 价格={price}")
                                return True
            except Exception as backup_error:
                print(f"备用方法也失败: {str(backup_error)}")
            
            raise ValueError(f"所有数据获取方法都失败: {str(e)}")
        
    except Exception as e:
        print(f"价格数据采集失败: {str(e)}")
        from data_store import insert_error
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