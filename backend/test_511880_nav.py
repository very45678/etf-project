import akshare as ak
import datetime
import re
import pandas as pd

fund_code = '511880'

print(f"测试511880的净值获取")
print(f"当前日期: {datetime.date.today().strftime('%Y-%m-%d')}")
print("=" * 60)

# 测试方法1：开放式基金接口
print("\n方法1：开放式基金接口")
try:
    nav_data = ak.fund_open_fund_daily_em()
    print(f"获取到的基金数量: {len(nav_data)}")
    
    # 查找511880
    fund_data = nav_data[nav_data['基金代码'] == fund_code]
    if not fund_data.empty:
        print(f"找到511880的数据")
        latest_row = fund_data.iloc[0]
        print(f"基金名称: {latest_row.get('基金简称', '未知')}")
        
        # 查看所有列名
        print(f"列名: {list(nav_data.columns)}")
        
        # 尝试不同的净值字段
        nav_value = None
        nav_date = datetime.date.today().strftime('%Y-%m-%d')
        
        for col in nav_data.columns:
            if '净值' in col:
                if pd.notna(latest_row[col]) and latest_row[col] != '':
                    nav_value = latest_row[col]
                    # 尝试从字段名提取日期
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', col)
                    if date_match:
                        nav_date = date_match.group(1)
                    print(f"找到净值: {nav_value}, 日期: {nav_date} (来自字段: {col})")
                    break
        
        if nav_value is None:
            if '最新净值' in latest_row:
                nav_value = latest_row['最新净值']
                print(f"找到最新净值: {nav_value}")
            elif '单位净值' in latest_row:
                nav_value = latest_row['单位净值']
                print(f"找到单位净值: {nav_value}")
    else:
        print("未在开放式基金接口找到511880")
except Exception as e:
    print(f"开放式基金接口失败: {e}")

print("=" * 60)

# 测试方法2：ETF基金接口
print("\n方法2：ETF基金接口")
try:
    etf_data = ak.fund_etf_spot_em()
    print(f"获取到的ETF数量: {len(etf_data)}")
    
    # 查找511880
    fund_data = etf_data[etf_data['代码'] == fund_code]
    if not fund_data.empty:
        print(f"找到511880的数据")
        latest_row = fund_data.iloc[0]
        print(f"基金名称: {latest_row.get('名称', '未知')}")
        print(f"净值: {latest_row.get('净值', '未知')}")
        print(f"现价: {latest_row.get('现价', '未知')}")
        print(f"最新价: {latest_row.get('最新价', '未知')}")
        # 查看所有列名
        print(f"列名: {list(etf_data.columns)}")
    else:
        print("未在ETF基金接口找到511880")
except Exception as e:
    print(f"ETF基金接口失败: {e}")

print("=" * 60)

# 测试方法3：货币基金接口
print("\n方法3：货币基金接口")
try:
    money_fund_data = ak.fund_money_fund_daily_em()
    print(f"获取到的货币基金数量: {len(money_fund_data)}")
    
    # 查找511880
    fund_data = money_fund_data[money_fund_data['基金代码'] == fund_code]
    if not fund_data.empty:
        print(f"找到511880的数据")
        latest_row = fund_data.iloc[0]
        print(f"基金名称: {latest_row.get('基金简称', latest_row.get('名称', '未知'))}")
        print(f"七日年化收益率: {latest_row.get('七日年化收益率', '未知')}")
        print(f"每万份收益: {latest_row.get('每万份收益', '未知')}")
        print(f"单位净值: {latest_row.get('单位净值', '未知')}")
        print(f"日期: {latest_row.get('日期', latest_row.get('净值日期', '未知'))}")
        # 查看所有列名
        print(f"列名: {list(money_fund_data.columns)}")
    else:
        print("未在货币基金接口找到511880")
except Exception as e:
    print(f"货币基金接口失败: {e}")

print("=" * 60)
print("测试完成")