from data_store import get_nav, get_prices
import datetime

fund_code = '511880'

# 获取最新价格数据
prices = get_prices(fund_code=fund_code, limit=1)
if prices:
    latest_price = prices[0]
    print("价格数据:", latest_price)
    print("price[2] (price):", latest_price[2])
    print("price[3] (buy_price):", latest_price[3])
    print("price[4] (sell_price):", latest_price[4])
    price_date = latest_price[5]
    print("price[5] (price_date):", price_date)

# 获取净值数据
nav_data = get_nav(fund_code=fund_code, limit=10)
print("\n净值数据:")
for nav in nav_data[:5]:
    print(nav)

# 查找匹配的净值
if prices and nav_data:
    price_date = prices[0][5]
    print(f"\n价格日期: {price_date}")
    for nav in nav_data:
        nav_date = nav[3]
        print(f"净值日期: {nav_date}, 是否匹配: {nav_date == price_date}")
        if nav_date == price_date:
            print(f"匹配的净值: {nav[2]}")
            break
    else:
        print(f"\n没有匹配的日期，使用最新净值: {nav_data[0][2]}")
