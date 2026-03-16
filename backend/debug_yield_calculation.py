# debug_yield_calculation.py
import logging
from yield_calculator import calculate_annualized_yield, calculate_yield_for_fund

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 手动测试511880基金的收益率计算
buy_price = 100.248
sell_price = 100.249
nav = 100.2474
days_held = 1

print("手动测试收益率计算:")
yield_rate_buy = calculate_annualized_yield(buy_price, nav, days_held)
yield_rate_sell = calculate_annualized_yield(sell_price, nav, days_held)
print(f"买入价收益率: {yield_rate_buy:.4f}%")
print(f"卖出价收益率: {yield_rate_sell:.4f}%")

# 测试完整的收益率计算流程
print("\n完整的收益率计算流程:")
calculate_yield_for_fund('511880')