# d:\etf\backend\nav_fetcher.py
import akshare as ak
import datetime
import time
import pandas as pd
import re
from data_store import insert_fund, insert_nav, insert_error

# 定义货币基金列表，这些基金的净值永远是100元
MONEY_FUNDS_WITH_FIXED_NAV = ['511990', '511800', '511850']

def fetch_fund_nav(fund_code):
    """
    使用akshare获取基金净值数据
    :param fund_code: 基金代码
    :return: 是否获取成功
    """
    try:
        print(f"开始获取基金净值数据: {fund_code}")
        
        # 特殊处理：对于固定净值的货币基金，直接返回100
        if fund_code in MONEY_FUNDS_WITH_FIXED_NAV:
            print(f"货币基金 {fund_code} 使用固定净值 100")
            nav = 100.0
            nav_date = datetime.date.today().strftime('%Y-%m-%d')
            fund_name = f"货币基金{fund_code}"
            
            # 尝试获取基金名称
            try:
                # 尝试从开放式基金接口获取名称
                nav_data = ak.fund_open_fund_daily_em()
                fund_data = nav_data[nav_data['基金代码'] == fund_code]
                if not fund_data.empty:
                    fund_name = fund_data.iloc[0]['基金简称']
            except:
                pass
            
            # 存储数据
            insert_fund(fund_code, fund_name)
            insert_nav(fund_code, nav, nav_date)
            
            print(f"基金净值数据存储成功: {fund_code}, 名称={fund_name}, 净值={nav}, 日期={nav_date}")
            return True
        
        # 方法1：尝试使用fund_open_fund_daily_em接口获取最新净值
        nav, nav_date, fund_name = fetch_latest_nav(fund_code)
        
        # 方法2：如果未找到数据，尝试使用ETF基金专用接口
        if nav is None:
            nav, nav_date, fund_name = fetch_etf_fund_nav(fund_code)
        
        # 方法3：如果未找到数据，尝试使用货币基金专用接口
        if nav is None:
            nav, nav_date, fund_name = fetch_money_fund_nav(fund_code)
        
        if nav is None:
            raise ValueError(f"无法获取基金净值数据: {fund_code}")
        
        # 存储数据
        insert_fund(fund_code, fund_name)
        insert_nav(fund_code, nav, nav_date)
        
        print(f"基金净值数据存储成功: {fund_code}, 名称={fund_name}, 净值={nav}, 日期={nav_date}")
        return True
        
    except Exception as e:
        print(f"净值数据采集失败: {str(e)}")
        insert_error('净值数据采集失败', str(e))
        return False

def fetch_latest_nav(fund_code):
    """
    使用fund_open_fund_daily_em接口获取最新净值数据
    """
    try:
        # 获取所有开放式基金的最新净值数据
        nav_data = ak.fund_open_fund_daily_em()
        
        # 查找指定基金代码的数据
        fund_data = nav_data[nav_data['基金代码'] == fund_code]
        
        if not fund_data.empty:
            print(f"在开放式基金接口找到数据: {fund_code}")
            
            # 获取最新数据
            latest_row = fund_data.iloc[0]
            
            # 获取基金名称
            if '基金简称' in latest_row:
                fund_name = latest_row['基金简称']
            else:
                fund_name = f"基金{fund_code}"
            
            # 查找净值相关字段
            nav_value = None
            nav_date = datetime.date.today().strftime('%Y-%m-%d')
            
            # 优先查找单位净值
            unit_nav_found = False
            for col in nav_data.columns:
                if '单位净值' in col and '累计' not in col:
                    if pd.notna(latest_row[col]) and latest_row[col] != '':
                        nav_value = latest_row[col]
                        unit_nav_found = True
                        # 尝试从字段名提取日期
                        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', col)
                        if date_match:
                            nav_date = date_match.group(1)
                        break
            
            # 如果没找到单位净值，再找其他净值字段（排除累计净值）
            if not unit_nav_found:
                for col in nav_data.columns:
                    if '净值' in col and '累计' not in col:
                        if pd.notna(latest_row[col]) and latest_row[col] != '':
                            nav_value = latest_row[col]
                            # 尝试从字段名提取日期
                            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', col)
                            if date_match:
                                nav_date = date_match.group(1)
                            break
            
            # 如果没有找到净值字段，尝试使用'最新净值'或其他可能的字段
            if nav_value is None:
                if '单位净值' in latest_row:
                    nav_value = latest_row['单位净值']
                elif '最新净值' in latest_row:
                    nav_value = latest_row['最新净值']
            
            if pd.notna(nav_value) and nav_value != '':
                return float(nav_value), nav_date, fund_name
            else:
                print(f"未找到有效净值数据: {fund_code}")
        else:
            print(f"在开放式基金接口未找到数据: {fund_code}")
        
        return None, None, None
        
    except Exception as e:
        print(f"获取最新净值失败: {str(e)}")
        return None, None, None

