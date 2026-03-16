import sqlite3
from datetime import datetime

def verify_yield_calculation():
    """验证收益率计算问题"""
    try:
        conn = sqlite3.connect('fund_arb.db')
        cursor = conn.cursor()
        
        # 获取收益率计算时使用的价格数据（2026-03-09的价格）
        cursor.execute('SELECT * FROM prices WHERE fund_code = ? AND price_date = ? ORDER BY created_at DESC LIMIT 1', ('511880', '2026-03-09'))
        price_row = cursor.fetchone()
        print("=== 收益率计算时使用的价格数据 ===")
        print(f"价格日期: {price_row[5]}")
        print(f"买入价: {price_row[3]}")
        print(f"卖出价: {price_row[4]}")
        print(f"价格数据创建时间: {price_row[6]}")
        
        # 获取收益率计算时可能使用的旧净值数据（2026-03-03的净值）
        cursor.execute('SELECT * FROM nav WHERE fund_code = ? AND nav_date = ? ORDER BY created_at DESC LIMIT 1', ('511880', '2026-03-03'))
        old_nav_row = cursor.fetchone()
        print("\n=== 收益率计算时使用的旧净值数据 ===")
        print(f"净值日期: {old_nav_row[3]}")
        print(f"净值: {old_nav_row[2]}")
        print(f"净值数据创建时间: {old_nav_row[4]}")
        
        # 获取新的净值数据（2026-03-06的净值）
        cursor.execute('SELECT * FROM nav WHERE fund_code = ? AND nav_date = ? ORDER BY created_at DESC LIMIT 1', ('511880', '2026-03-06'))
        new_nav_row = cursor.fetchone()
        print("\n=== 新的净值数据 ===")
        print(f"净值日期: {new_nav_row[3]}")
        print(f"净值: {new_nav_row[2]}")
        print(f"净值数据创建时间: {new_nav_row[4]}")
        
        # 计算持有天数（价格日期 - 净值日期）
        price_date = datetime.strptime(price_row[5], '%Y-%m-%d')
        old_nav_date = datetime.strptime(old_nav_row[3], '%Y-%m-%d')
        new_nav_date = datetime.strptime(new_nav_row[3], '%Y-%m-%d')
        
        old_holding_days = (price_date - old_nav_date).days
        new_holding_days = (price_date - new_nav_date).days
        
        print(f"\n=== 持有天数计算 ===")
        print(f"使用旧净值的持有天数: {old_holding_days}天")
        print(f"使用新净值的持有天数: {new_holding_days}天")
        
        # 验证收益率计算
        def calculate_annualized_yield(nav, price, holding_days):
            """计算年化收益率"""
            if holding_days == 0:
                holding_days = 1
            # 单期收益率 = (赎回净值 - 买入价格) / 买入价格
            period_yield = (nav - price) / price
            # 年化收益率 = ((1 + 单期收益率) ^ (365 / 持有天数)) - 1
            annualized_yield = ((1 + period_yield) ** (365 / holding_days)) - 1
            return annualized_yield * 100
        
        # 使用旧净值计算
        old_yield_buy = calculate_annualized_yield(old_nav_row[2], price_row[3], old_holding_days)
        old_yield_sell = calculate_annualized_yield(old_nav_row[2], price_row[4], old_holding_days)
        
        # 使用新净值计算
        new_yield_buy = calculate_annualized_yield(new_nav_row[2], price_row[3], new_holding_days)
        new_yield_sell = calculate_annualized_yield(new_nav_row[2], price_row[4], new_holding_days)
        
        print(f"\n=== 收益率计算结果 ===")
        print(f"使用旧净值计算的买入价收益率: {old_yield_buy:.4f}%")
        print(f"使用旧净值计算的卖出价收益率: {old_yield_sell:.4f}%")
        print(f"使用新净值计算的买入价收益率: {new_yield_buy:.4f}%")
        print(f"使用新净值计算的卖出价收益率: {new_yield_sell:.4f}%")
        
        # 获取数据库中的收益率数据
        cursor.execute('SELECT * FROM yields WHERE fund_code = ? AND yield_date = ? ORDER BY created_at DESC LIMIT 1', ('511880', '2026-03-09'))
        yield_row = cursor.fetchone()
        print(f"\n=== 数据库中的收益率数据 ===")
        print(f"买入价收益率: {yield_row[5]:.4f}%")
        print(f"卖出价收益率: {yield_row[6]:.4f}%")
        
        conn.close()
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    verify_yield_calculation()