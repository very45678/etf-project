# demo_yield_calculator.py
import os
import sys
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from yield_calculator import calculate_annualized_yield, calculate_yields_for_all_funds, get_latest_yields, analyze_yield_trend
from data_store import get_prices, get_nav

def demo_basic_yield_calculation():
    """演示基本收益率计算"""
    print("=" * 50)
    print("基本收益率计算演示")
    print("=" * 50)
    
    # 演示不同情况下的年化收益率计算
    test_cases = [
        (100.5, 100.0, 1, "价格高于净值，持有1天"),
        (99.5, 100.0, 1, "价格低于净值，持有1天"),
        (100.5, 100.0, 7, "价格高于净值，持有7天"),
        (100.0, 100.0, 1, "价格等于净值，持有1天"),
    ]
    
    for price, nav, days, description in test_cases:
        yield_rate = calculate_annualized_yield(price, nav, days)
        print(f"{description}:")
        print(f"  价格: {price}, 净值: {nav}, 持有天数: {days}")
        print(f"  年化收益率: {yield_rate:.4f}%")
        print()

def demo_real_data_yield_calculation():
    """演示使用真实数据计算收益率"""
    print("=" * 50)
    print("真实数据收益率计算演示")
    print("=" * 50)
    
    # 获取最新的价格和净值数据
    prices = get_prices(limit=5)
    navs = get_nav(limit=5)
    
    if not prices or not navs:
        print("未找到足够的数据进行演示")
        return
    
    print("最新的价格数据:")
    for price in prices:
        print(f"  基金: {price[1]}, 价格: {price[2]}, 日期: {price[5]}")
    
    print("\n最新的净值数据:")
    for nav in navs:
        print(f"  基金: {nav[1]}, 净值: {nav[2]}, 日期: {nav[3]}")
    
    # 为所有基金计算收益率
    print("\n开始计算所有基金的收益率...")
    success_count = calculate_yields_for_all_funds()
    print(f"成功计算 {success_count} 只基金的收益率")

def demo_yield_analysis():
    """演示收益率分析功能"""
    print("=" * 50)
    print("收益率分析演示")
    print("=" * 50)
    
    # 获取最新的收益率数据
    yields_data = get_latest_yields(limit=10)
    
    if not yields_data:
        print("未找到收益率数据")
        return
    
    print("最新的收益率数据:")
    for yield_data in yields_data:
        print(f"  基金: {yield_data[1]}, 收益率: {yield_data[2]:.4f}%, 日期: {yield_data[3]}")
    
    # 分析收益率趋势
    if yields_data:
        fund_codes = list(set([yield_data[1] for yield_data in yields_data]))
        for fund_code in fund_codes[:2]:  # 只分析前2只基金
            print(f"\n分析基金 {fund_code} 的收益率趋势:")
            analysis = analyze_yield_trend(fund_code, days=7)
            if 'error' not in analysis:
                print(f"  当前收益率: {analysis['current_yield']:.4f}%")
                print(f"  平均收益率: {analysis['average_yield']:.4f}%")
                print(f"  最高收益率: {analysis['max_yield']:.4f}%")
                print(f"  最低收益率: {analysis['min_yield']:.4f}%")
                print(f"  趋势: {analysis['trend']}")
                print(f"  数据点数: {analysis['data_points']}")
            else:
                print(f"  分析失败: {analysis['error']}")

def main():
    """主演示函数"""
    print("收益率计算功能演示")
    print("=" * 60)
    
    # 演示基本收益率计算
    demo_basic_yield_calculation()
    
    # 演示真实数据收益率计算
    demo_real_data_yield_calculation()
    
    # 演示收益率分析
    demo_yield_analysis()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("收益率计算功能已成功实现，包括：")
    print("1. 年化收益率计算")
    print("2. 自动为所有基金计算收益率")
    print("3. 收益率数据存储")
    print("4. 收益率趋势分析")
    print("5. 集成到定时任务调度器")

if __name__ == '__main__':
    main()