def fetch_money_fund_nav(fund_code):
    """
    使用fund_money_fund_daily_em接口获取货币基金净值数据
    """
    try:
        # 获取所有货币基金的最新净值数据
        money_fund_data = ak.fund_money_fund_daily_em()
        
        # 查找指定基金代码的数据
        fund_data = money_fund_data[money_fund_data['基金代码'] == fund_code]
        
        if not fund_data.empty:
            print(f"在货币基金接口找到数据: {fund_code}")
            
            # 获取最新数据
            latest_row = fund_data.iloc[0]
            
            # 获取基金名称
            if '基金简称' in latest_row:
                fund_name = latest_row['基金简称']
            elif '名称' in latest_row:
                fund_name = latest_row['名称']
            else:
                fund_name = f"基金{fund_code}"
            
            # 查找净值相关字段
            nav_value = None
            nav_date = datetime.date.today().strftime('%Y-%m-%d')
            
            # 尝试不同的净值字段
            if '七日年化收益率' in latest_row:
                # 对于货币基金，使用七日年化收益率作为参考
                # 注意：这里只是作为示例，实际应用中可能需要调整
                nav_value = latest_row['七日年化收益率']
            elif '每万份收益' in latest_row:
                # 每万份收益
                nav_value = latest_row['每万份收益']
            elif '单位净值' in latest_row:
                # 单位净值
                nav_value = latest_row['单位净值']
            
            # 尝试获取日期字段
            if '日期' in latest_row:
                nav_date = latest_row['日期']
            elif '净值日期' in latest_row:
                nav_date = latest_row['净值日期']
            
            if pd.notna(nav_value) and nav_value != '':
                return float(nav_value), nav_date, fund_name
            else:
                print(f"未找到有效净值数据: {fund_code}")
        else:
            print(f"在货币基金接口未找到数据: {fund_code}")
        
        return None, None, None
        
    except Exception as e:
        print(f"获取货币基金净值失败: {str(e)}")
        return None, None, None

def fetch_etf_fund_nav(fund_code):
    """
    使用fund_etf_spot_em接口获取ETF基金净值数据
    """
    try:
        # 获取所有ETF基金的最新数据
        etf_data = ak.fund_etf_spot_em()
        
        # 查找指定基金代码的数据
        fund_data = etf_data[etf_data['代码'] == fund_code]
        
        if not fund_data.empty:
            print(f"在ETF基金接口找到数据: {fund_code}")
            
            # 获取最新数据
            latest_row = fund_data.iloc[0]
            
            # 获取基金名称
            if '名称' in latest_row:
                fund_name = latest_row['名称']
            elif '基金简称' in latest_row:
                fund_name = latest_row['基金简称']
            else:
                fund_name = f"基金{fund_code}"
            
            # 查找净值相关字段
            nav_value = None
            nav_date = datetime.date.today().strftime('%Y-%m-%d')
            
            # 尝试不同的净值字段
            if '净值' in latest_row:
                nav_value = latest_row['净值']
            elif '单位净值' in latest_row:
                nav_value = latest_row['单位净值']
            elif '现价' in latest_row:
                # 对于ETF，也可以使用现价作为参考
                nav_value = latest_row['现价']
            elif '最新价' in latest_row:
                # 尝试另一种可能的字段名
                nav_value = latest_row['最新价']
            
            if pd.notna(nav_value) and nav_value != '':
                return float(nav_value), nav_date, fund_name
            else:
                print(f"未找到有效净值数据: {fund_code}")
        else:
            print(f"在ETF基金接口未找到数据: {fund_code}")
        
        return None, None, None
        
    except Exception as e:
        print(f"获取ETF基金净值失败: {str(e)}")
        return None, None, None

def fetch_all_funds_nav():
    """
    获取所有货币基金的净值数据
    :return: 成功获取的基金数量
    """
    # 这里可以配置需要监控的货币基金列表
    fund_codes = ['511880', '511990']  # 示例基金代码
    success_count = 0
    
    for fund_code in fund_codes:
        # 获取净值数据
        if fetch_fund_nav(fund_code):
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

def should_fetch_nav_today():
    """
    检查今天是否需要采集净值数据
    :return: 是否需要采集
    """
    import datetime
    now = datetime.datetime.now()
    # 净值数据通常每天只需要采集一次
    # 这里可以添加更复杂的逻辑，比如检查是否已经采集过今天的净值
    return True

if __name__ == '__main__':
    # 测试数据采集
    print("开始采集净值数据...")
    success_count = fetch_all_funds_nav()
    print(f"净值数据采集完成，成功获取 {success_count} 条数据")