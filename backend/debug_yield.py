import sys
import os
sys.path.append(os.path.dirname(__file__))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

from data_store import get_nav, get_prices

fund_code = '511880'

logger.info("开始调试...")

prices = get_prices(fund_code=fund_code, limit=1)
if prices:
    latest_price = prices[0]
    logger.info(f"价格数据: {latest_price}")
    
    buy_price = latest_price[3] if latest_price[3] else latest_price[2]
    sell_price = latest_price[4] if latest_price[4] else latest_price[2]
    price_date = latest_price[5]
    
    logger.info(f"buy_price: {buy_price}, type: {type(buy_price)}")
    logger.info(f"sell_price: {sell_price}, type: {type(sell_price)}")
    logger.info(f"price_date: {price_date}, type: {type(price_date)}")

nav_data = get_nav(fund_code=fund_code, limit=10)
logger.info(f"净值数据数量: {len(nav_data)}")

target_nav = None
for nav in nav_data:
    nav_date = nav[3]
    logger.info(f"检查净值日期: '{nav_date}' vs 价格日期: '{price_date}'")
    if nav_date == price_date:
        target_nav = nav
        logger.info("找到匹配的净值!")
        break

if not target_nav:
    target_nav = nav_data[0]
    logger.info(f"使用最新净值: {target_nav}")

nav_value = target_nav[2]
nav_date = target_nav[3]
logger.info(f"最终使用的nav_value: {nav_value}, type: {type(nav_value)}")
logger.info(f"最终使用的nav_date: {nav_date}")

# 计算天数
from datetime import datetime
price_dt = datetime.strptime(price_date, '%Y-%m-%d')
nav_dt = datetime.strptime(nav_date, '%Y-%m-%d')
days_held = abs((nav_dt - price_dt).days)
logger.info(f"价格日期: {price_dt}, 净值日期: {nav_dt}, 天数差: {days_held}")
