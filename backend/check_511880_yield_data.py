import sqlite3

def check_511880_yield_data():
    """检查511880的收益率数据"""
    try:
        conn = sqlite3.connect('fund_arb.db')
        cursor = conn.cursor()
        
        # 查询511880的最新收益率数据
        print("=== 511880最新收益率数据 ===")
        cursor.execute('SELECT * FROM yields WHERE fund_code = ? ORDER BY created_at DESC LIMIT 10', ('511880',))
        yield_rows = cursor.fetchall()
        print('id | fund_code | yield_rate | yield_date | created_at | yield_rate_buy | yield_rate_sell')
        print('-' * 120)
        for row in yield_rows:
            print(row)
        
        # 查询511880的最新价格数据
        print("\n=== 511880最新价格数据 ===")
        cursor.execute('SELECT * FROM prices WHERE fund_code = ? ORDER BY created_at DESC LIMIT 10', ('511880',))
        price_rows = cursor.fetchall()
        print('id | fund_code | price | buy_price | sell_price | price_date | created_at')
        print('-' * 120)
        for row in price_rows:
            print(row)
        
        # 查询511880的最新净值数据
        print("\n=== 511880最新净值数据 ===")
        cursor.execute('SELECT * FROM nav WHERE fund_code = ? ORDER BY created_at DESC LIMIT 10', ('511880',))
        nav_rows = cursor.fetchall()
        print('id | fund_code | nav | nav_date | created_at')
        print('-' * 80)
        for row in nav_rows:
            print(row)
        
        conn.close()
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    check_511880_yield_data()