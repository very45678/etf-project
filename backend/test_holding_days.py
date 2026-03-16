import sqlite3
from datetime import datetime

def calculate_holding_days(price_date, nav_date, has_matching_nav=False):
    """计算持有天数（考虑节假日和周末）"""
    try:
        price_dt = datetime.strptime(price_date, '%Y-%m-%d')
        nav_dt = datetime.strptime(nav_date, '%Y-%m-%d')
        
        # 如果有匹配的净值日期，使用实际天数差
        if has_matching_nav and nav_date == price_date:
            days_held = 1  # 日期相同，默认持有1天
        else:
            # 计算实际天数差
            days_held = abs((nav_dt - price_dt).days)
            
            # 如果没有匹配的净值日期（使用最新净值），考虑节假日
            if not has_matching_nav or nav_date != price_date:
                # 检查价格日期是星期几
                price_weekday = price_dt.weekday()  # 0=周一, 6=周日
                
                # 周五：默认持有3天（周五、周六、周日）
                if price_weekday == 4:  # 周五
                    days_held = 3
                # 周六：默认持有2天（周六、周日）
                elif price_weekday == 5:  # 周六
                    days_held = 2
                # 周日：默认持有1天（周日）
                elif price_weekday == 6:  # 周日
                    days_held = 1
                # 工作日：默认持有1天
                else:
                    days_held = 1
        return days_held
    except Exception:
        return 1  # 日期解析失败时默认持有1天

def test_holding_days():
    """测试持有天数计算"""
    test_cases = [
        # (price_date, nav_date, has_matching_nav, expected_days, description)
        ('2026-03-09', '2026-03-09', True, 1, '周一，有匹配净值'),
        ('2026-03-07', '2026-03-07', True, 1, '周六，有匹配净值'),
        ('2026-03-08', '2026-03-08', True, 1, '周日，有匹配净值'),
        ('2026-03-07', '2026-03-06', False, 2, '周六，无匹配净值'),
        ('2026-03-08', '2026-03-06', False, 1, '周日，无匹配净值'),
        ('2026-03-06', '2026-03-03', False, 3, '周五，无匹配净值'),
        ('2026-03-05', '2026-03-03', False, 1, '周四，无匹配净值'),
        ('2026-03-04', '2026-03-03', False, 1, '周三，无匹配净值'),
        ('2026-03-03', '2026-03-03', True, 1, '周二，有匹配净值'),
        ('2026-03-02', '2026-03-02', True, 1, '周一，有匹配净值'),
    ]
    
    print("=== 持有天数计算测试 ===")
    print("价格日期 | 净值日期 | 有匹配净值 | 计算结果 | 预期结果 | 描述")
    print("-" * 80)
    
    for price_date, nav_date, has_matching_nav, expected_days, description in test_cases:
        result = calculate_holding_days(price_date, nav_date, has_matching_nav)
        status = "✓" if result == expected_days else "✗"
        print(f"{price_date} | {nav_date} | {'是' if has_matching_nav else '否'} | {result} | {expected_days} | {status} {description}")

if __name__ == "__main__":
    test_holding_days()