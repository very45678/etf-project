import sqlite3
from datetime import datetime

def debug_511880_yield():
    """调试511880的收益率计算"""
    try:
        conn = sqlite3.connect('fund_arb.db')
        cursor = conn.cursor()
        
        # 查询511880的最新价格数据
        print("=== 511880最新价格数据 ===")
        cursor.execute('SELECT * FROM prices WHERE fund_code = ? ORDER BY price_date DESC LIMIT 5', ('511880',))
        price_rows = cursor.fetchall()
        print('id | fund_code | price | buy_price | sell_price | price_date | created_at')
        print('-' * 120)
        for row in price_rows:
            print(row)
        
        # 查询511880的最新净值数据
        print("\n=== 511880最新净值数据 ===")
        cursor.execute('SELECT * FROM nav WHERE fund_code = ? ORDER BY nav_date DESC LIMIT 5', ('511880',))
        nav_rows = cursor.fetchall()
        print('id | fund_code | nav | nav_date | created_at')
        print('-' * 80)
        for row in nav_rows:
            print(row)
        
        # 模拟收益率计算过程
        print("\n=== 收益率计算过程 ===")
        if price_rows and nav_rows:
            latest_price = price_rows[0]
            buy_price = latest_price[3] if latest_price[3] else latest_price[2]
            sell_price = latest_price[4] if latest_price[4] else latest_price[2]
            price_date = latest_price[5]
            
            print(f"最新价格数据:")
            print(f"  价格日期: {price_date}")
            print(f"  最新价: {latest_price[2]}")
            print(f"  买入价: {buy_price}")
            print(f"  卖出价: {sell_price}")
            
            # 查找与价格日期最接近的净值数据
            target_nav = None
            for nav in nav_rows:
                nav_date = nav[3]
                if nav_date == price_date:
                    target_nav = nav
                    break
            
            if not target_nav:
                target_nav = nav_rows[0]
                print(f"\n未找到与价格日期匹配的净值数据，使用最新净值:")
            else:
                print(f"\n找到与价格日期匹配的净值数据:")
            
            nav_value = target_nav[2]
            nav_date = target_nav[3]
            
            print(f"  净值日期: {nav_date}")
            print(f"  净值: {nav_value}")
            
            # 计算持有天数
            try:
                price_dt = datetime.strptime(price_date, '%Y-%m-%d')
                nav_dt = datetime.strptime(nav_date, '%Y-%m-%d')
                days_held = (nav_dt - price_dt).days
                if days_held <= 0:
                    days_held = 1
                print(f"  持有天数: {days_held}")
            except Exception as e:
                days_held = 1
                print(f"  日期解析失败，默认持有天数: {days_held} (错误: {e})")
            
            # 计算收益率
            def calculate_annualized_yield(buy_price, nav, days_held=1):
                if buy_price <= 0 or nav <= 0:
                    return 0.0
                single_period_yield = (nav - buy_price) / buy_price
                if days_held > 0:
                    annualized_yield = (1 + single_period_yield) ** (365 / days_held) - 1
                else:
                    annualized_yield = single_period_yield
                return annualized_yield * 100
            
            yield_rate_buy = calculate_annualized_yield(buy_price, nav_value, days_held)
            yield_rate_sell = calculate_annualized_yield(sell_price, nav_value, days_held)
            
            print(f"\n计算结果:")
            print(f"  以买入价计算的年化收益率: {yield_rate_buy:.4f}%")
            print(f"  以卖出价计算的年化收益率: {yield_rate_sell:.4f}%")
        
        conn.close()
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    debug_511880_yield()