import akshare as ak
import pandas as pd
import datetime

# 获取开放式基金数据
try:
    nav_data = ak.fund_open_fund_daily_em()
    fund_data = nav_data[nav_data['基金代码'] == '511880']
    if not fund_data.empty:
        print("在开放式基金接口找到511880数据:")
        print(fund_data.head())
        print("\n所有列名:")
        print(nav_data.columns.tolist())
    else:
        print("在开放式基金接口未找到511880数据")
except Exception as e:
    print(f"开放式基金接口错误: {e}")

# 尝试ETF基金接口
try:
    etf_data = ak.fund_etf_spot_em()
    etf_fund = etf_data[etf_data['代码'] == '511880']
    if not etf_fund.empty:
        print("\n在ETF接口找到511880数据:")
        print(etf_fund)
except Exception as e:
    print(f"ETF接口错误: {e}")

# 尝试货币基金接口
try:
    money_fund = ak.fund_money_fund_daily_em()
    mf = money_fund[money_fund['基金代码'] == '511880']
    if not mf.empty:
        print("\n在货币基金接口找到511880数据:")
        print(mf)
    else:
        print("\n在货币基金接口未找到511880数据")
except Exception as e:
    print(f"货币基金接口错误: {e}")
