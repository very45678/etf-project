# test_arb_opportunity.py - 测试套利机会判断功能
from yield_calculator import check_arb_opportunity, check_arb_opportunities_for_all_funds

def test_check_arb_opportunity():
    """测试单个基金的套利机会判断"""
    print("测试单个基金的套利机会判断...")
    
    # 测试基金 511880
    fund_code = "511880"
    result = check_arb_opportunity(fund_code)
    print(f"{fund_code}基金套利机会判断结果:")
    if "error" in result:
        print(f"  错误: {result['error']}")
    else:
        print(f"  当前收益率: {result['当前收益率']:.4f}%")
        print(f"  存在套利机会: {result['存在套利机会']}")
    
    # 测试基金 511990
    fund_code = "511990"
    result = check_arb_opportunity(fund_code)
    print(f"\n{fund_code}基金套利机会判断结果:")
    if "error" in result:
        print(f"  错误: {result['error']}")
    else:
        print(f"  当前收益率: {result['当前收益率']:.4f}%")
        print(f"  存在套利机会: {result['存在套利机会']}")

def test_check_arb_opportunities_for_all_funds():
    """测试所有基金的套利机会判断"""
    print("\n测试所有基金的套利机会判断...")
    results = check_arb_opportunities_for_all_funds()
    
    if not results:
        print("未找到任何基金的收益率数据")
        return
    
    for result in results:
        print(f"\n基金 {result['fund_code']} 套利机会判断结果:")
        print(f"  当前收益率: {result['当前收益率']:.4f}%")
        print(f"  存在套利机会: {result['存在套利机会']}")

if __name__ == "__main__":
    print("套利机会判断功能测试")
    print("=" * 60)
    
    test_check_arb_opportunity()
    test_check_arb_opportunities_for_all_funds()
    
    print("\n" + "=" * 60)
    print("测试完成！")