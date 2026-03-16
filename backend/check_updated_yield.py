import sqlite3

def check_updated_yield():
    """检查511880的最新收益率数据"""
    try:
        conn = sqlite3.connect('fund_arb.db')
        cursor = conn.cursor()
        
        # 查询511880的最新收益率数据
        print("=== 511880最新收益率数据 ===")
        cursor.execute('SELECT * FROM yields WHERE fund_code = ? ORDER BY created_at DESC LIMIT 5', ('511880',))
        yield_rows = cursor.fetchall()
        print('id | fund_code | yield_rate | yield_date | created_at | yield_rate_buy | yield_rate_sell')
        print('-' * 120)
        for row in yield_rows:
            print(row)
        
        conn.close()
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    check_updated_yield()