# d:\etf\backend\nav_fetcher.py
import datetime
import time
import requests
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
    获取基金净值数据 - 使用天天基金网API
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
        
        # 使用天天基金网API获取净值
        nav, nav_date, fund_name = fetch_nav_from_tiantian(fund_code)
        
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

def fetch_nav_from_tiantian(fund_code):
    """
    使用天天基金网API获取基金净值
    """
    try:
        # 天天基金网API
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 解析返回的JSONP数据
            text = response.text
            # 提取JSON部分
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                import json
                data = json.loads(text[start:end])
                
                nav = float(data.get('dwjz', 0))  # 单位净值
                nav_date = data.get('jzrq', datetime.date.today().strftime('%Y-%m-%d'))
                fund_name = data.get('name', FUND_NAME_MAP.get(fund_code, f"基金{fund_code}"))
                
                if nav > 0:
                    return nav, nav_date, fund_name
        
        return None, None, None
        
    except Exception as e:
        print(f"从天天基金网获取净值失败: {str(e)}")
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
