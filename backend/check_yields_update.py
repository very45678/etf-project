import sqlite3

def check_yields_update():
    """检查收益率数据的更新状态"""
    try:
        conn = sqlite3.connect('fund_arb.db')
        cursor = conn.cursor()
        
        # 查询最新的收益率数据
        cursor.execute('SELECT * FROM yields ORDER BY yield_date DESC LIMIT 10')
        rows = cursor.fetchall()
        
        print('最新的收益率数据:')
        print('id | fund_code | yield_rate | yield_date | created_at | yield_rate_buy | yield_rate_sell')
        print('-' * 120)
        for row in rows:
            print(row)
        
        # 查询所有基金的最新收益率日期
        print('\n所有基金的最新收益率日期:')
        cursor.execute('SELECT fund_code, MAX(yield_date) as latest_date FROM yields GROUP BY fund_code')
        latest_yields = cursor.fetchall()
        for item in latest_yields:
            print(f"基金代码: {item[0]}, 最新收益率日期: {item[1]}")
        
        conn.close()
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    check_yields_update()