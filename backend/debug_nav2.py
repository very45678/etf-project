import sys
import os
sys.path.append(os.path.dirname(__file__))

from data_store import get_nav, get_prices

fund_code = '511880'

# 获取最新价格数据
prices = get_prices(fund_code=fund_code, limit=1)
print("get_prices返回:")
if prices:
    latest_price = prices[0]
    print(f"  返回类型: {type(latest_price)}")
    print(f"  返回值: {latest_price}")
    print(f"  price[2] (price): {latest_price[2]}")
    print(f"  price[3] (buy_price): {latest_price[3]}")
    print(f"  price[4] (sell_price): {latest_price[4]}")
    price_date = latest_price[5]
    print(f"  price[5] (price_date): {price_date}")
else:
    print("  没有数据")

# 获取净值数据
nav_data = get_nav(fund_code=fund_code, limit=10)
print("\nget_nav返回:")
print(f"  返回类型: {type(nav_data)}")
print(f"  返回数量: {len(nav_data)}")
if nav_data:
    print(f"  第一条数据: {nav_data[0]}")
    print(f"  nav[2]: {nav_data[0][2]}")
    print(f"  nav[3]: {nav_data[0][3]}")
