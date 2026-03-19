# d:\etf\backend\nav_fetcher.py
import akshare as ak
import datetime
import time
import re
from data_store import insert_fund, insert_nav, insert_error, has_nav_for_date

# 定义货币基金列表，这些基金的净值永远是100元
MONEY_FUNDS_WITH_FIXED_NAV = ['511990', '511800', '511850']

# 定义基金名称映射
FUND_NAME_MAP = {
    '511880': '银华日利',
    '511990': '华宝添益',
    '511800': '易方达货币',
    '511850': '财富宝ETF'
}

def fetch_fund_nav(fund_code, force_update=False):
    """
    使用akshare获取基金净值数据
    :param fund_code: 基金代码
    :param force_update: 是否强制更新，即使已有数据
    :return: 是否获取成功
    """
    try:
        print(f"开始获取基金净值数据: {fund_code}")
        
        # 特殊处理：对于固定净值的货币基金，直接返回100
        if fund_code in MONEY_FUNDS_WITH_FIXED_NAV:
            print(f"货币基金 {fund_code} 使用固定净值 100")
            nav = 100.0
            nav_date = datetime.date.today().strftime('%Y-%m-%d')
            fund_name = FUND_NAME_MAP.get(fund_code, f"货币基金{fund_code}")
            
            # 存储数据
            insert_fund(fund_code, fund_name)
            insert_nav(fund_code, nav, nav_date)
            
            print(f"基金净值数据存储成功: {fund_code}, 名称={fund_name}, 净值={nav}, 日期={nav_date}")
            return True
        
        # 使用akshare获取基金历史净值
        nav, nav_date, fund_name = fetch_fund_nav_from_akshare(fund_code)
        
        if nav is None:
            raise ValueError(f"无法获取基金净值数据: {fund_code}")
        
        # 检查是否已有该日期的数据（除非强制更新）
        if not force_update and has_nav_for_date(fund_code, nav_date):
            print(f"基金 {fund_code} 在 {nav_date} 的净值数据已存在，跳过采集")
            return True
        
        # 存储数据
        insert_fund(fund_code, fund_name)
        insert_nav(fund_code, nav, nav_date)
        
        print(f"基金净值数据存储成功: {fund_code}, 名称={fund_name}, 净值={nav}, 日期={nav_date}")
        return True
        
    except Exception as e:
        print(f"净值数据采集失败: {str(e)}")
        insert_error('净值数据采集失败', str(e))
        return False

def fetch_fund_nav_from_akshare(fund_code):
    """
    使用akshare获取基金历史净值数据
    """
    try:
        # 获取基金历史净值
        fund_nav_data = ak.fund_etf_hist_em(symbol=fund_code, period="daily", 
                                            start_date="20240101", end_date="20251231",
                                            adjust="")
        
        if fund_nav_data is not None and len(fund_nav_data) > 0:
            # 获取最新一条数据
            latest_data = fund_nav_data.iloc[-1]
            
            # 获取净值和日期
            nav_value = latest_data.get('收盘', latest_data.get('close', None))
            nav_date = latest_data.get('日期', latest_data.get('date', None))
            
            if nav_value is not None:
                # 获取基金名称
                fund_name = FUND_NAME_MAP.get(fund_code, f"基金{fund_code}")
                
                # 格式化日期
                if isinstance(nav_date, str):
                    nav_date = nav_date.replace('-', '')
                    nav_date = f"{nav_date[:4]}-{nav_date[4:6]}-{nav_date[6:8]}"
                else:
                    nav_date = datetime.date.today().strftime('%Y-%m-%d')
                
                return float(nav_value), nav_date, fund_name
        
        return None, None, None
        
    except Exception as e:
        print(f"从akshare获取净值失败: {str(e)}")
        return None, None, None

def fetch_all_funds_nav(force_update=False):
    """
    获取所有基金的净值数据
    """
    fund_codes = ['511880', '511990']
    
    for fund_code in fund_codes:
        fetch_fund_nav(fund_code, force_update)
        time.sleep(1)  # 避免请求过快

if __name__ == '__main__':
    fetch_all_funds_nav()
